"""
Program Name: Tag Bind
Author: Gabriele M. Nunez ( https://github.com/GabrieleNunez )
Description: Combines video files through ffmpeg  targeted toward the Level Crush channel 
"""
import sys
import os
import os.path
import glob
import argparse
import random
import subprocess
from pprint import pprint
from video_database  import VideoDatabase
from video_encoder import VideoEncoder
from Config import Configuration

OUTRO_YOUTUBE = './outros/YouTube_Outro.mp4'



configs = Configuration()






#output our input and output information
print("Input Directory\t:\t{input}\nOutput File\t:\t{output}".format(input=configs.input, output=configs.output))


# initialize our database
database_connection = VideoDatabase()
database_connection.connect()

if configs.recurse:
	print("Scanning  directory recursively for video files")
else:
	print("Scanning directory for video files")


# scan for all files in our video directory 
glob_search = "{input}/*.mp4".format(input = configs.input)
video_files = glob.glob(glob_search, recursive = configs.recurse)

# now that we have searched for all of our files, determine which ones are new compared to the last time we ran the program
new_files = []
for file in video_files:
	if database_connection.already_used(file):
		continue
	else:
		new_files.append(file)

if configs.shuffle:
	random.shuffle(new_files)

# count how many clips we are going to use in our slice
using_clips = len(new_files[:configs.clip_count])

# if we have no clips we are going to terminate the script right here right now
if using_clips == 0:
	print('No clips found...video cannot be produced')
	sys.exit() 

# out of those new files grab X amount based on target clip
print("New Clips Found: {new_count}\tUsing: {using_count}".format(new_count=len(new_files),using_count = using_clips))

# prepare our video encoder
video_encoder = VideoEncoder(configs.width, configs.height, configs.fps, True, False)

for file in new_files[:configs.clip_count]:
	print("Using\t: {tag}".format(tag=file))
	video_encoder.add_clip(file, "Banner Text")

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
	for file in new_files[:configs.clip_count]:
		database_connection.add_video(file)

else:
	print('Please check the log (DEV NOTE: THIS IS NOT IMPLEMENTED)')


database_connection.close()