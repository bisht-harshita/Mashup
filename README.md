# YouTube Mashup Generator

A modern Streamlit web application that generates a mashup from YouTube videos of your favorite singer and delivers it directly via email.

This project was developed as part of the Mashup Assignment, which includes:

- Command Line Mashup Program  
- Web App Mashup Generator  
- Email delivery of generated mashup  
- Secure credential handling  

---

## Features

- Download N YouTube videos of a singer  
- Extract and trim first Y seconds from each video  
- Merge all trimmed audios into one mashup  
- Compress output into ZIP file  
- Automatically send mashup to user email  
- Secure credentials using Streamlit Secrets  
- Automatic cleanup of temporary files  

---

## Tech Stack

- Python  
- Streamlit  
- yt-dlp  
- FFmpeg  
- SMTP (Gmail App Password)  

---

## How It Works

User enters:

- Singer Name  
- Number of Videos (>10)  
- Duration per Video (>20 seconds)  
- Valid Email Address  

Application:

- Searches and downloads videos using yt-dlp  
- Extracts and trims audio using FFmpeg  
- Merges all trimmed audio clips  
- Creates mashup.zip  
- Sends ZIP file to user email  # Mashup
