#!/usr/bin/env python3

## IMPROVEMENTS

## it is possible to name edges in the graph, see https://www.graphviz.org/pdf/dotguide.pdf
## we would need a pretty large update to parse the files to get this info

import sys
import re
from pathlib import Path

def main():
	if len(sys.argv) != 2:
		sys.exit('ERROR: Improper usage of script. Proper usage is "python3 generate_dot_file.py <folder_to_recursively_traverse_for_cpp_files>')

	folder_to_traverse = sys.argv[1]
	folder = Path(folder_to_traverse)

	if not folder.exists():
		sys.exit('ERROR: Cannot find directory "' + folder_to_traverse + '"')

	if not folder.is_dir():
		sys.exit('ERROR: "' + folder_to_traverse + '" is not a directory')

	cpp_files = find_cpp_files_in_dir(folder, excluded_folders='([tT]est|inc|obj|\\.idea|cmake|\\.git)')

	if len(cpp_files) == 0:
		sys.exit('ERROR: No cpp files found after recursively searching through directory "' + folder_to_traverse + '"')
	
	screen_links = {}
	for file in cpp_files:
		screen_name, links = get_outgoing_screens(file, matcher='(currentScreen = screenName|currentScreen = sessionData::ms_previousScreen)')
		screen_links[screen_name] = links

	err = validate_links(screen_links)
	if err:
		sys.exit('ERROR: Validation failed! See messages printed to stderr')

	#GraphViz DOT file format
	print('digraph G {')
	for screen in screen_links:
		if len(screen_links[screen]) == 0:
			continue # either this is a utility class or screens are navigated to in unconventonial ways so we will skip it
		print('\t' + screen + ' -> { ', end='')
		for link in screen_links[screen]:
			print (link + ' ', end='')
		print('};')
	print('}')


def find_cpp_files_in_dir(folder, excluded_folders):
	cpp_files = []
	for path in folder.iterdir():
		if path.is_dir():
			if re.search(excluded_folders, str(path)) != None:
				continue # skip any file or folder that contains this pattern
			cpp_files.extend(find_cpp_files_in_dir(Path(path), excluded_folders))
		elif path.suffix == '.cpp':
			cpp_files.append(path)

	return cpp_files


def get_outgoing_screens(file, matcher):
	file_name = str(file).split('/')[-1][:-4]
	screen_name = file_name[:1].lower() + file_name[1:] # make the first letter lowercase to match the screenName enum
	screen_name = manually_fix_broken_screen_names(screen_name)
	links = []

	with file.open() as f:
		for line in f.readlines():
			if line.lstrip().startswith('//'):
				continue
			if re.search(matcher, line) != None:
				link = line.split(';')[0].split(':')[-1]
				links.append(link)

	return screen_name, links


def manually_fix_broken_screen_names(screen_name):
	if screen_name == 'buttonDebuggerScreen':
		return 'buttonTesterScreen'
	if screen_name == 'caseIdScreen':
		return 'scanCaseIdScreen'
	return screen_name


def validate_links(screen_links):
	validation = {}
	for key in screen_links:
		validation[key] = True # was delcared as a key in screen_links which means it is a screen you can go to

		for link in screen_links[key]:
			if link == 'ms_previousScreen':
				continue
			if link not in validation:
				validation[link] = False # linked to, but not declared as a screen you can go to

	err = False
	for key in validation:
		if validation[key] == False:
			err = True
			sys.stderr.write(key + ' was linked to, but was not found as a key in screen_links!\n')
	return err


def print_links(screen_links):
	for key in screen_links:
		print(key + ':')
		for link in screen_links[key]:
			print('\t' + link)


if __name__ == '__main__':
	main()
