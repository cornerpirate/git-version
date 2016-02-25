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
* git clone https://github.com/cornerpirate/git-version.git
* You will need to place "git-version.py" into your executable path.
* Modify your ~/.bashrc file to include the directory you just cloned.
* For example, if you cloned it to "/root/git-version" 
* Then add: "export PATH=$PATH:/root/Desktop/git-version/"
* Then refresh your terminal: source ~/.bashrc

If you can now type "git-version" to obtain the help page you have succeeded.

# Example Usage (Wordpress)
* Say your target site has left the license.txt file at the web root.
* download it: wget http://targetsite.com/license.txt
* By default that will save "license.txt" into your current directory
* clone the git repo for your target (in this case WordPress)
* git clone https://github.com/WordPress/WordPress.git
* This will create a directory "WordPress" in the current directory
* execute git-version as shown below:

<pre>
> git-version.py license.txt WordPress/
> Found git folder: WordPress/.git
> Checking that file license.txt exists in the repo within WordPress/
> 1)	./wp-includes/images/crystal/license.txt
> 2)	./wp-includes/js/swfupload/license.txt
> 3)	./wp-includes/js/plupload/license.txt
> 4)	./wp-includes/js/tinymce/license.txt
> 5)	./wp-includes/ID3/license.txt
> 6)	./wp-content/themes/twentyeleven/license.txt
> 7)	./wp-content/themes/twentyten/license.txt
> 8)	./license.txt
> 0) exit
> Multiple files in repo with that name. Enter a number: 8
> User chose path: ./license.txt
> Fetch URL: https://github.com/WordPress/WordPress.git
> Using URL: https://raw.githubusercontent.com/WordPress/WordPress/
> Getting MD5 hash for target file
> MD5(license.txt):b7d6694302f24cbe13334dfa6510fd02
> Checking log for license.txt
> =========================
> Match found!
> Raw URL: https://raw.githubusercontent.com/WordPress/WordPress/3c9a06672ebaec21847e4917e1086d9b9274ab6b/./license.txt
> Context URL: https://github.com/WordPress/WordPress/blob/3c9a06672ebaec21847e4917e1086d9b9274ab6b/./license.txt
> Found at 6 of 13 commits of that file 
> If it is '1 of 32' then you have the latest version of the file
>If it is '30 of 32' then you have a very early version of the file
</pre>

In this case the target license version was outdated!

Have fun with using this for more exciting web accessible files.

