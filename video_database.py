"""
manages the video database configuration
"""

import mysql.connector
from mysql.connector import Error
import glob

SQL_HOST = 'videodatabase.json'
SQL_USER = ""
SQL_PASSWORD = ""

class VideoDatabase:

	# constructor for the video database class, just initialize all variables
	def __init__(self, input_dir, recursive=False):
		self.connection = None
		self.cursor = None
		self.input_dir = input_dir
		self.recursive = recursive

	# connect to the "database" although ATM this is just connected to a JSON file
	def connect(self, create_db=True):
		try:
			self.connection = mysql.connector.connect(
				host=SQL_HOST,
				user=SQL_USER,
				passwd=SQL_PASSWORD,
				database="tagbind"
			)
			self.cursor = self.connection.cursor()
			print("Connected to DB")
			return True
		except Error as e:
			if (create_db):
				return self.create_db()
			else:
				print(f"Failed to connect to DB: '{e}'")
				return False

	def create_db(self):
		connection = None
		try:
			connection = mysql.connector.connect(
				host=SQL_HOST,
				user=SQL_USER,
				passwd=SQL_PASSWORD
			)
			print("Connected to SQL, Creating tagbind DB")
		except Error as e:
			print(f"Failed to connect to SQL: '{e}'")
			return False
		try:
			cursor = connection.cursor()
			cursor.execute("CREATE DATABASE tagbind")
			cursor.execute("USE [tagbind] GO SET ANSI_NULLS ON GO SET QUOTED_IDENTIFIER ON GO CREATE TABLE [dbo].[clips]([id] [int] IDENTITY(1,1) NOT NULL, [banner] [varchar](50) NULL, [path] [varchar](260) NOT NULL, [used] [bit] NOT NULL, PRIMARY KEY CLUSTERED ([id] ASC )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY] ) ON [PRIMARY] GO")
			cursor.execute("USE [tagbind] GO SET ANSI_NULLS ON GO SET QUOTED_IDENTIFIER ON GO CREATE TABLE [dbo].[montages]([id] [int] IDENTITY(1,1) NOT NULL, [clip_count] [int] NOT NULL, [path] [varchar](260) NOT NULL, PRIMARY KEY CLUSTERED ([id] ASC)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY] GO")
			cursor.execute("USE [tagbind] GO SET ANSI_NULLS ON GO SET QUOTED_IDENTIFIER ON GO CREATE TABLE [dbo].[montage_clips](	[montageId] [int] NOT NULL,	[clipId] [int] NOT NULL, CONSTRAINT [PK_montage_clips] PRIMARY KEY CLUSTERED ([montageId] ASC,[clipId] ASC )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY] GO ALTER TABLE [dbo].[montage_clips]  WITH CHECK ADD  CONSTRAINT [FK_montage_clips_clip] FOREIGN KEY([clipId]) REFERENCES [dbo].[clips] ([id]) GO ALTER TABLE [dbo].[montage_clips] CHECK CONSTRAINT [FK_montage_clips_clip] GO ALTER TABLE [dbo].[montage_clips]  WITH CHECK ADD  CONSTRAINT [FK_montage_clips_montages] FOREIGN KEY([montageId]) REFERENCES [dbo].[montages] ([id]) GO ALTER TABLE [dbo].[montage_clips] CHECK CONSTRAINT [FK_montage_clips_montages] GO")
			return self.connect(False)
		except Error as e:
			print(f"Failed to Create DB: '{e}'")
			return False

	def scan_clips(self):
		glob_search = "{input}/*.mp4".format(input=configs.input)
		video_files = glob.glob(glob_search, recursive=configs.recurse)
		if self.recursive:
			print("Scanning recursively for clips")
		else:
			print("Scanning for clips")

	def already_used(self, video_file):
		return video_file in self.used_videos or video_file in self.created_videos

	def add_video(self, video_file):
		if self.already_used(video_file):
			return False
		else:
			self.created_videos.append(video_file)
			return True
