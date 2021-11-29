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
database_connection.connect()
database_connection.scan_clips()
clips = database_connection.get_clips(configs.clip_count)
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
video_encoder.create(configs.output)


# ask if the video output was saved. ATM this doesnt do anything either
ok_input = input('Did the video save? y/n > ')
if len(ok_input) > 0 and ok_input.lower()[0] == 'y':
	print('Success! Saving into database')
	database_connection.save_montage()
else:
	print('Please check the log (DEV NOTE: THIS IS NOT IMPLEMENTED)')