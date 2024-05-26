import musicbrainzngs

#TODO set this as command line input
atd_filename = "capsule-losing-contact.atd"
release_id = "6e8f4e70-01cf-4cb8-bd32-84a537acb3e5"

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

    for disc_num, disc in enumerate(result["release"]["medium-list"]):
        for track_num, track in enumerate(disc["track-list"]):
            atd_file.write(f'        \t|{disc_num+1}\t|{track_num+1}\t|{track["recording"]["title"]}\t|{album_artist}\n')

    atd_file.close()

    print(f'Successfully generated "{atd_filename}"! You will need to specify the cover art path, genres, and filenames in this atd file before using it with tag_album.py.')