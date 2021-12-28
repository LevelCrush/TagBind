"""
Program Name: Tag Bind
Author: Gabriele M. Nunez ( https://github.com/GabrieleNunez )
Description: Combines video files through ffmpeg  targeted toward the Level Crush channel 
"""
import sys
from video_database  import VideoDatabase
from video_encoder import VideoEncoder
from Config import Configuration

OUTRO_YOUTUBE = './outros/YouTube_Outro.mp4'

configs = Configuration()

#output our input and output information
print("Input Directory\t:\t{input}\nOutput File\t:\t{output}".format(input=configs.input, output=configs.output))

# initialize our database
database_connection = VideoDatabase(configs.input, configs.recurse)
database_connection.scan_clips()
clips = database_connection.get_clips(configs.clip_count, configs.shuffle, not configs.repeat)

if len(clips) == 0:
	print('No clips found...video cannot be produced')
	sys.exit()

# prepare our video encoder
video_encoder = VideoEncoder(configs.width, configs.height, configs.fps, configs.banners, configs.mute_clips,configs.volume,configs.transition_duration,configs.vcodec,configs.acodec)

for file, banner in clips:
	print("Using\t: {tag}, {name}".format(tag=file, name=banner))
	video_encoder.add_clip(file, banner)

# append our outro 
video_encoder.add_outro(OUTRO_YOUTUBE)
#video_encoder.add_music("./Samples/song1.mp3")
#video_encoder.add_music("./Samples/song2.mp3")

# create video
if video_encoder.create(configs.output):
	print(f'Success! Saving into database, Montage ID: {database_connection.save_montage(configs.output)}')
else:
	print('Failed, Please check the log (DEV NOTE: THIS IS NOT IMPLEMENTED)')

database_connection.close()