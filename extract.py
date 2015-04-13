from socket import timeout
import urllib2
import shutil
import logging
import re

# Setting up wanted resolution
resolution = "1920x1080"

# Setting up target folder
folder = "wallpaper"

# Setting up extract log file
file = open("extract.txt", "w")

# Setting up range you want to download
from_skip = 0 # http://www.vladstudio.com/fr/wallpapers/?skip=24 <= this is the skip value
to_skip = 480 # http://www.vladstudio.com/fr/wallpapers/?skip=24 <= this is the skip value

# Setting up first wallpaper ID on target folder
idWallpaper = 0

while (from_skip < to_skip):
    sock = urllib2.urlopen("http://www.vladstudio.com/fr/wallpapers/?skip={s}".format(s=from_skip))
    htmlSource = sock.read()
    sock.close()

    # Increment skip value
    from_skip+= 24

    # Regex expression
    re1='(<img class="framed" src=")'
    re2='.*?((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'

    # Finder iterator
    it = re.finditer(re1+re2, htmlSource)
    for match in it:
        url = g=match.group(2)
        url = url.replace("480x320", resolution);
        print "{g}".format(g=url, s=match.span())
        idWallpaper+= 1

        # Download wallpaper
        try:
            src = urllib2.urlopen(url, timeout=10)
        except (IOError) as error:
            logging.error('IOError URL: {url}'.format(url=url))
        except timeout:
            logging.error('Timeout URL: {url}'.format(url=url))
        else:
            dst = open("{f}/{id}.jpg".format(id=idWallpaper, f=folder), 'w');
            shutil.copyfileobj(src, dst)


        file.write(url+"\n")

file.close()
