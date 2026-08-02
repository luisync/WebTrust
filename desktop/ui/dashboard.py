import customtkinter as ctk
import desktop.api.client as client
import datetime
from desktop.scanner.scan import security_scan

# Define the in-app visuals.
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Define the dashboard's name and dimensions.
        self.title("WebTrust Desktop")
        self.geometry("900x600")

        # Main app frame.
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Load the other frames on the app.
        self.create_header()
        self.create_statistics()
        self.create_controls()
        self.create_activity()

        # Refresh the dashboard.
        self.refresh_dashboard()

        # Scan for security posture changes.
        self.scan()

    # Define the visuals for the header frame in the app.
    def create_header(self):
        # Set title.
        title = ctk.CTkLabel(
            self.main_frame,
            text="WebTrust",
            font=("Arial", 28, "bold")
        )
        title.pack()

        # Set subtitle.
        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Digital security helper."
        )
        subtitle.pack(pady=(0, 25))

    # Define the visuals for the statistics frame in the app.
    def create_statistics(self):
        frame = ctk.CTkFrame(self.main_frame)

        frame.pack(fill="x", pady=10)

        # Create a section that displays the time of the latest scan. 
        self.last_scan_label = ctk.CTkLabel(
            frame,
            text="Last Scan\nNever",
            justify="left"
        )

        # Create a section that displays the status of the back-end.
        self.backend_label = ctk.CTkLabel(
            frame,
            text="Backend\nLoading...",
            justify="left"
        )

        # Create a section that displays the amount of companies in the database.
        self.companies_label = ctk.CTkLabel(
            frame,
            text="Companies\nLoading...",
            justify="left"
        )

        # Define the position of each element.
        self.last_scan_label.pack(side="left", padx=40, pady=20)
        self.backend_label.pack(side="left", padx=40)
        self.companies_label.pack(side="left", padx=40)

    # Define the visuals for the controls frame in the app.
    def create_controls(self):
        frame = ctk.CTkFrame(self.main_frame)

        frame.pack(fill="x", pady=20)

        # A button allowing the user to commence the next security scan.
        button = ctk.CTkButton(
            frame,
            text="Scan All",
            command=self.scan
        )
        button.pack(side="left", padx=20, pady=20)

        # A button allowing the user to refresh the dashboard, ensuring data is updated.
        refresh = ctk.CTkButton(
            frame,
            text="Refresh",
            command=self.refresh_dashboard
        )
        refresh.pack(side="left")

    # Define the visuals for the activity frame in the app.
    def create_activity(self):
        frame = ctk.CTkFrame(self.main_frame)

        frame.pack(fill="both", expand=True)

        # Set the label indicating to the user that below is the latest activity.
        title = ctk.CTkLabel(
            frame,
            text="Recent Activity",
            font=("Arial", 18, "bold")
        )
        title.pack(anchor="w", padx=20, pady=20)

        # Offer comments on the scans.
        self.activity = ctk.CTkTextbox(
            frame,
            height=300
        )
        self.activity.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        self.activity.insert(
            "1.0",
            "No scans have been run yet."
        )

    # Refresh the dashboard's data.
    def refresh_dashboard(self):
        # Check the api's health.
        backend = client.health()
        
        # Update the dashborad's status label.
        self.backend_label.configure(
            text=f"Backend\n{backend['status']}"
        )

        # Check the database for companies.
        companies = client.get_companies()

        # Update the dashboard's companies label.
        self.companies_label.configure(
            text=f"Companies\n{len(companies)}"
        )

    # Scans the security posture of the companies in the database.
    def scan(self):
        # Check the domain's security posture.
        results = security_scan()

        # No companies in the database.
        if not results:
            self.activity.insert(
                "end",
                "No companies found.\n"
            )
            return

        # Replace the old text.
        self.activity.delete("1.0", "end")
        for result in results:
            self.activity.insert(
                "end",
                f"[{datetime.datetime.now().__format__('%x %X')}]: {result.details}\n"
            )

        # Update last scan label.
        self.last_scan_label.configure(
            text=f"Last Scan\n{datetime.datetime.now().__format__('%x %X')}"
        )