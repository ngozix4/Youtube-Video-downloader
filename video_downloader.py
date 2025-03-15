import streamlit as st
import yt_dlp
import os
import shutil

def download_media(url, save_path, format_type, ffmpeg_installed):
    """Downloads media from YouTube Music with progress tracking."""
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'noplaylist': False  # Allow playlist downloads
    }

    if ffmpeg_installed and format_type == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            # Handle playlists/albums
            if 'entries' in info_dict:
                tracks = info_dict['entries']
                st.write(f"Found playlist with {len(tracks)} tracks.")
                main_progress = st.progress(0)

                for i, track in enumerate(tracks):
                    track_url = track['webpage_url']
                    st.write(f"Downloading track {i + 1}/{len(tracks)}: {track.get('title', 'Unknown Title')}")

                    track_opts = ydl_opts.copy()
                    track_opts['outtmpl'] = os.path.join(save_path, f"{track['title']}.%(ext)s")

                    # Progress bar for each track
                    track_progress = st.progress(0)

                    with yt_dlp.YoutubeDL(track_opts) as ydl_individual:
                        ydl_individual.download([track_url])

                    track_progress.progress(100)
                    main_progress.progress((i + 1) / len(tracks))

                st.success("Playlist/album download completed successfully!")
            else:
                ydl.download([url])
                st.success("Download completed successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit App
st.title("YouTube Music Downloader")

# Input URL
url = st.text_input("Enter YouTube Music URL", "")

# Custom save folder path
save_path = st.text_input("Enter the folder path to save downloads", "C:\\Users\\HP\\Desktop\\Music\\Liked_Music(2)")
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Check if ffmpeg is installed
ffmpeg_installed = shutil.which("ffmpeg") is not None
if not ffmpeg_installed:
    st.warning("FFmpeg is not installed. Downloads will be saved in the default available format.")

# Download buttons
if st.button("Download as MP3"):
    if url:
        st.write("Starting MP3 download...")
        download_media(url, save_path, 'mp3', ffmpeg_installed)
    else:
        st.warning("Please enter a valid YouTube Music URL.")

if st.button("Download as MP4"):
    if url:
        st.write("Starting MP4 download...")
        download_media(url, save_path, 'mp4', ffmpeg_installed)
    else:
        st.warning("Please enter a valid YouTube Music URL.")
