import os
import sys
import json
import re

__author__          = "Jordan Matelsky"
__copyright__       = "Copyright 2015"
__credits__         = ["Jordan Matelsky", "Raghav Sood"]
__license__         = "CC"


if 1 <= len(sys.argv) > 3:
    print "Usage:\n    python parser.py [response_file [output_file]]\n" + \
          "After you have found thread_info.php in the Network tab of \n" +  \
          "Chrome Developer Tools, click on the Response tab and paste \n" + \
          "everything from that tab into a file `response_file`."
    sys.exit()

with open(sys.argv[1], "r") as response_file:
    response = response_file.read()

    # Response = curl 'https://www.facebook.com...' with all vars stored
    # in the string in many different ways. We've gotta pull them out...
    values = {}
    values["__user"] = re.search(r"user=(\w+)", response).group(1)
    values["cookie"] = re.search(r"'cookie: (.+?)'", response).group(1)
    values["__a"] = re.search(r"__a=(.+?)&", response).group(1)
    values["__dyn"] = re.search(r"__dyn=(.+?)&", response).group(1)
    values["__req"] = re.search(r"__req=(.+?)&", response).group(1)
    values["fb_dtsg"] = re.search(r"fb_dtsg=(.+?)&", response).group(1)
    values["ttstamp"] = re.search(r"ttstamp=(.+?)&", response).group(1)
    values["__rev"] = re.search(r"__rev=(.+?)'", response).group(1)


    output_file ="_response_values"
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
   
    with open(output_file, 'w') as export:
        for (i, v) in values.iteritems():
            export.write(i + "\n" + v + "\n\n")

