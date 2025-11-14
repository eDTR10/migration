import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re
from datetime import datetime

class BusinessRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Registration CSV Generator")
        self.root.geometry("900x700")
        
        self.records = []
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Title
        title = ttk.Label(scrollable_frame, text="Business Registration Form", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        row = 1
        
        # Business Information Section
        ttk.Label(scrollable_frame, text="BUSINESS INFORMATION", 
                 font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10,5))
        row += 1
        
        # BIN
        ttk.Label(scrollable_frame, text="*BIN (0000000-0000-0000000):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.bin_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.bin_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Business Name
        ttk.Label(scrollable_frame, text="*Business Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.business_name_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.business_name_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Trade Name
        ttk.Label(scrollable_frame, text="Trade Name (optional):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.trade_name_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.trade_name_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Business Type
        ttk.Label(scrollable_frame, text="*Business Type:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.business_type_var = tk.StringVar()
        business_types = ["SOLE PROPRIETORSHIP", "ONE PERSON CORPORATION", "PARTNERSHIP", "CORPORATION", "COOPERATIVE"]
        business_combo = ttk.Combobox(scrollable_frame, textvariable=self.business_type_var, values=business_types, width=28, state="readonly")
        business_combo.grid(row=row, column=1, sticky="w", pady=2)
        business_combo.bind("<<ComboboxSelected>>", self.on_business_type_change)
        row += 1
        
        # DTI Number
        ttk.Label(scrollable_frame, text="DTI Number:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.dti_var = tk.StringVar()
        self.dti_entry = ttk.Entry(scrollable_frame, textvariable=self.dti_var, width=30, state="disabled")
        self.dti_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # SEC Number
        ttk.Label(scrollable_frame, text="SEC Number:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.sec_var = tk.StringVar()
        self.sec_entry = ttk.Entry(scrollable_frame, textvariable=self.sec_var, width=30, state="disabled")
        self.sec_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # CDA Number
        ttk.Label(scrollable_frame, text="CDA Number:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.cda_var = tk.StringVar()
        self.cda_entry = ttk.Entry(scrollable_frame, textvariable=self.cda_var, width=30, state="disabled")
        self.cda_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # TIN
        ttk.Label(scrollable_frame, text="TIN (000-000-000-00000):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.tin_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.tin_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Contact Information Section
        ttk.Label(scrollable_frame, text="CONTACT INFORMATION", 
                 font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10,5))
        row += 1
        
        # Email
        ttk.Label(scrollable_frame, text="*Email Address:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.email_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Cellphone
        ttk.Label(scrollable_frame, text="*Cellphone (639XXXXXXXXX):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.cellphone_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.cellphone_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Telephone
        ttk.Label(scrollable_frame, text="Telephone:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.telephone_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.telephone_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Person in Charge Section
        ttk.Label(scrollable_frame, text="PERSON IN CHARGE", 
                 font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10,5))
        row += 1
        
        # First Name
        ttk.Label(scrollable_frame, text="*First Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_fname_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_fname_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Middle Name
        ttk.Label(scrollable_frame, text="Middle Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_mname_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_mname_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Last Name
        ttk.Label(scrollable_frame, text="*Last Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_lname_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_lname_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Extension Name
        ttk.Label(scrollable_frame, text="Extension (no period):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_ext_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_ext_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Sex
        ttk.Label(scrollable_frame, text="*Sex:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_sex_var = tk.StringVar()
        sex_frame = ttk.Frame(scrollable_frame)
        sex_frame.grid(row=row, column=1, sticky="w", pady=2)
        ttk.Radiobutton(sex_frame, text="Male", variable=self.incharge_sex_var, value="M").pack(side=tk.LEFT)
        ttk.Radiobutton(sex_frame, text="Female", variable=self.incharge_sex_var, value="F").pack(side=tk.LEFT)
        row += 1
        
        # Country of Citizenship
        ttk.Label(scrollable_frame, text="*Country of Citizenship:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_country_var = tk.StringVar(value="Philippines")
        ttk.Entry(scrollable_frame, textvariable=self.incharge_country_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # In-Charge Address
        ttk.Label(scrollable_frame, text="Street:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_street_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_street_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Barangay:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_barangay_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_barangay_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Municipality:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_municipality_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_municipality_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Province:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.incharge_province_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.incharge_province_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Office Address Section
        ttk.Label(scrollable_frame, text="OFFICE ADDRESS", 
                 font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10,5))
        row += 1
        
        ttk.Label(scrollable_frame, text="Office Street:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.office_street_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.office_street_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="*Office Barangay Code:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.office_barangay_code_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.office_barangay_code_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Location Ownership
        ttk.Label(scrollable_frame, text="*Location:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.location_owned_var = tk.StringVar()
        location_frame = ttk.Frame(scrollable_frame)
        location_frame.grid(row=row, column=1, sticky="w", pady=2)
        ttk.Radiobutton(location_frame, text="Owned", variable=self.location_owned_var, 
                       value="1", command=self.on_location_change).pack(side=tk.LEFT)
        ttk.Radiobutton(location_frame, text="Rented", variable=self.location_owned_var, 
                       value="0", command=self.on_location_change).pack(side=tk.LEFT)
        row += 1
        
        # TDN Number
        ttk.Label(scrollable_frame, text="TDN Number:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.tdn_var = tk.StringVar()
        self.tdn_entry = ttk.Entry(scrollable_frame, textvariable=self.tdn_var, width=30, state="disabled")
        self.tdn_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # PIN Number
        ttk.Label(scrollable_frame, text="PIN Number:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.pin_var = tk.StringVar()
        self.pin_entry = ttk.Entry(scrollable_frame, textvariable=self.pin_var, width=30, state="disabled")
        self.pin_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Lessor Name
        ttk.Label(scrollable_frame, text="Lessor Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.lessor_var = tk.StringVar()
        self.lessor_entry = ttk.Entry(scrollable_frame, textvariable=self.lessor_var, width=30, state="disabled")
        self.lessor_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Monthly Rental
        ttk.Label(scrollable_frame, text="Monthly Rental:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.rental_var = tk.StringVar()
        self.rental_entry = ttk.Entry(scrollable_frame, textvariable=self.rental_var, width=30, state="disabled")
        self.rental_entry.grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Business Details Section
        ttk.Label(scrollable_frame, text="BUSINESS DETAILS", 
                 font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10,5))
        row += 1
        
        # Area
        ttk.Label(scrollable_frame, text="*Total Floor Area (sqm):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.area_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.area_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Male Employees
        ttk.Label(scrollable_frame, text="*Male Employees:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.male_emp_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.male_emp_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Female Employees
        ttk.Label(scrollable_frame, text="*Female Employees:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.female_emp_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.female_emp_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Employees within LGU
        ttk.Label(scrollable_frame, text="*Employees within LGU:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.emp_in_lgu_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.emp_in_lgu_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Vehicles
        ttk.Label(scrollable_frame, text="*Number of Vans:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.van_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.van_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="*Number of Trucks:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.truck_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.truck_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="*Number of Motorcycles:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.motorcycle_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.motorcycle_var, width=30).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Activity Type
        ttk.Label(scrollable_frame, text="*Activity Type:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.activity_var = tk.StringVar()
        activity_types = ["Main Office", "Branch Office", "Admin Office Only", "Warehouse", "Others"]
        ttk.Combobox(scrollable_frame, textvariable=self.activity_var, values=activity_types, width=28).grid(row=row, column=1, sticky="w", pady=2)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=f"Generate CSV ({len(self.records)} records)", 
                  command=self.generate_csv).pack(side=tk.LEFT, padx=5)
        
        self.button_frame = button_frame
        
    def on_business_type_change(self, event=None):
        """Enable/disable registration number fields based on business type"""
        business_type = self.business_type_var.get()
        
        # Disable all first
        self.dti_entry.config(state="disabled")
        self.sec_entry.config(state="disabled")
        self.cda_entry.config(state="disabled")
        
        # Clear values
        self.dti_var.set("")
        self.sec_var.set("")
        self.cda_var.set("")
        
        # Enable based on type
        if business_type == "SOLE PROPRIETORSHIP":
            self.dti_entry.config(state="normal")
        elif business_type in ["ONE PERSON CORPORATION", "PARTNERSHIP", "CORPORATION"]:
            self.sec_entry.config(state="normal")
        elif business_type == "COOPERATIVE":
            self.cda_entry.config(state="normal")
    
    def on_location_change(self):
        """Enable/disable location fields based on ownership"""
        if self.location_owned_var.get() == "1":  # Owned
            self.tdn_entry.config(state="normal")
            self.pin_entry.config(state="normal")
            self.lessor_entry.config(state="disabled")
            self.rental_entry.config(state="disabled")
            self.lessor_var.set("")
            self.rental_var.set("")
        else:  # Rented
            self.tdn_entry.config(state="disabled")
            self.pin_entry.config(state="disabled")
            self.lessor_entry.config(state="normal")
            self.rental_entry.config(state="normal")
            self.tdn_var.set("")
            self.pin_var.set("")
    
    def validate_bin(self, bin_val):
        """Validate BIN format"""
        pattern = r'^\d{7}-\d{4}-\d{7}$'
        return bool(re.match(pattern, bin_val))
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_cellphone(self, phone):
        """Validate cellphone format"""
        pattern = r'^639\d{9}$'
        return bool(re.match(pattern, phone))
    
    def validate_tin(self, tin):
        """Validate TIN format"""
        if not tin:
            return True  # Optional field
        pattern = r'^\d{3}-\d{3}-\d{3}-\d{5}$'
        return bool(re.match(pattern, tin))
    
    def add_record(self):
        """Validate and add record to list"""
        # Validate required fields
        if not self.bin_var.get():
            messagebox.showerror("Error", "BIN is required!")
            return
        
        if not self.validate_bin(self.bin_var.get()):
            messagebox.showerror("Error", "Invalid BIN format! Use: 0000000-0000-0000000")
            return
        
        if not self.business_name_var.get() or len(self.business_name_var.get()) < 3:
            messagebox.showerror("Error", "Business Name must be at least 3 characters!")
            return
        
        if not self.business_type_var.get():
            messagebox.showerror("Error", "Business Type is required!")
            return
        
        # Validate conditional registration numbers
        business_type = self.business_type_var.get()
        if business_type == "SOLE PROPRIETORSHIP" and not self.dti_var.get():
            messagebox.showerror("Error", "DTI Number is required for Sole Proprietorship!")
            return
        elif business_type in ["ONE PERSON CORPORATION", "PARTNERSHIP", "CORPORATION"] and not self.sec_var.get():
            messagebox.showerror("Error", "SEC Number is required for this business type!")
            return
        elif business_type == "COOPERATIVE" and not self.cda_var.get():
            messagebox.showerror("Error", "CDA Number is required for Cooperative!")
            return
        
        if not self.validate_tin(self.tin_var.get()):
            messagebox.showerror("Error", "Invalid TIN format! Use: 000-000-000-00000")
            return
        
        if not self.email_var.get():
            messagebox.showerror("Error", "Email is required!")
            return
        
        if not self.validate_email(self.email_var.get()):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        if not self.cellphone_var.get():
            messagebox.showerror("Error", "Cellphone is required!")
            return
        
        if not self.validate_cellphone(self.cellphone_var.get()):
            messagebox.showerror("Error", "Invalid cellphone format! Use: 639XXXXXXXXX")
            return
        
        if not self.incharge_fname_var.get():
            messagebox.showerror("Error", "In-Charge First Name is required!")
            return
        
        if not self.incharge_lname_var.get():
            messagebox.showerror("Error", "In-Charge Last Name is required!")
            return
        
        if not self.incharge_sex_var.get():
            messagebox.showerror("Error", "In-Charge Sex is required!")
            return
        
        if not self.incharge_country_var.get():
            messagebox.showerror("Error", "Country of Citizenship is required!")
            return
        
        if not self.office_barangay_code_var.get():
            messagebox.showerror("Error", "Office Barangay Code is required!")
            return
        
        if not self.location_owned_var.get():
            messagebox.showerror("Error", "Location ownership status is required!")
            return
        
        # Validate location-specific fields
        if self.location_owned_var.get() == "1":  # Owned
            if not self.tdn_var.get() and not self.pin_var.get():
                messagebox.showerror("Error", "Either TDN or PIN is required for owned property!")
                return
        else:  # Rented
            if not self.lessor_var.get():
                messagebox.showerror("Error", "Lessor Name is required for rented property!")
                return
            if not self.rental_var.get():
                messagebox.showerror("Error", "Monthly Rental is required for rented property!")
                return
        
        if not self.area_var.get():
            messagebox.showerror("Error", "Total Floor Area is required!")
            return
        
        # Validate employee counts
        try:
            male_emp = int(self.male_emp_var.get())
            female_emp = int(self.female_emp_var.get())
            emp_in_lgu = int(self.emp_in_lgu_var.get())
            total_emp = male_emp + female_emp
            
            if emp_in_lgu > total_emp:
                messagebox.showerror("Error", f"Employees within LGU cannot exceed total employees ({total_emp})!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid employee count!")
            return
        
        if not self.activity_var.get():
            messagebox.showerror("Error", "Activity Type is required!")
            return
        
        # Create record
        record = {
            'bin': self.bin_var.get(),
            'business_name': self.business_name_var.get(),
            'trade_name': self.trade_name_var.get(),
            'business_type': self.business_type_var.get(),
            'dti_no': self.dti_var.get(),
            'sec_no': self.sec_var.get(),
            'cda_no': self.cda_var.get(),
            'tin_no': self.tin_var.get(),
            'email_address': self.email_var.get(),
            'cellphone_no': self.cellphone_var.get(),
            'telephone_no': self.telephone_var.get(),
            'incharge_first_name': self.incharge_fname_var.get(),
            'incharge_middle_name': self.incharge_mname_var.get(),
            'incharge_last_name': self.incharge_lname_var.get(),
            'incharge_extension_name': self.incharge_ext_var.get(),
            'incharge_sex': self.incharge_sex_var.get(),
            'incharge_country_of_citizenship': self.incharge_country_var.get(),
            'incharge_street': self.incharge_street_var.get(),
            'incharge_barangay': self.incharge_barangay_var.get(),
            'incharge_municipality': self.incharge_municipality_var.get(),
            'incharge_province': self.incharge_province_var.get(),
            'office_street': self.office_street_var.get(),
            'office_barangay_code': self.office_barangay_code_var.get(),
            'location_owned': self.location_owned_var.get(),
            'tdn_no': self.tdn_var.get(),
            'pin_no': self.pin_var.get(),
            'lessor_name': self.lessor_var.get(),
            'monthly_rental': self.rental_var.get(),
            'area': self.area_var.get(),
            'no_of_male_employees': self.male_emp_var.get(),
            'no_of_female_employees': self.female_emp_var.get(),
            'no_of_employees_residing_within_the_area': self.emp_in_lgu_var.get(),
            'no_of_van': self.van_var.get(),
            'no_of_truck': self.truck_var.get(),
            'no_of_motorcycle': self.motorcycle_var.get(),
            'activity_type': self.activity_var.get()
        }
        
        self.records.append(record)
        messagebox.showinfo("Success", f"Record added! Total records: {len(self.records)}")
        
        # Update button text
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, ttk.Button) and "Generate CSV" in widget.cget("text"):
                widget.config(text=f"Generate CSV ({len(self.records)} records)")
        
        self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        self.bin_var.set("")
        self.business_name_var.set("")
        self.trade_name_var.set("")
        self.business_type_var.set("")
        self.dti_var.set("")
        self.sec_var.set("")
        self.cda_var.set("")
        self.tin_var.set("")
        self.email_var.set("")
        self.cellphone_var.set("")
        self.telephone_var.set("")
        self.incharge_fname_var.set("")
        self.incharge_mname_var.set("")
        self.incharge_lname_var.set("")
        self.incharge_ext_var.set("")
        self.incharge_sex_var.set("")
        self.incharge_country_var.set("Philippines")
        self.incharge_street_var.set("")
        self.incharge_barangay_var.set("")
        self.incharge_municipality_var.set("")
        self.incharge_province_var.set("")
        self.office_street_var.set("")
        self.office_barangay_code_var.set("")
        self.location_owned_var.set("")
        self.tdn_var.set("")
        self.pin_var.set("")
        self.lessor_var.set("")
        self.rental_var.set("")
        self.area_var.set("")
        self.male_emp_var.set("0")
        self.female_emp_var.set("0")
        self.emp_in_lgu_var.set("0")
        self.van_var.set("0")
        self.truck_var.set("0")
        self.motorcycle_var.set("0")
        self.activity_var.set("")
        
        # Reset entry states
        self.dti_entry.config(state="disabled")
        self.sec_entry.config(state="disabled")
        self.cda_entry.config(state="disabled")
        self.tdn_entry.config(state="disabled")
        self.pin_entry.config(state="disabled")
        self.lessor_entry.config(state="disabled")
        self.rental_entry.config(state="disabled")
    
    def generate_csv(self):
        """Generate CSV file from records"""
        if not self.records:
            messagebox.showwarning("Warning", "No records to generate!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"business_registration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return
        
        fieldnames = [
            'bin', 'business_name', 'trade_name', 'business_type', 'dti_no', 'sec_no', 'cda_no',
            'tin_no', 'email_address', 'cellphone_no', 'telephone_no', 'incharge_first_name',
            'incharge_middle_name', 'incharge_last_name', 'incharge_extension_name', 'incharge_sex',
            'incharge_country_of_citizenship', 'incharge_street', 'incharge_barangay',
            'incharge_municipality', 'incharge_province', 'office_street', 'office_barangay_code',
            'location_owned', 'tdn_no', 'pin_no', 'lessor_name', 'monthly_rental', 'area',
            'no_of_male_employees', 'no_of_female_employees', 'no_of_employees_residing_within_the_area',
            'no_of_van', 'no_of_truck', 'no_of_motorcycle', 'activity_type'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.records)
            
            messagebox.showinfo("Success", f"CSV file generated successfully!\n\nFile: {filename}\nRecords: {len(self.records)}")
            
            # Ask if user wants to clear records
            if messagebox.askyesno("Clear Records?", "Do you want to clear all records and start fresh?"):
                self.records = []
                for widget in self.button_frame.winfo_children():
                    if isinstance(widget, ttk.Button) and "Generate CSV" in widget.cget("text"):
                        widget.config(text=f"Generate CSV ({len(self.records)} records)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate CSV: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessRegistrationApp(root)
    root.mainloop()