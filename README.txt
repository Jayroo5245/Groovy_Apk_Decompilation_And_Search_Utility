This is README file for an Android Apk decompiler and search script

This utility takes a directory with Android applications, converts all the apks
in that directory to .jar files, extracts all of them to an archive
directory, then converts all the .class files to human readable .java
files and then searches query terms. The java files will be 
under <home>/<working_directory>/<app_name>/archive/decompiled_java. The 
search results will be in a file in the working directory called SearchResults.txt

Assumptions: 
1. Java and Python are on your path.
If not here are links to download them:
	Java: http://www.java.com/en/download/index.jsp
	Python: http://www.python.org/getit/
	
2. That whomever is using this utility has extracted all files from the compressed version
of the utility into some directory which I will refer to as "working_directory".

3. Finally have fun good luck and hopefully it all works =)

Setup:
1. Copy all applications to decompile and search too: <home>/<working_directory>/apks/
2. If a search of the resulting decompiled .java files is desired, Add a query term to each line of SearchQueries.txt
3. launch from terminal: python decompilationAndSearchScript.py