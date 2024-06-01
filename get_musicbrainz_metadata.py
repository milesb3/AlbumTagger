import sys
import musicbrainzngs
import os

#Handle user input
#Sort normal input and switch input. Switch inputs start with "-"
input_normal :list[str] = []
input_switches :list[str] = []
for i in range(1,len(sys.argv)):
    input_switches.append(sys.argv[i]) if (sys.argv[i][0] == "-") else input_normal.append(sys.argv[i])

#Handle normal input
if len(input_normal) < 2:
    print("Insufficient number of arguments provided! Please provide input like <atd_filename> <musicbrainz_release_id>. For example:")
    print("python3 get_musicbrainz_metadata.py aphex_twin_drukqs.atd facbe59c-6bf7-45c6-bb0c-85aaba8d8670")
    exit(-1)
else:
    atd_filename :str = input_normal[0]
    release_id :str = input_normal[1]
    del input_normal

print("Executing request with musicbrainzngs...")
musicbrainzngs.set_useragent("album-tagger", "0.1")
try:
    result = musicbrainzngs.get_release_by_id(release_id, includes=["recordings", "artists", "labels"])
except Exception as error:
    print(f'Error! Failed to fetch release:\n{error}')
else:
    print(f'Generating "{atd_filename}"...')
    album :str = result["release"]["title"]
    album_artist :str = result["release"]["artist-credit-phrase"]
    year :str = result["release"]["date"].split("-")[0]

    atd_file = open(atd_filename, "w")
    atd_file.write(f'#{atd_filename}\n\n')
    atd_file.write(f'album = {album}\n')
    atd_file.write("cover_file_path =\n")
    atd_file.write(f'album_artist = {album_artist}\n')
    atd_file.write(f'year = {year}\n')
    atd_file.write("genre =\n\n")
    atd_file.write("filename\t|disc_num\t|track_num\t|track_title\t|artists\n")

    #TODO Handle -f switch for inputting filenames into atd file

    for disc_num, disc in enumerate(result["release"]["medium-list"]):
        for track_num, track in enumerate(disc["track-list"]):
            atd_file.write(f'        \t|{disc_num+1}      \t|{track_num+1}       \t|{track["recording"]["title"]}\t|{album_artist}\n')

    atd_file.close()

    print(f'Successfully generated "{atd_filename}"! You will need to specify the cover art path, genres, and filenames in this atd file before using it with tag_album.py.')
