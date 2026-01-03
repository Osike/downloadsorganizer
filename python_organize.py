import os
import shutil

# Define the path to your Downloads folder
downloads_folder = os.path.expanduser('~/Downloads')

# Define the folders you want to create
folders = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.mkv', '.mov'],
    'Music': ['.mp3', '.wav'],
    'Others': []
}

# Create folders if they don't exist
for folder in folders.keys():
    folder_path = os.path.join(downloads_folder, folder)
    os.makedirs(folder_path, exist_ok=True)

# Move files into the appropriate folders
for filename in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, filename)

    if os.path.isfile(file_path):
        moved = False
        for folder, extensions in folders.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(downloads_folder, folder, filename))
                moved = True
                break
        
        # Move to 'Others' if no extension matched
        if not moved:
            shutil.move(file_path, os.path.join(downloads_folder, 'Others', filename))

print("Files have been organized!")
