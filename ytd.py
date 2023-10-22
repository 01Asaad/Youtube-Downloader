from pytube import YouTube
from pytube import exceptions
from moviepy.editor import AudioFileClip
  
def download_video(options) :
    try : yt = YouTube(options["video_url"])
    except exceptions.RegexMatchError : raise Exception("Failed to get the video, make sure the link is valid")
    except : raise Exception("Failed to get the video, make sure your internet is working and the link is valid")

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

if __name__ == "__main__" :
    try :
        import json
        with open("options.json", "r") as f :
            options=json.loads(f.read())
    except :
        options={}
        options["video_url"] = "    "
        options["only_audio"]=True
        options["resolution"] = '720p'
    download_video(options)
    print("downloaded")