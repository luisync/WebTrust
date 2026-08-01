import customtkinter as ctk
from ui.dashboard import Dashboard

# Load the app.
def start():
    # Define visuals.
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Materialise the visuals and start the main logic of the app.
    app = Dashboard()
    app.mainloop()