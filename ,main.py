from fastapi import FastAPI, HTTPException
import subprocess
import uuid
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the multi-downloader API! Use /download?url=YOUR_VIDEO_URL"}

@app.get("/download")
async def download_video(url: str):
    """
    Universal endpoint to download a video from YouTube, TikTok, Instagram Reels, etc.
    using yt-dlp.
    """
    # Generate a unique filename to avoid collisions
    filename_pattern = f"downloaded_video_{uuid.uuid4()}.%(ext)s"

    try:
        # 1. Run yt-dlp via subprocess to download the video.
        # 2. Capture stdout and stderr for proper error handling.
        cmd = [
            "yt-dlp",
            "-o",
            filename_pattern,  # output filename pattern
            url
        ]
        process_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # If yt-dlp returns a non-zero exit code, something went wrong
        if process_result.returncode != 0:
            error_msg = process_result.stderr.strip()
            raise HTTPException(
                status_code=400,
                detail=f"Error: Could not download video.\nDetails:\n{error_msg}"
            )

        # Successfully downloaded
        return {
            "message": "Video downloaded successfully!",
            "filename_pattern": filename_pattern
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An unexpected error occurred: {str(e)}"
        )
