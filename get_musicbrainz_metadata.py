import argparse
import musicbrainzngs
import os

COMMON_MUSIC_FILE_EXTS = [".mp3", ".opus", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma", ".aiff", "alac", "ape"]

#Parse user input
parser = argparse.ArgumentParser(
        prog='AlbumTagger_GenAtd',
        description='Fetches album metadata from MusicBrainz and writes it to an atd file')

parser.add_argument('atd_filename')
parser.add_argument('release_id')
parser.add_argument('-f', '--files_include', action='store_true')

args = parser.parse_args()

#Attempt MusicBrainz metadata request
print("executing request with musicbrainzngs...")
musicbrainzngs.set_useragent("album-tagger", "0.1")
try:
    result = musicbrainzngs.get_release_by_id(args.release_id, includes=["recordings", "artists", "labels"])
except Exception as error:
    print(f'error! failed to fetch release:\n{error}')
    exit(1)

#Extract information from result variable into more readable variables
album_title :str = result.get("release", {}).get("title")
album_artist :str = result.get("release", {}).get("artist-credit-phrase")
year :str = result.get("release", {}).get("date")
if (year):
    year = year.split("-")[0]

# --------------------------------------------------------------------
#Generate atd file from MusicBrainz metadata request result
# --------------------------------------------------------------------
print(f'generating "{args.atd_filename}"...')

#Write album-wide information section
atd_file = open(args.atd_filename, "w")
atd_file.write(f'#{args.atd_filename}\n\n')

if (album_title):
    atd_file.write(f'album_title = {album_title}\n')
else:
    atd_file.write("#album_title = (could not extract this data from MusicBrainz)\n")

if (album_artist):
    atd_file.write(f'album_artist = {album_artist}\n')
else:
    atd_file.write("#album_artist = (could not extract this data from MusicBrainz)\n")

if (year):
    atd_file.write(f'year = {year}\n')
else:
    atd_file.write("#year = (could not extract this data from MusicBrainz)\n")

atd_file.write("\n#some optional information to add to your tracks:\n")
atd_file.write("#cover_file_path =\n")
atd_file.write("#genre =\n\n")

#Write track specific information
if (args.files_include):
    #If the files_include flag was set true, all audio files will in current
    #directory will be added to the filenames column in alphanumeric order

    #Extract working directory of filenames from atd_filename
    path_end_index :int = -1
    for i, character in enumerate(args.atd_filename):
        if character == "/":
            path_end_index = i
    if path_end_index == -1:
        atd_dir = "."
    else:
        atd_dir :str = args.atd_filename[:path_end_i+1]

    #Add any files with music extensions to the filenames list
    filenames :list[str] = []
    for file in os.listdir(atd_dir):
        if os.path.splitext(file)[1] in COMMON_MUSIC_FILE_EXTS:
            filenames.append(file)
    filenames = sorted(filenames)

#Create list to store track information for writing to atd file after parsing the 
#track information
track_write :list[list[str]] = []
track_write.append(["filename", "disc_num", "track_num", "track_title", "artists"])

if (args.files_include):
    #Create iterator to loop through filenames
    filename_i :int = 0
    num_filenames = len(filenames)

#Write track information to track_write
for disc_num, disc in enumerate(result["release"]["medium-list"]):
    for track_num, track in enumerate(disc["track-list"]):
        if (args.files_include):
            try:
                track_write.append([filenames[filename_i], str(disc_num+1), str(track_num+1), track["recording"]["title"], album_artist])
                filename_i += 1
            except:
                track_write.append(["", str(disc_num+1), str(track_num+1), track["recording"]["title"], album_artist])

        else:
            track_write.append(["", str(disc_num+1), str(track_num+1), track["recording"]["title"], album_artist])

#Find longest entry in each column, so table of track info can be printed in a more organized fashion
col_lengths :list[int] = [0] * len(track_write[0])
for row in track_write:
    for i in range(len(row)):
        if len(row[i]) > col_lengths[i]:
            col_lengths[i] = len(row[i])

#Write track info to atd.file
for row in track_write:
    for i in range(len(row)):
        atd_file.write(f'{row[i]}{" "*(col_lengths[i]-len(row[i]))}')
        if i != (len(row) - 1):
            atd_file.write("\t|")
    atd_file.write("\n")

atd_file.close()

print(f'"{args.atd_filename}" has been created.')

