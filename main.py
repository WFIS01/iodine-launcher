import tkinter as tk
from tkinter import ttk  # Import ttk for Progressbar
from tkinter import PhotoImage, filedialog, messagebox, Toplevel
import os
import subprocess
import time

# Constants for image paths
ICON_DIR = "icons"  # Assuming icons are inside the "icons" folder
LOGO_PATH = os.path.join(ICON_DIR, "minecraft_logo.png")
SKIN_DIRECTORY = "/lib/minecraft-pi-reborn-client/game/data/images/mob"  # Path to save the skin

def clear_frame(frame):
    """
    Clears all widgets from the given frame.
    """
    for widget in frame.winfo_children():
        widget.destroy()


def show_home():
    """
    Show the Home screen with the Minecraft Pi launcher elements.
    """
    clear_frame(main_frame)  # Clear the current screen's widgets

    home_label = tk.Label(main_frame, text="Iodine Launcher", font=("Arial", 20), fg="#ffffff", bg="#1d1d1d")
    home_label.pack(pady=20)

    logo_image = PhotoImage(file=LOGO_PATH)  # Use the provided Minecraft logo
    logo_label = tk.Label(main_frame, image=logo_image, bg="#1d1d1d")
    logo_label.image = logo_image  # Keep a reference
    logo_label.pack(pady=10)

    button_frame = tk.Frame(main_frame, bg="#1d1d1d")
    button_frame.pack(pady=40)

    play_button = tk.Button(button_frame, text="Play", font=("Arial", 18), command=play_minecraft, width=20, height=2, bg="#4caf50", fg="#ffffff", relief="flat", bd=0)
    play_button.pack(pady=20)

    edit_skin_button = tk.Button(button_frame, text="Edit Skin", font=("Arial", 14), command=edit_skin, width=20, height=2, bg="#ff9800", fg="#ffffff", relief="flat", bd=0)
    edit_skin_button.pack(pady=10)

    footer_frame = tk.Frame(main_frame, bg="#1d1d1d")
    footer_frame.pack(fill="x", pady=10)

    footer_label = tk.Label(footer_frame, text="Powered by Minecraft Pi Launcher", font=("Arial", 10), fg="#ffffff", bg="#1d1d1d")
    footer_label.pack()


def show_servers():
    """
    Show the Servers screen with a custom message.
    """
    clear_frame(main_frame)  # Clear the current screen's widgets

    servers_message = tk.Label(main_frame, text="Check Iodine's GitHub wiki, to get your server added!", font=("Arial", 14), fg="#ffffff", bg="#1d1d1d")
    servers_message.pack(pady=20)


def show_settings():
    """
    Show the Settings screen with Update and Changelog buttons.
    """
    clear_frame(main_frame)  # Clear the current screen's widgets

    update_button = tk.Button(main_frame, text="Update", font=("Arial", 14), command=update_launcher, width=20, height=2, bg="#ff9800", fg="#ffffff", relief="flat", bd=0)
    update_button.pack(pady=20)

    changelog_button = tk.Button(main_frame, text="Changelog", font=("Arial", 14), command=show_changelog, width=20, height=2, bg="#ff9800", fg="#ffffff", relief="flat", bd=0)
    changelog_button.pack(pady=20)


def show_changelog():
    """
    Show a changelog window with details about the release.
    """
    changelog_window = Toplevel(window)
    changelog_window.title("Changelog - Iodine v0.1.1")
    changelog_window.geometry("400x200")
    changelog_window.config(bg="#1d1d1d")

    changelog_text = tk.Label(changelog_window, text="Iodine v0.1.1 released", font=("Arial", 14), fg="#ffffff", bg="#1d1d1d")
    changelog_text.pack(pady=50)


