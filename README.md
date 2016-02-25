# git-version - Find out what version of the file you have compared to the github.com repository

In penetration testing we often come across web sites which may attempt to mask their version information.
The question this answers is "how can I be certain about the version of the site my target is running?".
There are various tools which do this very well already. 

When I had a thought about how powerful the git command is I realised we could use it to pinpoint the exact version
of a file.

# Pre-requisites
* Tested only on linux (specifically Kali linux)
* Make sure that the OS has; wget, git (client), and md5sum installed (script checks path before running)
* Your target must host its source code on github.com publicly.
* Future might support other providers so long as gitweb is ENABLED.

# Installation 
* `git clone https://github.com/cornerpirate/git-version.git`
* You will need to place "git-version.py" into your executable path.
* Modify your ~/.bashrc file to include the directory you just cloned.
* For example, if you cloned it to `/root/git-version` 
* Then add: `export PATH=$PATH:/root/Desktop/git-version/`
* Then refresh your terminal: `source ~/.bashrc`

If you can now type "git-version" to obtain the help page you have succeeded.

# Example Usage (Wordpress)
* Say your target site has left the license.txt file at the web root.
* download it: `wget http://targetsite.com/license.txt`
* By default that will save "license.txt" into your current directory
* clone the git repo for your target (in this case WordPress)
* `git clone https://github.com/WordPress/WordPress.git`
* This will create a directory "WordPress" in the current directory
* execute git-version as shown below:

<pre>
git-version.py license.txt WordPress/
1)	./wp-includes/images/crystal/license.txt
2)	./wp-includes/js/swfupload/license.txt
3)	./wp-includes/js/plupload/license.txt
4)	./wp-includes/js/tinymce/license.txt
5)	./wp-includes/ID3/license.txt
6)	./wp-content/themes/twentyeleven/license.txt
7)	./wp-content/themes/twentyten/license.txt
8)	./license.txt
0) exit
Multiple files in repo with that name. Enter a number: 8
Found at [6/13]: https://github.com/WordPress/WordPress/blob/3c9a06672ebaec21847e4917e1086d9b9274ab6b/./license.txt
</pre>

In this case the target license version was outdated!

# Enumerating a target site

You need to find web servable files such as; `*.txt`, `*.inc`, `*.js`, `*.css`, `*.png`, `*.gif` etc
The only thing that is important is that the content you download is not dynamically generated. You will
get nowhere if you are trying to find "php" files etc.

Bit of an explanation on the reasoning of the file choices:

* txt files - are good for licenses, and readme files. The license should let you find the YEAR the target was updated.
* js files - can change more frequently for sites relying on heavy use of js.
* image files - can change in minor ways across versions.

You need to locate a list of files to retrive from your target, and then download the files. To do this:
* `cd WordPress` # get into the cloned repository
* `find . -name '*.txt' >> ./txt-files.txt` # locate files from the current dir with the name *.txt and save each result
* `find . -name '*.inc' >> ./inc-files.txt` # same for inc files
* repeat for any other file extensions that you know will work.
* `cd ..` # get yourself back to a directory outside your local git repo folder
* Use a bash for loop to download every file possible from your target site:
<pre>
for i in `cat txt-files.txt`; do wget https://targetsite/$i; done
</pre>
* some files may have been removed by a crafty admin removing "unnecessary content". Ignore the 404s
* your current directory should be full of many *.txt files
* Use a bash for loop to then run git-version against each file
<pre>
for f in `ls -a *.txt | cat`; do git-version.py $f WordPress/; done
</pre>

# Dislaimer

For research purposes only, do not use this on any target which you do not have permission to do so.
