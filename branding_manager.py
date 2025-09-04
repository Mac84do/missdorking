"""
Branding Manager for MissDorking™
Manages company logos, customer information, and professional branding
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import shutil
import uuid

class BrandingManager:
    def __init__(self):
        """Initialize the Branding Manager"""
        self.config_file = "branding_config.json"
        self.logos_dir = "company_logos"
        self.customer_logos_dir = "customer_logos"
        
        # Create directories if they don't exist
        os.makedirs(self.logos_dir, exist_ok=True)
        os.makedirs(self.customer_logos_dir, exist_ok=True)
        
        # Load existing configuration
        self.config = self.load_config()
    
    def load_config(self):
        """Load branding configuration from file"""
        default_config = {
            "company": {
                "name": "Your Company Name",
                "address": "123 Business Street\nCity, State 12345",
                "phone": "(555) 123-4567",
                "email": "contact@company.com",
                "website": "www.company.com",
                "logo_path": None
            },
            "customers": {},
            "branding_settings": {
                "primary_color": "#FF1493",  # Hot pink from original
                "secondary_color": "#00CCFF",  # Electric blue
                "accent_color": "#00FF88",  # Cyber green
                "font_family": "Arial",
                "report_template": "professional"
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to handle new keys
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
            else:
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def save_config(self):
        """Save branding configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def set_company_info(self, name, address, phone, email, website):
        """Set company information"""
        self.config["company"]["name"] = name
        self.config["company"]["address"] = address
        self.config["company"]["phone"] = phone
        self.config["company"]["email"] = email
        self.config["company"]["website"] = website
        self.save_config()
    
    def set_company_logo(self, logo_path):
        """Set company logo"""
        try:
            # Copy logo to logos directory
            filename = f"company_logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}" + os.path.splitext(logo_path)[1]
            dest_path = os.path.join(self.logos_dir, filename)
            shutil.copy2(logo_path, dest_path)
            
            # Update config
            self.config["company"]["logo_path"] = dest_path
            self.save_config()
            return dest_path
        except Exception as e:
            print(f"Error setting company logo: {e}")
            return None
    
    def add_customer(self, customer_id, name, company=None, address=None, phone=None, email=None, logo_path=None):
        """Add or update customer information"""
        customer_data = {
            "id": customer_id,
            "name": name,
            "company": company,
            "address": address,
            "phone": phone,
            "email": email,
            "logo_path": None,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        # Handle customer logo if provided
        if logo_path:
            try:
                filename = f"customer_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}" + os.path.splitext(logo_path)[1]
                dest_path = os.path.join(self.customer_logos_dir, filename)
                shutil.copy2(logo_path, dest_path)
                customer_data["logo_path"] = dest_path
            except Exception as e:
                print(f"Error setting customer logo: {e}")
        
        self.config["customers"][customer_id] = customer_data
        self.save_config()
        return customer_data
    
    def get_customer(self, customer_id):
        """Get customer information"""
        return self.config["customers"].get(customer_id, None)
    
    def get_all_customers(self):
        """Get all customers"""
        return self.config["customers"]
    
    def remove_customer(self, customer_id):
        """Remove customer"""
        if customer_id in self.config["customers"]:
            # Remove customer logo file if exists
            customer = self.config["customers"][customer_id]
            if customer.get("logo_path") and os.path.exists(customer["logo_path"]):
                try:
                    os.remove(customer["logo_path"])
                except Exception as e:
                    print(f"Error removing customer logo: {e}")
            
            del self.config["customers"][customer_id]
            self.save_config()
            return True
        return False
    
    def get_company_info(self):
        """Get company information"""
        return self.config["company"]
    
    def get_branding_settings(self):
        """Get branding settings"""
        return self.config["branding_settings"]
    
    def update_branding_settings(self, primary_color=None, secondary_color=None, accent_color=None, 
                                font_family=None, report_template=None):
        """Update branding settings"""
        settings = self.config["branding_settings"]
        if primary_color: settings["primary_color"] = primary_color
        if secondary_color: settings["secondary_color"] = secondary_color
        if accent_color: settings["accent_color"] = accent_color
        if font_family: settings["font_family"] = font_family
        if report_template: settings["report_template"] = report_template
        
        self.save_config()

class BrandingConfigWindow:
    def __init__(self, parent, branding_manager):
        """Initialize branding configuration window"""
        self.branding_manager = branding_manager
        self.window = tk.Toplevel(parent)
        self.window.title("🎨 Branding & Company Settings")
        self.window.geometry("800x700")
        self.window.resizable(True, True)
        
        # Configure dark theme
        self.window.configure(bg='#0a0a0a')
        
        self.create_widgets()
        self.load_current_settings()
    
    def create_widgets(self):
        """Create the branding configuration interface"""
        
        # Main container with scrollbar
        main_frame = tk.Frame(self.window, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎨 PROFESSIONAL BRANDING STUDIO",
            font=('Arial', 18, 'bold'),
            fg='#00CCFF',
            bg='#0a0a0a'
        )
        title_label.pack(pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Company Info Tab
        self.create_company_tab()
        
        # Customer Management Tab
        self.create_customer_tab()
        
        # Branding Settings Tab
        self.create_branding_tab()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#0a0a0a')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Save button
        save_button = tk.Button(
            buttons_frame,
            text="💾 Save All Settings",
            command=self.save_all_settings,
            bg='#00FF88',
            fg='#0a0a0a',
            font=('Arial', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=10
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Preview button
        preview_button = tk.Button(
            buttons_frame,
            text="👁️ Preview Report",
            command=self.preview_report,
            bg='#FF1493',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=10
        )
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_button = tk.Button(
            buttons_frame,
            text="❌ Close",
            command=self.window.destroy,
            bg='#666666',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=10
        )
        close_button.pack(side=tk.RIGHT)
    
    def create_company_tab(self):
        """Create company information tab"""
        company_frame = ttk.Frame(self.notebook)
        self.notebook.add(company_frame, text="🏢 Company Info")
        
        # Create scrollable frame
        canvas = tk.Canvas(company_frame, bg='#1a1a1a')
        scrollbar = ttk.Scrollbar(company_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Company form fields
        padding = {'padx': 20, 'pady': 10}
        
        # Company Name
        tk.Label(scrollable_frame, text="Company Name:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w', **padding)
        self.company_name_var = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=self.company_name_var, font=('Arial', 11),
                width=50, bg='#2a2a2a', fg='white', insertbackground='white').pack(anchor='w', **padding)
        
        # Company Address
        tk.Label(scrollable_frame, text="Address:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w', **padding)
        self.company_address_text = tk.Text(scrollable_frame, height=3, width=50, font=('Arial', 11),
                                          bg='#2a2a2a', fg='white', insertbackground='white')
        self.company_address_text.pack(anchor='w', **padding)
        
        # Phone
        tk.Label(scrollable_frame, text="Phone:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w', **padding)
        self.company_phone_var = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=self.company_phone_var, font=('Arial', 11),
                width=30, bg='#2a2a2a', fg='white', insertbackground='white').pack(anchor='w', **padding)
        
        # Email
        tk.Label(scrollable_frame, text="Email:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w', **padding)
        self.company_email_var = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=self.company_email_var, font=('Arial', 11),
                width=50, bg='#2a2a2a', fg='white', insertbackground='white').pack(anchor='w', **padding)
        
        # Website
        tk.Label(scrollable_frame, text="Website:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w', **padding)
        self.company_website_var = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=self.company_website_var, font=('Arial', 11),
                width=50, bg='#2a2a2a', fg='white', insertbackground='white').pack(anchor='w', **padding)
        
        # Logo section
        logo_frame = tk.Frame(scrollable_frame, bg='#1a1a1a')
        logo_frame.pack(anchor='w', **padding)
        
        tk.Label(logo_frame, text="Company Logo:", font=('Arial', 12, 'bold'), 
                fg='#00CCFF', bg='#1a1a1a').pack(anchor='w')
        
        logo_button_frame = tk.Frame(logo_frame, bg='#1a1a1a')
        logo_button_frame.pack(anchor='w', pady=5)
        
        self.logo_path_var = tk.StringVar()
        self.logo_path_label = tk.Label(logo_button_frame, textvariable=self.logo_path_var,
                                       font=('Arial', 9), fg='#888888', bg='#1a1a1a')
        self.logo_path_label.pack(anchor='w', pady=2)
        
        browse_logo_button = tk.Button(
            logo_button_frame,
            text="📁 Browse Logo...",
            command=self.browse_company_logo,
            bg='#FF1493',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        browse_logo_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Logo preview
        self.logo_preview_label = tk.Label(logo_frame, bg='#1a1a1a', text="No logo selected")
        self.logo_preview_label.pack(anchor='w', pady=10)
    
    def create_customer_tab(self):
        """Create customer management tab"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="👥 Customers")
        
        # Customer management interface
        tk.Label(customer_frame, text="Customer Management System", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Add customer button
        add_customer_button = tk.Button(
            customer_frame,
            text="➕ Add New Customer",
            command=self.add_customer_dialog,
            bg='#00FF88',
            fg='#0a0a0a',
            font=('Arial', 11, 'bold'),
            relief='flat'
        )
        add_customer_button.pack(pady=10)
        
        # Customer list
        self.customer_listbox = tk.Listbox(customer_frame, height=15, bg='#2a2a2a', 
                                         fg='white', selectbackground='#FF1493')
        self.customer_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Customer management buttons
        customer_buttons_frame = tk.Frame(customer_frame)
        customer_buttons_frame.pack(pady=10)
        
        edit_customer_button = tk.Button(
            customer_buttons_frame,
            text="✏️ Edit Customer",
            command=self.edit_customer_dialog,
            bg='#00CCFF',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        edit_customer_button.pack(side=tk.LEFT, padx=5)
        
        delete_customer_button = tk.Button(
            customer_buttons_frame,
            text="🗑️ Delete Customer",
            command=self.delete_customer,
            bg='#FF6B6B',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        delete_customer_button.pack(side=tk.LEFT, padx=5)
    
    def create_branding_tab(self):
        """Create branding settings tab"""
        branding_frame = ttk.Frame(self.notebook)
        self.notebook.add(branding_frame, text="🎨 Branding")
        
        tk.Label(branding_frame, text="Visual Branding Settings", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Color settings would go here
        # Font settings would go here
        # Template settings would go here
        
        # For now, just a placeholder
        tk.Label(branding_frame, text="🚧 Advanced branding options coming soon! 🚧",
                font=('Arial', 12), fg='orange').pack(pady=50)
    
    def browse_company_logo(self):
        """Browse for company logo"""
        file_path = filedialog.askopenfilename(
            title="Select Company Logo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.logo_path_var.set(file_path)
            self.update_logo_preview(file_path)
    
    def update_logo_preview(self, image_path):
        """Update logo preview"""
        try:
            # Load and resize image for preview
            image = Image.open(image_path)
            image.thumbnail((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update preview
            self.logo_preview_label.configure(image=photo, text="")
            self.logo_preview_label.image = photo  # Keep a reference
            
        except Exception as e:
            self.logo_preview_label.configure(text=f"Error loading image: {str(e)}", image="")
    
    def add_customer_dialog(self):
        """Show add customer dialog"""
        # This would open a dialog to add customer
        messagebox.showinfo("Feature", "Add customer dialog would open here!")
    
    def edit_customer_dialog(self):
        """Show edit customer dialog"""
        messagebox.showinfo("Feature", "Edit customer dialog would open here!")
    
    def delete_customer(self):
        """Delete selected customer"""
        selection = self.customer_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm", "Delete selected customer?"):
                messagebox.showinfo("Feature", "Customer would be deleted here!")
    
    def load_current_settings(self):
        """Load current settings into the form"""
        company_info = self.branding_manager.get_company_info()
        
        # Load company info
        self.company_name_var.set(company_info.get("name", ""))
        self.company_phone_var.set(company_info.get("phone", ""))
        self.company_email_var.set(company_info.get("email", ""))
        self.company_website_var.set(company_info.get("website", ""))
        
        # Load address
        address = company_info.get("address", "")
        self.company_address_text.delete(1.0, tk.END)
        self.company_address_text.insert(1.0, address)
        
        # Load logo
        logo_path = company_info.get("logo_path")
        if logo_path:
            self.logo_path_var.set(logo_path)
            if os.path.exists(logo_path):
                self.update_logo_preview(logo_path)
        
        # Load customers
        self.refresh_customer_list()
    
    def refresh_customer_list(self):
        """Refresh customer list"""
        self.customer_listbox.delete(0, tk.END)
        customers = self.branding_manager.get_all_customers()
        
        for customer_id, customer_data in customers.items():
            display_text = f"{customer_data.get('name', 'Unknown')} ({customer_id})"
            if customer_data.get('company'):
                display_text += f" - {customer_data['company']}"
            self.customer_listbox.insert(tk.END, display_text)
    
    def save_all_settings(self):
        """Save all settings"""
        try:
            # Save company info
            company_name = self.company_name_var.get()
            company_address = self.company_address_text.get(1.0, tk.END).strip()
            company_phone = self.company_phone_var.get()
            company_email = self.company_email_var.get()
            company_website = self.company_website_var.get()
            
            self.branding_manager.set_company_info(
                company_name, company_address, company_phone, 
                company_email, company_website
            )
            
            # Save logo if changed
            logo_path = self.logo_path_var.get()
            if logo_path and os.path.exists(logo_path):
                # Only save if it's a new path
                current_logo = self.branding_manager.get_company_info().get("logo_path")
                if logo_path != current_logo:
                    self.branding_manager.set_company_logo(logo_path)
            
            messagebox.showinfo("Success", "✅ All settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error saving settings: {str(e)}")
    
    def preview_report(self):
        """Preview how the branding will look in reports"""
        messagebox.showinfo("Preview", "📄 Report preview would show here with your branding!")


# Global branding manager instance
branding_manager = BrandingManager()

def show_branding_config(parent):
    """Show branding configuration window"""
    BrandingConfigWindow(parent, branding_manager)

def get_branding_manager():
    """Get the global branding manager instance"""
    return branding_manager

# Test the module
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    show_branding_config(root)
    root.mainloop()
