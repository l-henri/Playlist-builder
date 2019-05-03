import os
import re
import shutil
from pydub import AudioSegment

newFolder = "Music_Extracted"
musicLocation = "/Volumes/Henri 1/Muz/16_album/"

trackListCounter = 0
totalAudioFiles = 0
overFlowCount = 0
overFlowList = []
overFlowTotal = 0
weirdFormattedTitles = []
countedLinesInFiles = 0 
filesMissed = 0
missedFilesList = []

# Going through folders
for root, dirs, files in os.walk(musicLocation):
	# Going through files
	for file in files:
		# Finding _tracks.txt file a
		musicFileToExtractList = []
		if not file.endswith("_tracks.txt"):
			# print "Rien ici " + file
			continue
		else:
			# Program found a _tracks.txt file
			print(os.path.join(root, file))
			trackListCounter = trackListCounter + 1
			# Create new folders branch in newFolder
			destinationFolder = os.path.join(newFolder,root.replace(musicLocation, ""))
			if not os.path.exists(destinationFolder):
				os.makedirs(destinationFolder)
			print(destinationFolder)
			#Copying tracklist
			trackListFullPath = os.path.join(root, file)
			trackListCopyFullPath = os.path.join(destinationFolder, file)
			print(trackListFullPath, trackListCopyFullPath)
			shutil.copy2(trackListFullPath, trackListCopyFullPath)

			## Extract track numbers
			with open(os.path.join(root, file)) as openTrackFile:

				for line in openTrackFile:

					num = re.findall('\d+', line)
					countedLinesInFiles +=1 
					if num == []:
						print("No number was found here, line is" + str(line))
						if line != '':
							musicFileToExtractList.append(line)
							newFileAdress = os.path.join(destinationFolder , line)
							weirdFormattedTitles.append(newFileAdress)
						continue
					if len(num[0]) < 2:
						num[0] = '0'+num[0]
					musicFileToExtractList.append(str(num[0]))


		# print root
		print(musicFileToExtractList)
		print(countedLinesInFiles)



		
		# Looking  for files & copy, going through musicFileToExtractList
		for musicFileToExtract in musicFileToExtractList:
			# print str(musicFileToExtract)
			trackCounterOverflow = 0
			for fileInSubFolder in os.listdir(root):
				
				# Checking if a file contains the file we look for, copying it if so
				if fileInSubFolder.find(str(musicFileToExtract)) != -1:
					# print fileInSubFolder

					# Avoiding non audio files
					if (fileInSubFolder.endswith(".m3u8") or fileInSubFolder.endswith(".m3u") or fileInSubFolder.endswith(".jpg") or fileInSubFolder.endswith(".nfo") or fileInSubFolder.endswith(".sfv")):
						# print "Esquive!"
						continue
					# Retrieving full original file path, and creating new file path
					fileInSubFolderFullAdress = os.path.join(root , fileInSubFolder)
					newFileAdress = os.path.join(destinationFolder , fileInSubFolder)

					# Converting .flac file
					if (fileInSubFolder.endswith(".flac")  or fileInSubFolder.endswith(".FLAC")):
						flac_audio = AudioSegment.from_file(fileInSubFolderFullAdress, "flac")
						flac_audio.export(fileInSubFolderFullAdress.replace(".flac", ".mp3"), format="mp3")
					
					# Copying file (copying also .flac original file if so)	
					shutil.copy2(fileInSubFolderFullAdress, newFileAdress)

					# Logging copy number
					trackCounterOverflow = trackCounterOverflow +1
					totalAudioFiles = totalAudioFiles + 1
			if trackCounterOverflow > 1:
				print("we might have an overflow issue here")
				overFlowTotal += (trackCounterOverflow-1)
				overFlowCount += 1
				overFlowList.append(newFileAdress)
			elif trackCounterOverflow == 0:
				print("Hum, seems like we missed a file")
				filesMissed += 1
				missedFilesList.append(os.path.join(destinationFolder , musicFileToExtract))

print("We extracted " + str(trackListCounter) + " playlist files and " + str(totalAudioFiles) + " audio files")
print("There was " + str(overFlowCount) + " overflow events, for a total of " + str(overFlowTotal) + " overflow files")
for overFlowEvent in overFlowList:
	print(overFlowEvent)
print("There were " + str(len(weirdFormattedTitles)) + " weird formatting events")
for weirdTitle in weirdFormattedTitles:
	print(weirdTitle)

print("There were " + str(countedLinesInFiles) + " lines counted")

print("We missed " + str(filesMissed) + " files:")
for missedFile in missedFilesList:
	print(missedFile)