#!/usr/bin/python3
# decompilationAndSearchScript.py
#
# Author: Jared Sheehan
# Email: jaredasheehan@gmail.com
# The directory structure for this script was written to run on a mac but
# could easily be ported to a PC.
#
####################################################################
# This python file takes a directory as input, converts all the apks
# in that directory to .jar files, extracts all of them to an archive
# directory, then converts all the .class files to human readable .java
# files. The .java files will be 
# under <home>/<working_directory>/<app_name>/archive/decompiled_java

import re
import sys
import datetime
import os
import shutil

#########   Constants   #########
#Directory containing all the apks to be parsed.
APK_DIRECTORY = 'apks'

# Download: http://code.google.com/p/dex2jar/
DEX2JAR_HOME = "lib/dex2jar-2.0/d2j-dex2jar.sh"

# Good list of params that Jad takes:
# http://www.rune-server.org/runescape-development/rs2-server/help/377966-help-please-lost-my-files-but-rep.html
# Download: http://www.varaneckas.com/jad/
JAD_HOME = "lib/jad158g.mac.intel/jad"

#jar util home
JAR_HOME = '/usr/bin/jar'

#########   End Constants   #########

########################################################################
def setup(s_string):
	os.mkdir(s_string)
########################################################################

########################################################################
def printApkList(apkDirectory):
	print '\n	-------List of all of the apks to Parse-------\n'
	for dirname, dirnames, filenames in os.walk(apkDirectory):
		for subdirname in dirnames:
			print os.path.join(dirname, subdirname)
		for filename in filenames:
			print os.path.join(dirname, filename)
########################################################################
def search(applicationFilenameBeingSearched, queryString, workingDirectory):
	print '\n	-------Start Search-------\n'
	print ' 	-------Search Term: ' + queryString
	for dirname, dirnames, filenames in os.walk(workingDirectory):
		for subdirname in dirnames:
			print '.....'
		for filename in filenames:
			if filename.endswith('.java'):
				file = open(dirname + '/' + filename,'r')
				for line in file:
					if line.find(queryString) > -1:
						found = 'Found: ' + queryString
						inline = 'In line: ' + line
						offile = 'Of file: ' + filename
						print found
						print inline
						print offile
						searchResultsFile.write('\n\n---Found Query Term---')
						searchResultsFile.write('\nName of Application: ' + applicationFilenameBeingSearched)
						searchResultsFile.write(': ' + found)
						searchResultsFile.write('\n   ' + line)
						searchResultsFile.write('\n   ' + offile)
						searchResultsFile.write('\n---------------------')
				file.close()
########################################################################
def decompileClassFilesToJavaFormat(currentDirectory, archiveDirectory):
	print '\n	-------Starting Converstion from .class format to .java-------\n'
	os.system (currentDirectory + '/' + JAD_HOME + ' -o -r -sjava -ddecompiled_java **/*.class')	
########################################################################
def convertApksToJar(apkDirectory, currentDirectory, workingDirectory):
	print '\n	-------Start Conversion from APK to JAR-------\n'
	for dirname, dirnames, filenames in os.walk(apkDirectory):
		for subdirname in dirnames:
			print os.path.join(dirname, subdirname)
		for filename in filenames:
			#Remove the .apk from the directory name
			print '\n	Start decompilation for application: ' + filename + '\n'
			createDirectory = workingDirectory + filename[:-4]
			createDirectoryPlusArchive = createDirectory + '/' + 'archive'
			print 'Creating Directory: ' + createDirectory
			os.mkdir(createDirectory)
			os.mkdir(createDirectoryPlusArchive)
			copyFromDir = currentDirectory + '/' + apkDirectory + '/' + filename
			print 'copyFromDir: ' + copyFromDir
			os.system ("cp" + " " + copyFromDir + " " + createDirectory)
			#Convert Apk to Jar
			os.system (DEX2JAR_HOME + " " + createDirectory + "/" + filename)
			dex2jarfilename = filename[:-4] + "-dex2jar.jar"
			#Move converted file to the proper directory
			os.system ("mv" + " " + dex2jarfilename + " " + createDirectoryPlusArchive)
			os.chdir(createDirectoryPlusArchive)
			print '\nStarting jar extraction of: ' + dex2jarfilename
			os.system (JAR_HOME + " xf "+ dex2jarfilename)
			print 'Done with extraction: ' + dex2jarfilename
			decompileClassFilesToJavaFormat(currentDirectory, createDirectoryPlusArchive)
			#Iterate through query terms
			print 'Done with extraction: ' + dex2jarfilename
			print 'Start the search process from within the ' + filename + ' application'
			for line in searchQueriesArray:
				search(filename, line, createDirectory)
			os.chdir(currentDirectory)
			print '\n	---APK Conversion, Decompilation and Search Completed---\n'
########################################################################

# Begin Main()
now = datetime.datetime.now()
converted_jar_file_directory_root = 'workspace_root_' + str(now.month) + '_' + str(now.day) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second) + '/'
currentDirectory = os.getcwd()
searchResultsFile = open("searchResults.txt", "w")
searchQueriesFile = open("SearchQueries.txt", "r")
searchQueriesArray=[]
for line in searchQueriesFile:
	if (line.find("#") != 0) and (len(line) > 0):
		searchQueriesArray.append(line)
print "\nName of the file Search Results will be written to: ", searchResultsFile.name
workingDirectory = currentDirectory + '/' + converted_jar_file_directory_root
print 'currentDirectory: ' + currentDirectory
print 'workingDirectory: ' + workingDirectory
setup(converted_jar_file_directory_root)
printApkList(APK_DIRECTORY)
convertApksToJar(APK_DIRECTORY, currentDirectory, workingDirectory)
print "Decompiled files in: " + converted_jar_file_directory_root
print "Search Results in: searchResults.txt"
print "\n   ---Thanks for Playing!---"
searchResultsFile.close()
searchQueriesFile.close()
