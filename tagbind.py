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

OUTRO_YOUTUBE = './outros/YouTube_Outro.mp4'

# prepare argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('input_directory', help='Our initial directory of tags to go through and scan')
parser.add_argument('output_file', help='The final file destination that we want to render to')
parser.add_argument('-recurse',help='Scan directories recursively',action='store_true')
parser.add_argument('-target',help='The target amount of clips to aim for per video',default = 15)
parser.add_argument('-platform',help='Helps keep track of a specified platform for tags',default = 'youtube')
parser.add_argument('-shuffle',help='Shuffles the clips instead of sorting them alphabetically',action='store_true')
parser.add_argument('-allow-repeat',help='Allow Repeat', action='store_true')
parser.add_argument('-no-database-save',help='Do not save in the database')

# parse command line arguments
command_line_arguments = parser.parse_args()

video_directory = command_line_arguments.input_directory
output_file = command_line_arguments.output_file
recurse_directory = command_line_arguments.recurse
target_tag_count = int(command_line_arguments.target)
target_platform = command_line_arguments.platform
shuffle_videos = command_line_arguments.shuffle



#output our input and output information
print("Input Directory\t:\t{input}\nOutput File\t:\t{output}".format(input = video_directory, output = output_file))


# initialize our database
database_connection = VideoDatabase()
database_connection.connect()

if recurse_directory:
	print("Scanning  directory recursively for video files")
else:
	print("Scanning directory for video files")


# scan for all files in our video directory 
glob_search = "{input}/*.mp4".format(input = video_directory)
video_files = glob.glob(glob_search, recursive = recurse_directory)

# now that we have searched for all of our files, determine which ones are new compared to the last time we ran the program
new_files = []
for file in video_files:
	if database_connection.already_used(file):
		continue
	else:
		new_files.append(file)

if shuffle_videos:
	random.shuffle(new_files)

# count how many clips we are going to use in our slice
using_clips = len(new_files[:target_tag_count])

# if we have no clips we are going to terminate the script right here right now
if using_clips == 0:
	print('No clips found...video cannot be produced')
	sys.exit()

# out of those new files grab X amount based on target clip
print("New Clips Found: {new_count}\tUsing: {using_count}".format(new_count=len(new_files),using_count = using_clips))

# prepare our video encoder
video_encoder = VideoEncoder(1280, 720, 60, True, False)

for file in new_files[:target_tag_count]:
	print("Using\t: {tag}".format(tag=file))
	video_encoder.add_clip(file, "Banner Text")

# append our outro 
video_encoder.add_outro(OUTRO_YOUTUBE)
#video_encoder.add_music("./Samples/song1.mp3")
#video_encoder.add_music("./Samples/song2.mp3")

# create video
video_encoder.create(output_file)


# ask if the video output was saved. ATM this doesnt do anything either
ok_input = input('Did the video save? y/n > ')
if len(ok_input) > 0 and ok_input.lower()[0] == 'y':
	print('Success! Saving into database')
	for file in new_files[:target_tag_count]:
		database_connection.add_video(file)

else:
	print('Please check the log (DEV NOTE: THIS IS NOT IMPLEMENTED)')


database_connection.close()