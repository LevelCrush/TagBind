"""
manages the video database configuration 
TODO: migrate this over to mysql or sqlite for a better setup, currently it is using json which is inefficient for larger scopes, for now it gets the job done
"""
import os 
import os.path
import json
import pathlib
from pprint import pprint

VIDEO_DATABASE_FILE = 'videodatabase.json'

class VideoDatabase:

	# constructor for the video database class, just initialize all variables
	def __init__(self):
		self.used_videos = [] # container that already knows about videos we created previously
		self.created_videos = [] # container for any new videos we created this session
		self.database = {} # initialize an empty database instance

	# connect to the "database" although ATM this is just connected to a JSON file
	def connect(self): 
		database_path = pathlib.Path(VIDEO_DATABASE_FILE)
		if database_path.is_file(): # our file exists
			with database_path.open() as database_pointer:
				self.database = json.load(database_pointer)
				self.used_videos = self.database['videos']
			print('Database loaded')
		else:
			self.database = { 'videos' : [0] } 
			with database_path.open(mode='w') as database_pointer:
				json.dump(self.database, database_pointer)
			print('Initialized Database')

	# determine if we have already used a vidoe file
	def already_used(self, video_file):
		return video_file in self.used_videos or video_file in self.created_videos

	def add_video(self, video_file):
		if self.already_used(video_file):
			return False
		else:
			self.created_videos.append(video_file)
			return True

	# save and close any connection
	def close(self): 

		# extend the videos 
		self.database['videos'].extend(self.created_videos)

		# save the database connections
		database_path = pathlib.Path(VIDEO_DATABASE_FILE)
		with database_path.open(mode='w') as database_pointer:
			json.dump(self.database, database_pointer)
		print("Saved database")