#!/usr/bin/env python3
"""
requirements-upload-gui.py

Simple Tkinter GUI to upload requirements from a CSV (headers: name,description,note)
to the configured API endpoint. Allows editing the API URL, Bearer token, and
selecting the CSV file on disk. Shows logs and a summary. Uses `requests` if
installed, otherwise falls back to urllib.

Run:
  python requirements-upload-gui.py

Notes:
 - This uses tkinter (built-in), no extra GUI deps required.
 - If you really need a pyautogui automation instead, tell me and I'll add it.
"""
from __future__ import annotations

import csv
import json
import logging
import threading
import time
import queue
import sys
from typing import Dict, Tuple

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
except Exception:  # pragma: no cover - tkinter should be available on most installs
    print("tkinter is required for this GUI. Please install or run the CLI script instead.")
    raise

DEFAULT_URL = "https://elgu-r10-training-ws.oueg.info/api/v1/administrators/requirements"
DEFAULT_TOKEN = "8785|OrGgcCvakZB2EmvFE471nWCIhqj4WQMTWIdrxrh5e6f666f9"


def try_import_requests():
    try:
        import requests

        return requests
    except Exception:
        return None


REQUESTS = try_import_requests()


def post_with_requests(url: str, token: str, payload: Dict) -> Tuple[int, str]:
    requests = REQUESTS
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    session = requests.Session()
    resp = session.post(url, headers=headers, json=payload, timeout=30)
    return resp.status_code, resp.text


def post_with_urllib(url: str, token: str, payload: Dict) -> Tuple[int, str]:
    import ssl
    from urllib import request, error

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    ctx = ssl.create_default_context()
    try:
        with request.urlopen(req, context=ctx, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.getcode(), body
    except error.HTTPError as he:
        try:
            body = he.read().decode("utf-8", errors="replace")
        except Exception:
            body = str(he)
        return he.code, body
    except Exception as e:
        return 0, str(e)


def read_csv_rows(path: str):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        expected = {"name", "description", "note"}
        headers = {h.strip().lower() for h in reader.fieldnames or []}
        if not expected.issubset(headers):
            raise ValueError(f"CSV must contain headers: name,description,note (found: {reader.fieldnames})")
        for row in reader:
            yield {
                "name": row.get("name") or row.get("Name") or "",
                "description": row.get("description") or row.get("Description") or "",
                "note": row.get("note") or row.get("Note") or "",
            }


class UploaderThread(threading.Thread):
    def __init__(self, url: str, token: str, csvpath: str, queue_out: queue.Queue, dry_run: bool = False):
        super().__init__(daemon=True)
        self.url = url
        self.token = token
        self.csvpath = csvpath
        self.queue_out = queue_out
        self.dry_run = dry_run

    def log(self, *parts):
        self.queue_out.put(("log", " ".join(str(p) for p in parts)))

    def run(self):
        total = 0
        success = 0
        failed = 0
        try:
            rows = list(read_csv_rows(self.csvpath))
        except Exception as e:
            self.queue_out.put(("error", f"Failed to read CSV: {e}"))
            return

        self.log(f"Read {len(rows)} rows from CSV")

        for item in rows:
            total += 1
            payload = {k: (v or "").strip() for k, v in item.items()}

            if self.dry_run:
                self.queue_out.put(("payload", json.dumps(payload, ensure_ascii=False)))
                success += 1
                continue

            try:
                if REQUESTS:
                    status, text = post_with_requests(self.url, self.token, payload)
                else:
                    status, text = post_with_urllib(self.url, self.token, payload)
            except Exception as e:
                status, text = 0, str(e)

            if 200 <= status < 300:
                success += 1
                self.log(f"Uploaded: {payload.get('name')!r} -> {status}")
            else:
                failed += 1
                self.queue_out.put(("error", f"Failed {payload.get('name')!r} -> {status}: {text}"))

            # polite pacing
            time.sleep(0.2)

        self.queue_out.put(("summary", {"total": total, "success": success, "failed": failed}))


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Requirements Uploader")

        self.queue_out: queue.Queue = queue.Queue()

        frm = tk.Frame(root)
        frm.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(frm, text="API URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_var = tk.StringVar(value=DEFAULT_URL)
        tk.Entry(frm, textvariable=self.url_var, width=80).grid(row=0, column=1, sticky=tk.W)

        tk.Label(frm, text="Token:").grid(row=1, column=0, sticky=tk.W)
        self.token_var = tk.StringVar(value=DEFAULT_TOKEN)
        tk.Entry(frm, textvariable=self.token_var, width=80,).grid(row=1, column=1, sticky=tk.W)

        tk.Label(frm, text="CSV:").grid(row=2, column=0, sticky=tk.W)
        self.csv_label = tk.StringVar(value="(no file selected)")
        tk.Label(frm, textvariable=self.csv_label).grid(row=2, column=1, sticky=tk.W)
        tk.Button(frm, text="Choose CSV", command=self.choose_csv).grid(row=2, column=2, sticky=tk.W)

        btn_frm = tk.Frame(root)
        btn_frm.pack(fill=tk.X, padx=10, pady=6)
        tk.Button(btn_frm, text="Dry Run", command=self.dry_run).pack(side=tk.LEFT)
        tk.Button(btn_frm, text="Upload", command=self.upload).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frm, text="Quit", command=root.quit).pack(side=tk.RIGHT)

        self.logbox = ScrolledText(root, height=15, width=100)
        self.logbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.csv_path = None

        # schedule queue polling
        self.root.after(200, self.poll_queue)

    def choose_csv(self):
        p = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv"), ("All files", "*")])
        if p:
            self.csv_path = p
            self.csv_label.set(p)
            self.append_log(f"Selected CSV: {p}")

    def append_log(self, text: str):
        self.logbox.insert(tk.END, text + "\n")
        self.logbox.see(tk.END)

    def dry_run(self):
        if not self.csv_path:
            messagebox.showwarning("No CSV", "Please choose a CSV file first")
            return
        self.append_log("Starting dry-run...")
        t = UploaderThread(self.url_var.get().strip(), self.token_var.get().strip(), self.csv_path, self.queue_out, dry_run=True)
        t.start()

    def upload(self):
        if not self.csv_path:
            messagebox.showwarning("No CSV", "Please choose a CSV file first")
            return
        if not messagebox.askyesno("Confirm Upload", "Are you sure you want to upload all rows to the API?"):
            return
        self.append_log("Starting upload...")
        t = UploaderThread(self.url_var.get().strip(), self.token_var.get().strip(), self.csv_path, self.queue_out, dry_run=False)
        t.start()

    def poll_queue(self):
        try:
            while True:
                typ, payload = self.queue_out.get_nowait()
                if typ == "log":
                    self.append_log(str(payload))
                elif typ == "error":
                    self.append_log("ERROR: " + str(payload))
                elif typ == "payload":
                    self.append_log("DRY-PAYLOAD: " + str(payload))
                elif typ == "summary":
                    s = payload
                    self.append_log(f"Summary: total={s.get('total')} success={s.get('success')} failed={s.get('failed')}")
                else:
                    self.append_log(f"{typ}: {payload}")
        except queue.Empty:
            pass
        finally:
            self.root.after(200, self.poll_queue)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
