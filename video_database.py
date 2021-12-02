"""
manages the video database configuration
"""
import pyodbc
from pyodbc import Error
import glob
import os

from dotenv import load_dotenv
load_dotenv()
SQL_CONNECTION = os.getenv('SQL_CONNECTION_STRING')

class VideoDatabase:

	# constructor for the video database class, just initialize all variables
	def __init__(self, input_dir, recursive=False):
		self._connection = None
		self._cursor = None
		self._input_dir = input_dir
		self._recursive = recursive
		self._current_montage = None
		self._current_montage_id = -1

	# connect to the "database" although ATM this is just connected to a JSON file
	def connect(self, create_db=True):
		try:
			self._connection = pyodbc.connect(SQL_CONNECTION)
			self._cursor = self._connection.cursor()
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
			connection = pyodbc.connect(SQL_CONNECTION)
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
			cursor.commit()
			return self.connect(False)
		except Error as e:
			print(f"Failed to Create DB: '{e}'")
			return False

	def scan_clips(self):
		if self._recursive:
			print("Scanning recursively for clips")
		else:
			print("Scanning for clips")
		video_files = glob.glob(f"{self._input_dir}/*.mp4", recursive=self._recursive)
		for file in video_files:
			self._cursor.execute(f"SELECT * FROM [dbo].[clips] WHERE path = '{file}'")
			res = self._cursor.fetchall()
			if len(res) == 0:
				print(f"New Clip Found: {file}")
				print("Enter Clip Banner Text:")
				banner = input("Enter your value: ")
				self._cursor.execute(f"INSERT INTO [dbo].[clips] ([banner],[path],[used]) VALUES ('{banner}','{file}',0)")
		self._cursor.commit()

	def get_montage_clips(self, montage_id):
		self._current_montage = []
		self._current_montage_id = montage_id
		self._cursor.execute(f"SELECT [clipId],[clipIndex] FROM [dbo].[montage_clips] WHERE montageId = {montage_id}")
		clips = sorted(self._cursor.fetchall(), key=lambda x: x[1])
		for (clipId, index) in clips:
			self._cursor.execute(f"SELECT [path], [banner] FROM [dbo].[clips] WHERE id = {clipId}")
			clips[index] = self._cursor.fetchall()[0]

		return clips

	def get_clips(self, count=0, new_clips=False):
		selector = "WHERE 1 = 1"
		if new_clips:
			selector = "WHERE used = 0"
		self._cursor.execute(f"SELECT TOP {count} * FROM [dbo].[clips] {selector} ORDER BY NEWID()")
		self._current_montage = self._cursor.fetchall()
		self._current_montage_id = -1
		print(self._current_montage)
		clips = []
		for clipId, banner, file, used in self._current_montage:
			clips.append((file, banner))
		return clips

	def save_montage(self, output):
		if self._current_montage_id != -1:
			self._cursor.execute(f"INSERT INTO [dbo].[montages] ([clip_count] ,[path]) OUTPUT INSERTED.id VALUES ({len(self._current_montage)}, '{output}')")
			self._current_montage_id = self._cursor.fetchall()[0][0]
			clip_index = 0;
			for clip_id, name, path, used in self._current_montage:
				self._cursor.execute(f"UPDATE [dbo].[clips] SET [used] = 1 WHERE id = {clip_id}")
				self._cursor.execute(f"INSERT INTO [dbo].[montage_clips] ([montageId],[clipId],[clipIndex]) VALUES ({self._current_montage_id}, {clip_id}, {clip_index})")
				clip_index += 1
			self._cursor.commit()
		return self._current_montage_id
