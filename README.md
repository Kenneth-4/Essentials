# YouTube Downloader - MP3/MP4 Converter

A modern GUI application to download YouTube videos as MP3 or MP4 files using Python and CustomTkinter.

## Features

- Modern, beautiful GUI using CustomTkinter with dark theme
- Real-time download progress with percentage
- Visual feedback for success (✓) and failure (✗)
- Download videos as MP3 (audio only) or MP4 (video)
- Choose custom download location
- Progress bar with live percentage display
- Cross-platform support (Windows, macOS, Linux)

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install FFmpeg (required for audio conversion):
   
   **Windows:**
   - Download from: https://www.gyan.dev/ffmpeg/builds/
   - Extract to a folder
   - Add to PATH or place ffmpeg.exe in the same directory
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux:**
   ```bash
   sudo apt-get install ffmpeg
   ```

## Usage

1. Run the application:
   ```bash
   python main-yt.py
   ```

2. Enter a YouTube URL
3. Select MP4 (video) or MP3 (audio only)
4. Choose download location (default: Downloads folder)
5. Click "Download"

## Dependencies

- `yt-dlp`: YouTube video downloader
- `customtkinter`: Modern GUI framework
- `ffmpeg`: Media converter (separate installation required)

## New Features in This Version

- **Progress Tracking**: Real-time download progress with percentage (0-100%)
- **Visual Feedback**: Clear indicators showing success (✓) or failure (✗)
- **Error Handling**: Detailed error messages for common issues
- **Modern UI**: CustomTkinter with dark theme for a sleek look
- **Button States**: Download button disabled during active downloads to prevent multiple downloads

## Notes

- FFmpeg is required for audio conversion
- Download speed depends on your internet connection
- Some videos may have download restrictions
- The percentage shows 0-100% during download, then "Processing..." during conversion, and finally "✓ Completed" when done

