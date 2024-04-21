from AlbumInfo import AlbumInfo

import sys
import os
import subprocess
import eyed3
from eyed3.id3.frames import ImageFrame
from eyed3.core import Date

#TODO find way to pull tracklist from rym
#TODO add option to print AlbumInfo

#Handle user input
if (len(sys.argv) < 2):
    print("Insufficent parameters provided! Run program lie 'python3 tag_album <.atd file>'")
    exit(-1)
elif (not os.path.exists(sys.argv[1])):
    print("Input file not found!")
    exit(-1)
elif (sys.argv[1][-4:] != ".atd"):
    print("Input file does not have the correct extension, .atd!")
    exit(-1)

atd_file :str = sys.argv[1]

#Parse .atd file using AlbumInfo class
album_info :AlbumInfo = AlbumInfo(atd_file)

#Loop through all tracks
for track_info in album_info.tracks_info:
    #Convert track file to mp3 if necessary
    if track_info.filename[-4:] != ".mp3":
        #Convert file with ffmpeg
        convert_in :str = f'{album_info.dir}{track_info.filename}'
        #Update filename to .mp3
        track_info.filename = os.path.splitext(track_info.filename)[0] + ".mp3"
        convert_out :str = f'{album_info.dir}{track_info.filename}'

        try:
            subprocess.run(f'ffmpeg -i {convert_in} {convert_out}', shell=True)
        except Exception as error:
            print(f'Error! Failed to convert {convert_in} to {convert_out} using ffmpeg. Received error message:')
            print(error)
            continue

    #Tag mp3 file 
    mp3_file :eyed3.core.AudioFile = eyed3.load(f'{album_info.dir}{track_info.filename}')

    mp3_file.tag.album = album_info.album
    mp3_file.tag.album_artist = album_info.album_artist
    mp3_file.tag.images.set(ImageFrame.FRONT_COVER, album_info.cover_bytes, f'image/{os.path.splitext(album_info.cover_path)[1][1:]}')
    mp3_file.tag.year = Date(album_info.year)
    mp3_file.tag.genre = album_info.genre
    mp3_file.tag.artist = track_info.artist
    mp3_file.tag.disc_num = track_info.disc_num
    mp3_file.tag.track_num = track_info.track_num
    mp3_file.tag.title = track_info.track_title
    
    mp3_file.tag.save()