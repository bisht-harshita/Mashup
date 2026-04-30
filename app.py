import streamlit as st
import yt_dlp
import os
import zipfile
import smtplib
import re
import subprocess
from email.message import EmailMessage

st.set_page_config(
    page_title="YouTube Mashup Generator 🎵",
    page_icon="🎧",
    layout="centered"
)

SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #dddddd;
    margin-bottom: 30px;
}

section.main > div {
    background-color: rgba(255,255,255,0.05);
    padding: 40px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
}

.stButton>button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    border-radius: 10px;
    background-color: #ff4b4b;
    color: white;
    border: none;
}

.stButton>button:hover {
    background-color: #e63c3c;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎵 YouTube Mashup Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create a mashup from your favorite singer and receive it via email</div>', unsafe_allow_html=True)

singer = st.text_input("🎤 Singer Name")
num_videos = st.number_input("📹 Number of Videos (>10)", min_value=11, step=1)
duration = st.number_input("⏱ Duration per Video (seconds, >20)", min_value=21, step=1)
email = st.text_input("📧 Email Address")

generate = st.button("🚀 Generate Mashup")

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def download_videos(singer, num_videos):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True
    }

    search_query = f"ytsearch{num_videos}:{singer} songs"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

def create_mashup(duration, output_file):
    trimmed_files = []

    for file in os.listdir("downloads"):
        input_path = os.path.join("downloads", file)
        trimmed_path = f"downloads/trimmed_{file}.mp3"

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-t", str(duration),
            "-acodec", "mp3",
            trimmed_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        trimmed_files.append(trimmed_path)

    with open("file_list.txt", "w") as f:
        for file in trimmed_files:
            f.write(f"file '{file}'\n")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "file_list.txt",
        "-c", "copy",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def send_email(receiver, filename):
    msg = EmailMessage()
    msg["Subject"] = "🎵 Your Mashup is Ready!"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg.set_content("Your custom mashup is attached. Enjoy! 🎧")

    with open(filename, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename=filename
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

def cleanup():
    if os.path.exists("downloads"):
        for file in os.listdir("downloads"):
            os.remove(os.path.join("downloads", file))
        os.rmdir("downloads")

    for file in ["mashup.mp3", "mashup.zip", "file_list.txt"]:
        if os.path.exists(file):
            os.remove(file)

if generate:
    if not singer or not email:
        st.error("Please fill all fields.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email.")
    else:
        try:
            with st.spinner("📥 Downloading videos..."):
                download_videos(singer, num_videos)

            with st.spinner("🎧 Creating mashup..."):
                create_mashup(duration, "mashup.mp3")

            with zipfile.ZipFile("mashup.zip", 'w') as zipf:
                zipf.write("mashup.mp3")

            with st.spinner("📧 Sending email..."):
                send_email(email, "mashup.zip")

            st.success("🎉 Mashup sent successfully!")

            cleanup()

        except Exception as e:
            st.error(f"Error: {e}")
