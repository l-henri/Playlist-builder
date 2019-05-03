# Playlist Builder
A short Python program to gather all my bookmarked mp3 in a single folder.

Back when having huge folders with hundreds of MP3 album was a thing, long before Spotify, I used a simple system to bookmark the music I liked in an album.

I would simply leave a file called _tracks.txt in the folder, containing the number of the track I liked.

A simple script that will scan all the folders designated, find all the files named _tracks.txt, read all the flagged tracks and copy them in a new folder, Music_extracted.

Also, since iTunes does not like .mp3, it automatically converts .flac to .mp3.

## Requirements
> pip install requirements.txt
