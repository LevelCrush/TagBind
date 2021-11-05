from video_manager import VideoManager
from ffmpeg_wrapper import FFmpeg

video_manager = VideoManager("./Samples")
ffmpeg = FFmpeg()
for video in video_manager.videos:
    ffmpeg.addClip(video)
ffmpeg.run()