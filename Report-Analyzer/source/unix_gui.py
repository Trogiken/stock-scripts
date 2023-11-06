import sys
import time

try:
    import tkinter as tk
    from tkinter import filedialog
    import webbrowser
    from PIL import Image, ImageTk
    import pandas as pd
    from source.csv_functions import analyze_data, export_html
except ImportError:
    print("Please install the required packages: pip install -r requirements.txt")
    input("\nPress ENTER to exit...")
    sys.exit()


class GUI:
    def __init__(self, version):
        self.version = version

        # Create the Tkinter root
        self.root = tk.Tk()
        self.root.title("Report Analyzer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.iconphoto(False, tk.PhotoImage(data="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"))

        # Create a frame with padding
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame.config(padx=15, pady=15, background='teal', highlightbackground='black', highlightthickness=2)

        # Create a container frame
        self.container_frame = tk.Frame(self.content_frame)
        self.container_frame.pack(fill=tk.BOTH, expand=True)
        self.container_frame.config(padx=20, pady=20)

        # Create a horizontal frame for radio buttons
        self.radio_button_frame = tk.Frame(self.container_frame)
        self.radio_button_frame.pack(fill=tk.BOTH, expand=True)

        # Create a vertical frame for the file buttons
        self.file_button_frame = tk.Frame(self.container_frame)
        self.file_button_frame.pack(fill=tk.BOTH, expand=True)  

        # Create a frame for the version label
        self.version_frame = tk.Frame(self.container_frame)
        self.version_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize values
        self.radio_var = tk.IntVar()
        self.radio_var.set(4)
        self.account_history_path = ""
    
    def is_valid_csv(self, file_path):
        """Check if the selected CSV file is valid"""
        try:
            csv_file = pd.read_csv(file_path, sep=',')
            for column in csv_file.columns:
                if column not in ['Time', 'Balance Before', 'Balance After', 'P&L', 'Action']:
                    return False
            return True
        except:
            return False
        
    def create_overlay(self, message):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        image = Image.new('RGBA', (width, height), (128, 128, 128, 128))  # Semi-transparent grey

        # Create a PhotoImage from the image
        photo = ImageTk.PhotoImage(image)

        # Create the overlay and set the image as its background
        overlay = tk.Label(self.root, image=photo)
        overlay.image = photo  # Keep a reference to the image
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        label = tk.Label(overlay, text=message, font=('Arial', 14), bg='grey')
        label.place(relx=0.5, rely=0.5, anchor='c')

        self.root.update()
        time.sleep(1)

        return overlay
    
    def get_account_path(self):
        """Open csv file and store path in global variable"""
        self.account_history_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.account_history_path:
            return
        
        if self.is_valid_csv(self.account_history_path):
            self.acc_button.configure(bg='green', fg='white')
            self.export_button.configure(bg='blue', fg='white')
        else:
            tk.messagebox.showerror("Error", f"Please select a valid 'Account History' file.")
            self.account_history_path = ""
            self.acc_button.configure(bg='grey', fg='black')
            self.export_button.configure(bg='red', fg='white')

    def export(self):
        """Check if both csv files are selected, analyze data, and export html file"""
        if not self.account_history_path:
            return
        
        export_location = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if not export_location:
            return
        
        overlay = self.create_overlay("Exporting...")
        try:
            data_frames = analyze_data(self.account_history_path, self.radio_var.get())
        except:
            tk.messagebox.showerror("Error", f"An error occurred while analyzing the data.")
            overlay.destroy()
            return
        
        try:
            export_html(data_frames, export_location)
            overlay.destroy()
            if tk.messagebox.askyesno("Success", "HTML file exported successfully. Do you want to open it?"):
                webbrowser.open(export_location)  # TODO This does not work on Mac and Linux
        except:
            tk.messagebox.showerror("Error", "An error occurred while exporting the HTML file.")
            overlay.destroy()
            return

        overlay.destroy()

    def on_enter(self, event):
        # TODO Highlights look bad on Mac and Linux
        event.widget.original_highlightbackground = event.widget.cget("highlightbackground")
        event.widget.original_highlightthickness = event.widget.cget("highlightthickness")
        event.widget.original_borderwidth = event.widget.cget("borderwidth")
        event.widget.config(highlightbackground='black', highlightthickness=2, borderwidth=3)

    def on_leave(self, event):
        event.widget.config(highlightbackground=event.widget.original_highlightbackground, highlightthickness=event.widget.original_highlightthickness, borderwidth=event.widget.original_borderwidth)
    
    def run(self):
        # Create and label radio buttons
        # TODO Title is too small on Mac and Linux
        report_title_label = tk.Label(self.radio_button_frame, text="Time Frame of Report")
        report_title_label.pack(side=tk.TOP, anchor=tk.N)
        report_title_label.config(font=('Arial', 12))

        # TODO These buttons are not cented or any OS
        tk.Radiobutton(self.radio_button_frame, text="Daily", variable=self.radio_var, value=1, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Monthly", variable=self.radio_var, value=2, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Quarterly", variable=self.radio_var, value=3, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Yearly", variable=self.radio_var, value=4, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)

        # Account History button
        self.acc_button = tk.Button(self.file_button_frame, text="Select Account History CSV", command=self.get_account_path)
        self.acc_button.configure(bg='grey', fg='black', font=('Arial', 12), width=30)
        self.acc_button.pack(pady=2)

        # Export HTML button
        # TODO This color scheme doesn't show up on Mac and Linux
        self.export_button = tk.Button(self.file_button_frame, text="Export HTML", command=self.export)
        self.export_button.configure(bg='red', fg='white', font=('Arial', 12), width=30)
        self.export_button.pack(pady=2)

        # Bind enter and leave events to change button borders
        self.acc_button.bind("<Enter>", self.on_enter)
        self.acc_button.bind("<Leave>", self.on_leave)

        self.export_button.bind("<Enter>", self.on_enter)
        self.export_button.bind("<Leave>", self.on_leave)

        # Create version label
        version_label = tk.Label(self.version_frame, text=f"Version {self.version}", font=('Arial', 10))
        version_label.pack(side=tk.RIGHT, anchor=tk.S)

        self.root.mainloop()
