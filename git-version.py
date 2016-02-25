#!/usr/bin/python
# calling: ./git-version.py <file-to-check> <directory-of-local-git>
# for example: ./git-version.py drupal.js ./drupal7
# 
# Copyright 2016 cornerpirate.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# == Developers
# cornerpirate - https://twitter.com/cornerpirate
import commands
import os
import sys
from argparse import ArgumentParser

# Ok, globals make me feel bad. Sue me.
gitfolder=None
args=None

# taken from http://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def isToolInstalled(name):
    """Check whether `name` is on PATH."""

    from distutils.spawn import find_executable
    return find_executable(name) is not None

# if verbosity is enabled, print that thing
def printv(msg):
	if args.verbose:
		print msg

# get on with the task
def doTheThing():
	printv( "Found git folder: " + gitfolder)
	# check that target file exists
	printv( "Checking that file " + args.file + " exists in the repo within " + args.gitdir)
	cmd = "(cd "  + gitfolder + "; cd .. ; find .  -name " + args.file + ")"
	answer = commands.getoutput(cmd)
	path = answer[2:]
	#print "Path : " + path

	# if we did not find the file in the repo tell the user and end this madness!
	if len(answer)==0:
		print "========================="
		print "Could not find your file using: " + cmd
		print "Make sure that " + args.file + " has the same name as a file in the repository"
		sys.exit(-1)

	answerid=-1
	# if we have found multiple lines we need to remove ambiguity
	if len(answer.split())!=1:
		count=1
		for p in answer.split():
			print str(count) + ")\t" + p
			count = count +1
		print "0) exit"

		while True:
 	
			userpath = raw_input("Multiple files in repo with that name. Enter a number: ")
			if userpath is "0":
				print "========================"
				print "User has chosen to exit, bye..."
				sys.exit(0)


			try:
				usersaid = int(userpath)
				if int(userpath)>=1 and int(userpath)<=len(answer.split()):
					answerid=int(userpath)
					break # get out of the while True
			except:
				a="a" # do nothing

		path = answer.split()[answerid-1]
		printv( "User chose path: " + path)


	# Get the remote URL for the git repo
	cmd = "(cd " + gitfolder + "; cd .. ;  git remote show origin | grep Fetch | cut -d \" \" -f 5)"
        answer = commands.getoutput(cmd)
        printv( "Fetch URL: " + answer)

	# Some repo fetch URLs have ".git" at the end. Some do not. Cope with that
	url=""
	if ".git" in answer:
		url = answer[0:answer.rfind(".")] + "/"
	else:
		url = answer + "/"

	# The repo must support gitweb. I know that github.com does so lets only support that for now
	if not "github.com" in url:
		print "========================="
		print "Sorry, the target needs to have gitweb enabled. This script only works on github.com"
		sys.exit(-1)

	# We need the raw output which is a flip of hostnames to achieve
	url = url.replace("github.com", "raw.githubusercontent.com")
	printv( "Using URL: " + url)

	# Compute the md5 of our users target file
	printv( "Getting MD5 hash for target file")
	cmd = "md5sum " + args.file + " | cut -d \" \" -f 1"  
	answer = commands.getoutput(cmd)
	md5 = answer
	printv( "MD5(" + args.file + "):" + md5)
	
	# we got here so a file with the same name exists, lets get cracking!
	printv( "Checking log for " + args.file)
	cmd = "(cd " + gitfolder + "; cd .. ; git log " + path + " | grep \"commit \" | cut -d \" \" -f 2)"
	answer = commands.getoutput(cmd)

	matchfound=False
	# Ok do the thing we came here to do
	printv( "=========================")
	count=0
	lines = answer.split()
	# for each id 
	for id in lines:
		count=count+1
		# construct the full URL to the raw file on github.com
		fullUrl = url + id + "/" + path
		blobUrl = url + "blob/" + id + "/" + path
		blobUrl = blobUrl.replace("raw.githubusercontent.com", "github.com") # hacky.. hacky.
		# execute a wget to quietly download the file to stdout, and get the md5sum output
		md52 = commands.getoutput("wget -qO - " + fullUrl + " | md5sum | cut -d \" \" -f 1")
		# compare the md5 from our file against the latest version from github.com  
		if md5 == md52:
			# GREAT Success!!
			print "Found at ["+str(count)+"/" + str(len(lines))+ "]: " + blobUrl
			printv( "Match found!")
			printv( "Raw URL: " + fullUrl )
			printv( "Context URL: " + blobUrl)
			printv( "Found at " +str(count) + " of " + str(len(lines)) + " commits of that file ")
			printv( "If it is '1 of 32' then you have the latest version of the file")
			printv( "If it is '30 of 32' then you have a very early version of the file")
			matchfound=True
			break

	# If we get here apparently the git archive does NOT have the same file
	# Most likely the site admin has altered the file slightly or it is from 
	# a different stream of development somehow.
	if matchfound==False:
		print "========================="
		print "We did not find the target file in the revision history"
		print "1) your file version has been altered after a clone"
		print "2) something fishy! Investigate the repo on github.com"
		
	# we are finished entirely
	sys.exit(1)

# Main method, to check input parameters
if __name__ == "__main__":
	# Create argument parer object
	parser = ArgumentParser(description="Finds out the version of a file you have in a git compliant repository")

	# Adding positional items (THESE ARE REQUIRED)
	parser.add_argument("file", help="File to check version of")
	parser.add_argument("gitdir", help="Directory of local git repository")

	# Adding optional items
	parser.add_argument("-v", "--verbose", action="store_true",help="increase output verbosity")

	# parse the user input
	args = parser.parse_args()

	printv("Verbosity Enabled")

	# check that the file exists
	if os.path.isfile(args.file)==False:
		parser.print_help()
		print "==========================="
		print "Provided file did not exist"
		sys.exit(-1)

	# check that the directory exists
	if os.path.isdir(args.gitdir)==False:
		parser.print_help()
		print "=========================="
		print "Provided directory did not exist"
		sys.exit(-1)

	# we know the dir exists. Does it contain a git ?
	# first make sure the folder ends in a /
	gitfolder = args.gitdir if args.gitdir[len(args.gitdir)-1]=="/" else args.gitdir + "/"
	gitfolder = gitfolder + ".git"
	# now check that inside that full path we have a .git folder
	if os.path.isdir(gitfolder)==False:
		parser.print_help()
		print "========================="
		print "Provided directory did not contain a .git folder. Not likely to be a repository"
		sys.exit(-1)

	# check that the OS has the git client installed
	if isToolInstalled("git")==False:
		parser.print_help()
		print "========================="
		print "You do not have the 'git' client in your path. Install it, or sort your path out"
		sys.exit(-1)

	# check that the OS has wget installed
	if isToolInstalled("wget")==False:
		parser.print_help()
		print "========================="
		print "You do not have 'wget' in your path. Install it, or sort your path out"

	# check that the OS has md5sum installe
	if isToolInstalled("md5sum")==False:
		parser.print_help()
		print "========================="
		print "You do not have 'md5sum' in your path. Install it, or sort your path out"

	# if we get here then you deserve to execute the functionality
	doTheThing()
