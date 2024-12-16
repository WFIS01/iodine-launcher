#!/bin/bash

# Print "Iodine Automatic Installer v0.1.1" in cyan
echo -e "\033[0;36mIodine Automatic Installer v0.1.1\033[0m"

# Define variables
REPO_URL="https://github.com/WFIS01/iodine-launcher/archive/refs/heads/main.zip"
DOWNLOAD_DIR="$HOME"
FOLDER_NAME="iodine-launcher"
ZIP_FILE="iodine-launcher.zip"
DESKTOP_ENTRY="$HOME/Desktop/Iodine-Launcher.desktop"
ICON_PATH="$DOWNLOAD_DIR/$FOLDER_NAME/iodine-launcher-main/icons/minecraft.png"
START_MENU_ENTRY="$HOME/.local/share/applications/iodine-launcher.desktop"

# Download the zip file from the GitHub repository
echo "Downloading the iodine-launcher repository from GitHub..."
wget -O "$DOWNLOAD_DIR/$ZIP_FILE" "$REPO_URL"

# Create the iodine-launcher folder in the home directory
echo "Creating the iodine-launcher directory..."
mkdir -p "$DOWNLOAD_DIR/$FOLDER_NAME"

# Extract the downloaded zip file into the iodine-launcher folder
echo "Extracting the zip file..."
unzip "$DOWNLOAD_DIR/$ZIP_FILE" -d "$DOWNLOAD_DIR/$FOLDER_NAME"

# Delete the zip file after extraction
echo "Deleting the zip file..."
rm "$DOWNLOAD_DIR/$ZIP_FILE"

# Change to the iodine-launcher directory
cd "$DOWNLOAD_DIR/$FOLDER_NAME/iodine-launcher-main"  # Ensure this matches the extracted folder's structure

# Run the Python script to launch the Iodine launcher
echo "Running the Iodine Launcher..."
python3 main.py

# Add a desktop shortcut for the Iodine Launcher
echo "Creating a desktop shortcut for Iodine Launcher..."

# Create the .desktop file on the Desktop
echo "[Desktop Entry]
Name=Iodine Launcher
Comment=Launch Minecraft Pi Reborn Client
Exec=python3 $DOWNLOAD_DIR/$FOLDER_NAME/iodine-launcher-main/main.py
Icon=$ICON_PATH
Terminal=false
StartupWMClass=Iodine-Launcher
Type=Application
Categories=Games;Utility;
StartupNotify=true" > "$DESKTOP_ENTRY"

# Make the shortcut executable
chmod +x "$DESKTOP_ENTRY"

# Notify the user that the shortcut has been created
echo "Iodine Launcher shortcut created on your Desktop!"

# Add the Iodine Launcher to the Raspberry Pi Start Menu under Games
echo "Adding Iodine Launcher to the Start Menu under Games..."

# Create a .desktop entry in the Start Menu (applications folder)
mkdir -p "$HOME/.local/share/applications"  # Ensure the directory exists
echo "[Desktop Entry]
Name=Iodine Launcher
Comment=Launch Minecraft Pi Reborn Client
Exec=python3 $DOWNLOAD_DIR/$FOLDER_NAME/iodine-launcher-main/main.py
Icon=$ICON_PATH
Terminal=false
StartupWMClass=Iodine-Launcher
Type=Application
Categories=Games;Utility;
StartupNotify=true" > "$START_MENU_ENTRY"

# Make the Start Menu entry executable
chmod +x "$START_MENU_ENTRY"

# Notify the user that the Start Menu entry has been added
echo "Iodine Launcher has been added to the Start Menu under Games."