def edit_skin():
    """
    Opens the file manager to select a PNG file and updates the character skin.
    """
    file_path = filedialog.askopenfilename(
        title="Select Skin",
        filetypes=[("PNG Files", "*.png")]
    )

    if not file_path:
        return  # If no file was selected, return

    # Check if the selected file is a PNG
    if not file_path.lower().endswith(".png"):
        messagebox.showerror("Invalid File", "Please select a PNG file.")
        return

    # Define the path for the new skin and the old skin
    new_skin_path = os.path.join(SKIN_DIRECTORY, "char.png")
    old_skin_path = os.path.join(SKIN_DIRECTORY, "char.png")

    try:
        # Resize the selected image to 64x32
        resized_image_path = "/tmp/resized_skin.png"
        if not resize_image(file_path, resized_image_path):
            return
        
        # Remove the old char.png if it exists
        if os.path.exists(old_skin_path):
            os.remove(old_skin_path)

        # Rename the resized PNG file to char.png and move it to the skin directory
        os.rename(resized_image_path, new_skin_path)

        # Notify the user
        messagebox.showinfo("Success", "Skin updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def resize_image(input_path, output_path, size=(64, 32)):
    """
    Resizes the image to the specified size (default 64x32) and saves it to the output path.
    """
    try:
        from PIL import Image  # Pillow library for image processing
        img = Image.open(input_path)
        img = img.resize(size, Image.ANTIALIAS)
        img.save(output_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while resizing the image: {e}")
        return False
    return True


def play_minecraft():
    """
    Launch Minecraft Pi or any related game with a progress bar.
    """
    progress_window = Toplevel(window)
    progress_window.title("Installing / Launching Minecraft Pi")
    progress_window.geometry("400x200")
    progress_window.config(bg="#1d1d1d")

    progress_label = tk.Label(progress_window, text="Checking for MCPI++ installation...", font=("Arial", 12), fg="#ffffff", bg="#1d1d1d")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')  # Infinite progress bar
    progress_bar.pack(pady=10)
    progress_bar.start()  # Start the infinite scroll

    def check_and_launch():
        try:
            # Check if MCPI++ is installed
            result = subprocess.run("which minecraft-pi-reborn-client", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:  # Not installed
                # Install MCPI++
                subprocess.run("wget https://raw.githubusercontent.com/NoozSBC/mcpi-reborn-extended/main/install.sh && bash install.sh", shell=True, check=True)
                messagebox.showinfo("Installation", "MCPI++ installed successfully!")
            else:
                # Update if MCPI++ is installed
                subprocess.run("sudo apt update && sudo apt-get upgrade -y", shell=True, check=True)
                messagebox.showinfo("Update", "Minecraft Pi Reborn updated successfully!")

            # Launch Minecraft Pi Reborn
            subprocess.run("minecraft-pi-reborn-client", shell=True, check=True)

            # Close all windows after launch
            window.quit()  # Close the main window
            progress_window.quit()  # Close the progress window

            # Properly terminate the app after closing windows
            progress_window.destroy()
            window.destroy()

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            progress_window.quit()

    # Run the check and installation in a separate thread
    progress_window.after(500, check_and_launch)


def update_launcher():
    """
    Check for launcher updates or other logic (future functionality).
    """
    messagebox.showinfo("Update", "No new updates available for Iodine!")


def create_launcher():
    """
    Creates the Iodine Minecraft Pi launcher GUI with tkinter.
    """
    global window
    window = tk.Tk()
    window.title("Iodine Launcher v0.1.1")
    window.geometry("500x600")
    window.config(bg="#1d1d1d")

    # Set window icon
    window.iconphoto(True, PhotoImage(file=LOGO_PATH))

    # Create the top navigation bar with buttons (Servers, Home, Settings)
    top_bar = tk.Frame(window, bg="#333", height=50)
    top_bar.pack(fill="x", side="top")

    servers_button = tk.Button(top_bar, text="Servers", font=("Arial", 12), command=show_servers, width=10, height=2, relief="flat", bg="#4caf50", fg="white")
    servers_button.pack(side="left", padx=5, expand=True)

    home_button = tk.Button(top_bar, text="Home", font=("Arial", 12), command=show_home, width=10, height=2, relief="flat", bg="#4caf50", fg="white")
    home_button.pack(side="left", padx=5, expand=True)

    settings_button = tk.Button(top_bar, text="Settings", font=("Arial", 12), command=show_settings, width=10, height=2, relief="flat", bg="#4caf50", fg="white")
    settings_button.pack(side="left", padx=5, expand=True)

    # Create the main frame to display content
    global main_frame
    main_frame = tk.Frame(window, bg="#1d1d1d")
    main_frame.pack(fill="both", expand=True)

    # Show the Home screen by default
    show_home()

    window.mainloop()


if __name__ == "__main__":
    create_launcher()
