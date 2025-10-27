import customtkinter as ctk 
from tkinter import filedialog
import threading
import os
import sys


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x500")
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.url_var = ctk.StringVar()
        self.format_var = ctk.StringVar(value="mp4")
        self.download_path = ctk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="YouTube to MP3/MP4 Downloader", 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # URL Entry Frame
        url_frame = ctk.CTkFrame(self.root)
        url_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(url_frame, text="YouTube URL:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20, pady=(15, 5))
        self.url_entry = ctk.CTkEntry(url_frame, textvariable=self.url_var, height=35)
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Format Selection Frame
        format_frame = ctk.CTkFrame(self.root)
        format_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(format_frame, text="Download Format:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20, pady=(15, 10))
        
        format_options = ctk.CTkFrame(format_frame, fg_color="transparent")
        format_options.pack(fill="x", padx=20, pady=(0, 15))
        
        mp4_radio = ctk.CTkRadioButton(format_options, text="MP4 (Video)", variable=self.format_var, 
                                       value="mp4", font=ctk.CTkFont(size=12))
        mp4_radio.pack(side="left", padx=20)
        
        mp3_radio = ctk.CTkRadioButton(format_options, text="MP3 (Audio Only)", variable=self.format_var, 
                                       value="mp3", font=ctk.CTkFont(size=12))
        mp3_radio.pack(side="left", padx=20)
        
        # Download Path Frame
        path_frame = ctk.CTkFrame(self.root)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(path_frame, text="Download Location:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20, pady=(15, 5))
        
        path_inner_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.path_entry = ctk.CTkEntry(path_inner_frame, textvariable=self.download_path, 
                                       height=35, state="readonly")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(path_inner_frame, text="Browse", command=self.browse_folder,
                                    width=100, height=35)
        browse_btn.pack(side="left")
        
        # Download Button
        self.download_btn = ctk.CTkButton(self.root, text="Download", command=self.start_download,
                                          font=ctk.CTkFont(size=14, weight="bold"),
                                          height=40, fg_color="#4CAF50", hover_color="#45a049")
        self.download_btn.pack(pady=20, padx=20, fill="x")
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.root)
        self.progress.set(0)
        self.progress.pack(pady=10, padx=20, fill="x")
        
        # Status Label
        self.status_label = ctk.CTkLabel(self.root, text="Ready to download", 
                                         font=ctk.CTkFont(size=11))
        self.status_label.pack(pady=5)
        
        # Percentage Label
        self.percentage_label = ctk.CTkLabel(self.root, text="", 
                                             font=ctk.CTkFont(size=12, weight="bold"))
        self.percentage_label.pack(pady=5)
        
    def browse_folder(self):
        if self.is_downloading:
            return
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            
    def start_download(self):
        if self.is_downloading:
            return
            
        url = self.url_var.get().strip()
        
        if not url:
            self.show_error("Please enter a YouTube URL")
            return
            
        # Validate YouTube URL
        if "youtube.com" not in url and "youtu.be" not in url:
            self.show_error("Please enter a valid YouTube URL")
            return
            
        # Start download in separate thread
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="Downloading...")
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()
        
    def show_error(self, message):
        self.status_label.configure(text=message, text_color="red")
        self.percentage_label.configure(text="")
    
    def show_success(self, message):
        self.status_label.configure(text=message, text_color="green")
        self.percentage_label.configure(text="✓ Completed", text_color="green")
        
    def download_video(self):
        try:
            import yt_dlp
            
            url = self.url_var.get().strip()
            format_type = self.format_var.get()
            output_path = self.download_path.get()
            
            # Configure yt-dlp options with progress hook
            def download_hook(d):
                if d['status'] == 'downloading':
                    # Get progress percentage
                    if 'total_bytes' in d or 'total_bytes_estimate' in d:
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        downloaded = d.get('downloaded_bytes', 0)
                        if total > 0:
                            percent = (downloaded / total) * 100
                            self.root.after(0, lambda p=percent: self.progress.set(p / 100))
                            self.root.after(0, lambda p=int(percent): self.percentage_label.configure(
                                text=f"{p}%", text_color="blue"))
                elif d['status'] == 'finished':
                    self.root.after(0, lambda: self.progress.set(100))
                    self.root.after(0, lambda: self.percentage_label.configure(text="Processing...", text_color="blue"))
            
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [download_hook],
                'quiet': False,
                'no_warnings': True,
            }
            
            if format_type == "mp3":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = 'best[ext=mp4]/best'
            
            self.root.after(0, lambda: self.status_label.configure(text="Starting download...", text_color="blue"))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Video')
                
                self.root.after(0, lambda t=title: self.status_label.configure(
                    text=f"Downloading: {t[:50]}...", text_color="blue"))
                
                # Download the video
                ydl.download([url])
            
            # Success message
            self.root.after(0, lambda: self.show_success("Download completed successfully!"))
            self.root.after(0, lambda: self.download_btn.configure(state="normal", text="Download"))
            self.is_downloading = False
            
        except ImportError:
            self.root.after(0, lambda: self.progress.set(0))
            self.root.after(0, lambda: self.show_error("yt-dlp not installed. Run: pip install yt-dlp"))
            self.root.after(0, lambda: self.percentage_label.configure(text="✗ Failed", text_color="red"))
            self.root.after(0, lambda: self.download_btn.configure(state="normal", text="Download"))
            self.is_downloading = False
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.progress.set(0))
            self.root.after(0, lambda: self.show_error(f"Download failed: {error_msg[:60]}"))
            self.root.after(0, lambda: self.percentage_label.configure(text="✗ Failed", text_color="red"))
            self.root.after(0, lambda: self.download_btn.configure(state="normal", text="Download"))
            self.is_downloading = False
            
            # Special handling for common errors
            if "ffmpeg" in error_msg.lower() or "ffprobe" in error_msg.lower():
                self.root.after(0, lambda: self.status_label.configure(
                    text="FFmpeg not installed or not in PATH", text_color="red"))


def main():
    root = ctk.CTk()
    app = YouTubeDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()

