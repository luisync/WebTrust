import customtkinter as ctk

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
        last_scan = ctk.CTkLabel(
            frame,
            text="Last Scan\nNever",
            justify="left"
        )

        # Create a section that displays the status of the back-end.
        backend = ctk.CTkLabel(
            frame,
            text="Backend\nOnline",
            justify="left"
        )

        # Create a section that displays the amount of companies in the database.
        companies = ctk.CTkLabel(
            frame,
            text="Companies\n0",
            justify="left"
        )

        # Define the position of each element.
        last_scan.pack(side="left", padx=40, pady=20)
        backend.pack(side="left", padx=40)
        companies.pack(side="left", padx=40)

    # Define the visuals for the controls frame in the app.
    def create_controls(self):
        frame = ctk.CTkFrame(self.main_frame)

        frame.pack(fill="x", pady=20)

        # A button allowing the user to commence the next security scan.
        button = ctk.CTkButton(
            frame,
            text="Scan All"
        )
        button.pack(side="left", padx=20, pady=20)

        # A button allowing the user to refresh the database, ensuring data is updated.
        refresh = ctk.CTkButton(
            frame,
            text="Refresh"
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
        textbox = ctk.CTkTextbox(
            frame,
            height=300
        )
        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        textbox.insert(
            "1.0",
            "No scans have been run yet."
        )