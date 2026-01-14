# Desktop Organizer - Documentation

## Overview
The Desktop Organizer is a Python script that automatically organizes files in your Downloads folder every 14 hours.

## What It Does
- Scans your `~/Downloads` folder
- Moves files into categorized subfolders based on file type:
  - **Documents**: `.pdf`, `.docx`, `.doc`, `.txt`
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`
  - **Videos**: `.mp4`, `.mkv`, `.mov`
  - **Music**: `.mp3`, `.wav`
  - **Others**: Files that don't match any category

## How It Works

### Schedule
The script runs automatically every 14 hours using the `schedule` library:
```python
schedule.every(14).hours.do(organize_files)
```

### Timeline Example
- **Start time**: Script runs immediately
- **+14 hours**: First automatic run
- **+28 hours**: Second automatic run
- **+42 hours**: Third automatic run
- And continues every 14 hours...

### Main Components

#### 1. `organize_files()` Function
- Creates the category folders if they don't exist
- Iterates through all files in Downloads
- Moves each file to its appropriate folder
- Includes error handling and logging

#### 2. `start_scheduler()` Function
- Sets up the 14-hour schedule
- Runs a continuous loop checking every 60 seconds
- Executes the task when 14 hours have elapsed

#### 3. Logging System
All activity is logged to `~/organize_desktop.log`:
```
2026-01-14 12:00:00,123 - INFO - Starting file organization...
2026-01-14 12:00:05,456 - INFO - Files have been organized!
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install schedule
```

### 2. Run the Script

#### Option A: Background Process (Temporary)
```bash
nohup /var/www/html/demos/desktopOrgnizer/.venv/bin/python /var/www/html/demos/desktopOrgnizer/python_organize.py > organize.log 2>&1 &
```
- Runs in the background
- Continues even if terminal closes
- Stops when system restarts

#### Option B: Systemd Service (Permanent)
Setup to run automatically on system startup:
```bash
sudo cp /var/www/html/demos/desktopOrgnizer/desktop-organizer.service /etc/systemd/user/
sudo systemctl --user daemon-reload
sudo systemctl --user enable desktop-organizer.service
sudo systemctl --user start desktop-organizer.service
```

## How to Verify It's Working

### 1. Check if Process is Running
```bash
ps aux | grep python_organize.py
```
You should see your Python process listed.

### 2. View Real-Time Logs
```bash
tail -f organize.log
```
Shows live log entries as they happen.

### 3. Check Log File
```bash
cat organize.log
```
View the complete history of all runs.

### 4. Verify Folder Creation
```bash
ls -la ~/Downloads
```
Should show the organized folders: `Documents/`, `Images/`, `Videos/`, `Music/`, `Others/`

## Stopping the Script

### Kill Background Process
Find the process ID first:
```bash
ps aux | grep python_organize.py
```

Then kill it:
```bash
kill <PID>
```

### Disable Systemd Service
```bash
sudo systemctl --user stop desktop-organizer.service
sudo systemctl --user disable desktop-organizer.service
```

## Files Structure
```
/var/www/html/demos/desktopOrgnizer/
├── python_organize.py              # Main script with scheduler
├── desktop-organizer.service       # Systemd service file
├── README.md                        # Original documentation
└── DOCUMENTATION.md                # This file
```

## Troubleshooting

### Script Not Organizing Files
1. Check if process is still running: `ps aux | grep python_organize.py`
2. If not running, restart it using one of the options above
3. Check logs for errors: `tail organize.log`

### Permission Issues
Make sure the Downloads folder is accessible:
```bash
ls -la ~/Downloads
chmod 755 ~/Downloads
```

### High CPU Usage
The scheduler checks every 60 seconds but only runs the task every 14 hours, so CPU usage should be minimal. If high, the script may be stuck moving large files.

## Modified Code Details

The original script was a one-time execution. The updates include:

1. **Added imports**:
   - `schedule` - for task scheduling
   - `time` - for sleep between checks
   - `logging` - for tracking activity

2. **Added logging configuration**:
   - Logs to file: `~/organize_desktop.log`
   - Also prints to console

3. **Wrapped logic in `organize_files()` function**:
   - Can be called multiple times
   - Includes error handling

4. **Added `start_scheduler()` function**:
   - Sets up the 14-hour schedule
   - Runs infinite loop checking for pending tasks

5. **Added main execution logic**:
   - Runs once immediately on startup
   - Then enters scheduler loop

## Performance Notes
- The script checks for scheduled tasks every 60 seconds
- Each organization run typically takes a few seconds
- Memory usage is minimal (usually < 50MB)
- CPU usage is minimal except during file moving operations
