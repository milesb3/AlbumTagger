import sys
import os
import pandas
import subprocess
import eyed3
from eyed3.id3.frames import ImageFrame

#TODO Remove filename_out and just have it determined by filename in
#TODO find way to pull tracklist from rym

#Check user input
if (len(sys.argv) < 2):
    print("Insufficient number of arguments provided!")
    exit(-1)
elif (not os.path.exists(sys.argv[1])):
    print("Input file not found!")
    exit(-1)

album_csv :str = sys.argv[1]

#Read csv into pandas DataFrame
try:
    album_df :pandas.DataFrame = pandas.read_csv(album_csv)
except Exception as error:
    print(f'Could not parse input file {album_csv}:')
    print(error)

#TODO Check all columns present
if ("dir" not in album_df.columns or "filename_in" not in album_df.columns or "filename_out" not in album_df.columns):
    print("Input csv file does not match the expected format!")
    exit(-1)

for i in range(len(album_df.index)):
    #Convert file to mp3 if necessary
    if (album_df.loc[i]["filename_in"][-4:] != ".mp3"):
        convert_in :str = f'{album_df.loc[i]["dir"]}/{album_df.loc[i]["filename_in"]}'
        convert_out :str = f'{album_df.loc[i]["dir"]}/{album_df.loc[i]["filename_out"]}'
        subprocess.run(f'ffmpeg -i {convert_in} {convert_out}', shell=True)
    else:
        subprocess.run(f'cp {album_df.loc[i]["dir"]}/{album_df.loc[i]["filename_in"]} {album_df.loc[i]["dir"]}/{album_df.loc[i]["filename_out"]}', shell=True)

    #Tag mp3 file 
    #TODO improve error checking
    mp3_file :eyed3.core.AudioFile = eyed3.load(f'{album_df.loc[i]["dir"]}/{album_df.loc[i]["filename_out"]}')

    mp3_file.tag.album = album_df.loc[i]["album"]
    mp3_file.tag.album_artist = album_df.loc[i]["album_artist"]
    mp3_file.tag.images.set(ImageFrame.FRONT_COVER, open(album_df.loc[i]["cover"],"rb").read(), "image/png")
    mp3_file.tag.year = album_df.loc[i]["year"]
    mp3_file.tag.genre = album_df.loc[i]["genre"]
    mp3_file.tag.artist = album_df.loc[i]["artist"]
    mp3_file.tag.disc_num = int(album_df.loc[i]["disc"])
    mp3_file.tag.track_num = int(album_df.loc[i]["track_number"])
    mp3_file.tag.title = album_df.loc[i]["track_title"]
    
    mp3_file.tag.save()