from pytube import YouTube
from moviepy.editor import AudioFileClip
  
def download_video(options) :
    yt = YouTube(options["video_url"])

    if options["only_audio"] :
        stream = yt.streams.filter(only_audio=True).first()
    else : stream = yt.streams.filter(res=options["resolution"], file_extension='mp4', progressive=True).first()

    if stream:
        print(f'Downloading {yt.title} in {options["resolution"]}')
        stream.download()
        if options["only_audio"] :
            audio_clip = AudioFileClip(yt.title + ".mp4")
            audio_clip.write_audiofile(yt.title + ".mp3")
            audio_clip.close()
        return True
        
    else:
        raise Exception(f'Video in {options["resolution"]} is not available for {yt.title}')

    # Optional: Include audio download (remove the '-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"' part if not needed)
    # To get the best quality (video and audio), you can use the following:
    # yt.streams.get_highest_resolution().download(output_path='path_to_save_video')

if __name__ == "__main__" :
    try :
        import json
        with open("options.json", "r") as f :
            options=json.loads(f.read())
    except :
        options={}
        options["video_url"] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        options["only_audio"]=True
        options["resolution"] = '720p'
    download_video(options)
    print("downloaded")