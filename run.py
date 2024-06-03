import os
import argparse
from pytube import YouTube
from moviepy.editor import AudioFileClip
import whisper
import torch

def download_youtube_video_as_mp3(youtube_url, output_path):
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()
    output_file = video.download(output_path=output_path)

    # Convert to mp3
    base, ext = os.path.splitext(output_file)
    mp3_file = base + ".mp3"
    audio_clip = AudioFileClip(output_file)
    audio_clip.write_audiofile(mp3_file)
    audio_clip.close()

    # Optionally, remove the original file
    os.remove(output_file)

    return mp3_file, yt.title

def transcribe_audio(mp3_file, model_name="medium"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(mp3_file)
    return result["text"]

def process_url(youtube_url, output_path):
    mp3_file, video_title = download_youtube_video_as_mp3(youtube_url, output_path)
    print(f"MP3 file saved to: {mp3_file}")

    transcription = transcribe_audio(mp3_file)
    # Clean video title to create a valid file name
    valid_title = "".join(
        [c if c.isalnum() or c in (" ", ".", "_") else "_" for c in video_title]
    )
    output_file = os.path.join(output_path, f"{valid_title}.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    print(f"Transcription saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube video as MP3 and transcribe using Whisper."
    )
    parser.add_argument("--url", type=str, help="The URL of the YouTube video")
    args = parser.parse_args()

    # Set the output path to ./outputs/
    output_path = "./outputs/"

    # Create the outputs directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    while True:
        if args.url:
            youtube_url = args.url
            args.url = None  # Reset args.url after first use
        else:
            youtube_url = input("Enter the YouTube URL (or type 'exit' to quit): ")

        if youtube_url.lower() == "exit":
            break

        try:
            process_url(youtube_url, output_path)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    if torch.cuda.is_available():
        print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA is not available. Using CPU.")

    main()
