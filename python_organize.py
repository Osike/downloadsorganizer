import os
import shutil
import schedule
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/organize_desktop.log')),
        logging.StreamHandler()
    ]
)

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

def organize_files():
    """Main function to organize files"""
    try:
        logging.info("Starting file organization...")
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
        
        logging.info("Files have been organized!")
    except Exception as e:
        logging.error(f"Error organizing files: {str(e)}")

def start_scheduler():
    """Start the scheduler to run organize_files every 14 hours"""
    schedule.every(14).hours.do(organize_files)
    logging.info("Scheduler started. Files will be organized every 14 hours.")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute if a task needs to run

if __name__ == "__main__":
    # Run once immediately on startup
    organize_files()
    
    # Start the scheduler
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
