import os
for root, dirs, files in os.walk("~/Music/Music"):
    for file in files:
    	print file
        if file.endswith(".txt"):
             print(os.path.join(root, file))