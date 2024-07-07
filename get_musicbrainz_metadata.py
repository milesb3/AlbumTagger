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

    if "-f" in input_switches:
        #Extract directory of filenames from atd_filename
        path_end_i :int = -1
        for i, character in enumerate(atd_filename):
            if character == "/":
                path_end_i = i
        if path_end_i == -1:
            atd_dir = "."
        else:
            atd_dir :str = atd_filename[:path_end_i+1]

        #Add any files with music extensions to the filenames list
        filenames :list[str] = []
        common_music_file_extensions = [".mp3", ".opus", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma", ".aiff", "alac", "ape"]
        for file in os.listdir(atd_dir):
            if os.path.splitext(file)[1] in common_music_file_extensions:
                filenames.append(file)
        filenames = sorted(filenames)

    #Create list to store track information for printing
    track_print :list[list[str]] = []
    track_print.append(["filename", "disc_num", "track_num", "track_title", "artists"])

    #Create iterator to loop through filenames
    filename_i :int = 0

    #Write track information to track_print
    for disc_num, disc in enumerate(result["release"]["medium-list"]):
        for track_num, track in enumerate(disc["track-list"]):
            try:
                track_print.append([filenames[filename_i], str(disc_num+1), str(track_num+1), track["recording"]["title"], album_artist])
                filename_i += 1
            except:
                track_print.append(["", str(disc_num+1), str(track_num+1), track["recording"]["title"], album_artist])

    #Find longest entry in each column, so table of track info can be printed in a more organized fashion
    col_lengths :list[int] = [0] * len(track_print[0])
    for row in track_print:
        for i in range(len(row)):
            if len(row[i]) > col_lengths[i]:
                col_lengths[i] = len(row[i])

    #Write track info to atd.file
    for row in track_print:
        for i in range(len(row)):
            atd_file.write(f'{row[i]}{" "*(col_lengths[i]-len(row[i]))}')
            if i != (len(row) - 1):
                atd_file.write("\t|")
        atd_file.write("\n")

    atd_file.close()

    print(f'Successfully generated "{atd_filename}"! Please check the cover art path, genres, and filenames in this atd file before using it with tag_album.py.')