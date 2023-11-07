import sys
import time
from source.csv_functions import analyze_data, export_html
from source.version_check import get_latest

try:
    import tkinter as tk
    import pandas as pd
    import subprocess
    import webbrowser
    from PIL import Image, ImageTk
    from tkinter import filedialog
except ImportError as e:
    print("Please install the required packages: pip install -r requirements.txt")
    input("\nPress ENTER to exit...")
    sys.exit()


class GUI:
    """
    This class creates the GUI for the program

    Attributes:
        os (str): The operating system the program is running on
        version (str): The version of the program
        theme (dict): The theme of the GUI
        root (tk.Tk): The Tkinter root
        content_frame (tk.Frame): The frame that contains all the other frames
        container_frame (tk.Frame): The frame that contains the radio button frame, file button frame, and version frame
        radio_button_frame (tk.Frame): The frame that contains the radio buttons
        file_button_frame (tk.Frame): The frame that contains the file buttons
        version_frame (tk.Frame): The frame that contains the version label
        radio_var (tk.IntVar): The variable that stores the value of the radio buttons
        account_history_path (str): The path to the account history csv file

    Methods:
        hide_update_frame() -> None: Hide the update frame
        is_valid_csv(file_path: str) -> bool: Check if the selected CSV file is valid
        create_overlay(message: str) -> tk.Label: Create a semi-transparent overlay with a message in the center
        get_account_path() -> None: Open csv file and store path
        export() -> None: Check if both csv files are selected, analyze data, and export html file
        on_enter(event: tk.Event) -> None: Change button border when mouse hovers over it
        on_leave(event: tk.Event) -> None: Change button border back to normal when mouse leaves
    """
    def __init__(self, os, version):
        if os == 'windows':
            theme = {
                "os": "windows",
                "acc_btn_active_bg": "green",
                "acc_btn_active_fg": "white",
                "acc_btn_disabled_bg": "grey",
                "acc_btn_disabled_fg": "black",
                "expo_btn_active_bg": "blue",
                "expo_btn_active_fg": "white",
                "expo_btn_disabled_bg": "red",
                "expo_btn_disabled_fg": "white",
                "title_font": ('Arial', 14),
                "normal_font": ('Arial', 12),
                "small_font": ('Arial', 10)
            }
        elif os == 'unix':
            theme = {
                "os": "unix",
                "acc_btn_active_bg": "white",
                "acc_btn_active_fg": "black",
                "acc_btn_disabled_bg": "grey",
                "acc_btn_disabled_fg": "black",
                "expo_btn_active_bg": "white",
                "expo_btn_active_fg": "black",
                "expo_btn_disabled_bg": "grey",
                "expo_btn_disabled_fg": "black",
                "title_font": ('Arial', 16),
                "normal_font": ('Arial', 14),
                "small_font": ('Arial', 12)
            }
        else:
            raise ValueError("Invalid operating system")

        self.version = version
        self.theme = theme

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
        if self.theme["os"] == "windows":
            self.container_frame.config(padx=20, pady=20)
        
        # Create a frame to hold the update inidicator
        latest = get_latest()
        if self.version != latest and latest is not None:
            self.update_frame = tk.Frame(self.container_frame)
            self.update_frame.pack(fill=tk.BOTH, expand=True)
            if self.theme["os"] == "unix":
                spacer = tk.Frame(self.update_frame, height=20)
                spacer.pack()
            self.update_button = tk.Button(self.update_frame, text="Update Available", command=self.hide_update_frame)
            self.update_button.configure(bg=self.theme['expo_btn_active_bg'], fg=self.theme['expo_btn_active_fg'], font=self.theme['normal_font'], width=30)
            self.update_button.pack()


        # Create a horizontal frame for radio buttons
        self.radio_button_frame = tk.Frame(self.container_frame)
        self.radio_button_frame.pack(expand=True)

        # Create a vertical frame for the file buttons
        self.file_button_frame = tk.Frame(self.container_frame)
        self.file_button_frame.pack(fill=tk.BOTH, expand=True)  

        # Create a frame for the version label
        self.version_frame = tk.Frame(self.container_frame)
        self.version_frame.pack(fill=tk.BOTH, expand=True)
        if self.theme["os"] == "unix":
            self.version_frame.config(padx=10, pady=10)
        
        # Initialize values
        self.radio_var = tk.IntVar()
        self.radio_var.set(4)
        self.account_history_path = ""

        # Create and label radio buttons
        report_title_label = tk.Label(self.radio_button_frame, text="Time Frame of Report")
        report_title_label.pack(side=tk.TOP, anchor=tk.N)
        report_title_label.config(font=self.theme["title_font"])

        tk.Radiobutton(self.radio_button_frame, text="Daily", variable=self.radio_var, value=1, font=self.theme['normal_font']).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Monthly", variable=self.radio_var, value=2, font=self.theme['normal_font']).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Quarterly", variable=self.radio_var, value=3, font=self.theme['normal_font']).pack(side=tk.LEFT, anchor=tk.N)
        tk.Radiobutton(self.radio_button_frame, text="Yearly", variable=self.radio_var, value=4, font=self.theme['normal_font']).pack(side=tk.LEFT, anchor=tk.N)

        # Account History button
        self.acc_button = tk.Button(self.file_button_frame, text="Select Account History CSV", command=self.get_account_path)
        self.acc_button.configure(bg=self.theme['acc_btn_disabled_bg'], fg=self.theme['acc_btn_disabled_fg'], font=self.theme['normal_font'], width=30)
        self.acc_button.pack(pady=2)

        # Export HTML button
        self.export_button = tk.Button(self.file_button_frame, text="Export HTML", command=self.export)
        self.export_button.configure(bg=self.theme['expo_btn_disabled_bg'], disabledforeground=self.theme['expo_btn_disabled_fg'], font=self.theme['normal_font'], width=30, state=tk.DISABLED)
        self.export_button.pack(pady=2)

        # Bind enter and leave events to change button borders
        self.acc_button.bind("<Enter>", self.on_enter)
        self.acc_button.bind("<Leave>", self.on_leave)

        self.export_button.bind("<Enter>", self.on_enter)
        self.export_button.bind("<Leave>", self.on_leave)

        # Create version label
        version_label = tk.Label(self.version_frame, text=f"Version {self.version}", font=self.theme['small_font'])
        version_label.pack(side=tk.RIGHT, anchor=tk.S)

        self.root.mainloop()
    
    def hide_update_frame(self) -> None:
        """Hide the update frame"""
        self.update_frame.destroy()
    
    def is_valid_csv(self, file_path) -> bool:
        """Check if the selected CSV file is valid"""
        try:
            csv_file = pd.read_csv(file_path, sep=',')
            for column in csv_file.columns:
                if column not in ['Time', 'Balance Before', 'Balance After', 'P&L', 'Action']:
                    return False
            return True
        except:
            return False
        
    def create_overlay(self, message: str) -> tk.Label:
        """Create a semi-transparent overlay with a message in the center"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        image = Image.new('RGBA', (width, height), (128, 128, 128, 128))  # Semi-transparent grey

        # Create a PhotoImage from the image
        photo = ImageTk.PhotoImage(image)

        # Create the overlay and set the image as its background
        overlay = tk.Label(self.root, image=photo)
        overlay.image = photo  # Keep a reference to the image
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        label = tk.Label(overlay, text=message, font=self.theme['title_font'], bg="grey")  # TODO Fix weird label background
        label.place(relx=0.5, rely=0.5, anchor='c')

        self.root.update()
        time.sleep(1)

        return overlay
    
    def get_account_path(self) -> None:
        """Open csv file and store path"""
        self.account_history_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.account_history_path:
            return
        
        if self.is_valid_csv(self.account_history_path):
            self.acc_button.configure(bg=self.theme['acc_btn_active_bg'], fg=self.theme['acc_btn_active_fg'])
            self.export_button.configure(bg=self.theme['expo_btn_active_bg'], fg=self.theme['expo_btn_active_fg'])
            self.export_button.configure(state=tk.NORMAL)
        else:
            tk.messagebox.showerror("Error", f"Please select a valid 'Account History' file.")
            self.account_history_path = ""
            self.export_button.configure(bg=self.theme['expo_btn_disabled_bg'], disabledforeground=self.theme['expo_btn_disabled_fg'])
            self.export_button.configure(state=tk.DISABLED)

    def export(self) -> None:
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
                if sys.platform == 'darwin':  # Mac
                    subprocess.call(('open', export_location))
                elif sys.platform == 'linux':  # Linux
                    subprocess.call(('xdg-open', export_location))
                else:
                    webbrowser.open(export_location)
        except:
            tk.messagebox.showerror("Error", "An error occurred while exporting the HTML file.")
            overlay.destroy()
            return

        overlay.destroy()

    def on_enter(self, event: tk.Event) -> None:
        """Change button border when mouse hovers over it"""
        event.widget.original_borderwidth = event.widget.cget("borderwidth")
        event.widget.config(borderwidth=3)

    def on_leave(self, event: tk.Event) -> None:
        """Change button border back to normal when mouse leaves"""
        event.widget.config(borderwidth=event.widget.original_borderwidth)
