#!/usr/bin/python
import sys
import os

# Help message
if len(sys.argv) < 3:
	print(
		'Usage: tv-rename.py DIRECTORY... SEASON...\n' +
		'Batch renames files for TV series from an episodes.txt in the target directory.')
	quit()

# Sysargs
path = sys.argv[1]
season = sys.argv[2]

# Set dir
os.chdir(path)

# Consistent name construction
def nameConst(season, episode, name, ext):
	name = (season.zfill(2)  # Season no. padded
		+ 'x'  # Separator between season and ep
		+ episode.zfill(2)  # Episode no. padded
		+ ' - '  # Separator between designation and name
		+ name.strip()  # Episode name (strip newline)
		+ ext)  # Original extension name
	return name

# Preprocessing
try:
	with open('episodes.txt', mode='r') as episodes:
		names = episodes.readlines()
except FileNotFoundError:
	# Create file if can't open
	with open('episodes.txt', mode='a'):
		pass
	input('episodes.txt has been created, please populate\npress enter to exit...')
	quit()

files = sorted(os.listdir())
files.remove('episodes.txt')

# Safety check -- same amount of files as names
if len(files) != len(names):
	input('Mismatch between file count and episode names\npress enter to exit...')
	quit()

# Preview so I don't mess anything up accidentally
print('Preview:')
for i, file in enumerate(files):
	print('\t'  # Tab
		+ file  # Original file name
		+ ' -> '  # Separator
		+ nameConst(season, str(i+1), names[i], os.path.splitext(file)[1]))  # New file name

# Confirmation
con = input('Continue? [Y/n] ')
if con.lower() != 'y' and con != '':
	quit()

# Renaming
for i, file in enumerate(files):
	os.rename(file, nameConst(season, str(i+1), names[i], os.path.splitext(file)[1]))

# Done
print('Complete')
