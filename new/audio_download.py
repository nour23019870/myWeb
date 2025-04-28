import subprocess
import os
from pathlib import Path
from time import sleep
import sys
import json

# Modern hacker-style header
def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    banner = r'''
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░      
░▒▓█▓▒░   ░▒▓████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░  ░▒▓█▓▒░          
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          
░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          
                                                                 
                Welc0m T0 🄻①🄶🄷🅃 🄼🅄🅂①🄲                                
'''
    print(banner)

# Progress bar with percentage
def animate_bar(task, total):
    bar = ""
    for i in range(1, 51):
        percent = int((i / 50) * 100)
        sys.stdout.write(f"\r🎵 {task}... [{bar:<50}] {percent}%")
        sys.stdout.flush()
        bar += "▌"
        sleep(0.02)
    print("\n")

# Get playlist entries using yt-dlp JSON
def get_playlist_entries(url):
    result = subprocess.run([
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        url
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    entries = [json.loads(line) for line in result.stdout.strip().split("\n") if line.strip()]
    return entries

def download_audio(url):
    print("\n⬇️  Downloading and converting to MP3...\n")

    music_dir = str(Path.home() / "Music")
    os.makedirs(music_dir, exist_ok=True)

    entries = get_playlist_entries(url)
    total = len(entries) if entries else 1

    for i, entry in enumerate(entries if entries else [None], 1):
        label = f"Track {i}/{total}"
        animate_bar(label, total)

        cmd_url = f"https://www.youtube.com/watch?v={entry['id']}" if entry else url

        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", os.path.join(music_dir, "%(title)s.%(ext)s"),
            cmd_url
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\n✅ All downloads complete! Saved in ~/Music\n")

if __name__ == "__main__":
    print_banner()
    url = input("📎 Paste YouTube URL here: ").strip()
    if url:
        download_audio(url)
    else:
        print("❌ No URL provided. Exiting...")