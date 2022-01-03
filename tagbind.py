"""
Program Name: Tag Bind
Author: Gabriele M. Nunez ( https://github.com/GabrieleNunez ), Austin Harms (https://github.com/austinharms)
Description: Combines video files through ffmpeg  targeted toward the Level Crush channel 
"""
import sys
from video_database import VideoDatabase
from video_encoder import VideoEncoder
from Config import Configuration

# Load configs and args
configs = Configuration()
print("Input Directory\t:\t{input}\nOutput File\t:\t{output}".format(input=configs.input, output=configs.output))

# initialize our database
database_connection = VideoDatabase(configs.input, configs.recurse)
database_connection.scan_clips()

# Load clips from db
if configs.montage_id != -1:
    clips = database_connection.get_montage_clips(configs.montage_id)
else:
    clips = database_connection.get_clips(configs.clip_count, configs.shuffle, not configs.repeat)

if len(clips) == 0:
    print('No clips found...video cannot be produced')
    database_connection.close()
    sys.exit()

# Create video encoder with configs
video_encoder = VideoEncoder(configs.width,
                             configs.height,
                             configs.fps,
                             not configs.disabled_banners,
                             configs.font,
                             configs.mute_clips,
                             configs.music_volume,
                             configs.transition_time,
                             configs.vcodec,
                             configs.acodec)

# Log and load clips into video encoder
for file, banner in clips:
    print("Using:\t{tag},\t{name}".format(tag=file, name=banner))
    video_encoder.add_clip(file, banner)

# Add outro if any
if configs.outro != "":
    print("Add Outro: " + configs.outro)
    video_encoder.add_outro(configs.outro)

if len(configs.music) > 0:
    for song in configs.music:
        video_encoder.add_music(song)
        print("Add Song: " + song)

# Create the video
if video_encoder.create(configs.output):
    if not configs.no_database_save:
        print(f'Success! Saving into database, Montage ID: {database_connection.save_montage(configs.output)}')
    else:
        print('Success!')
else:
    print('Failed')

# Save any changes to the db
database_connection.close()
