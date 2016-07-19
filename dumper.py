import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO
import re
import sys
content = sys.stdin.read()

header_info = {}
header_info['cookie'] = re.search('cookie:(.*)\n', content).group(1)
header_info['user'] = re.search('__user:(.*)\n', content).group(1)
header_info['__a'] = re.search('__a:(.*)\n', content).group(1)
header_info['__dyn'] = re.search('__dyn:(.*)\n', content).group(1)
header_info['__req'] = re.search('__req:(.*)\n', content).group(1)
header_info['fb_dtsg'] = re.search('fb_dtsg:(.*)\n', content).group(1)
header_info['ttstamp'] = re.search('ttstamp:(.*)\n', content).group(1)
header_info['__rev'] = re.search('__rev:(.*)\n', content).group(1)

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
    print "Usage:\n     python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
    print "Example conversation with Raghav Sood"
    print " python dumper.py 1075686392 2000 0"
    sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
timestamp = int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {
    "origin": "https://www.facebook.com",
    "accept-encoding": "gzip,deflate",
    "accept-language": "en-US,en;q=0.8",
    "cookie": header_info['cookie'],
    "pragma": "no-cache",
    "user-agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "cache-control": "no-cache",
    "referer": "https://www.facebook.com/messages/zuck"
}

base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"

try:
    os.makedirs(directory)
except OSError:
    pass # already exists

try:
    os.makedirs(pretty_directory)
except OSError:
    pass # already exists

while end_mark not in messages_data:

    data_text = {
        "messages[user_ids][" + str(talk) + "][offset]": str(offset),
        "messages[user_ids][" + str(talk) + "][limit]": str(limit),
        "messages[user_ids]["+ str(talk) + "][timestamp]": str(timestamp),
        "client": "web_messenger"
        # "__user": "678098123",  # fill POST form values
        # "__a": "1",
        # "__dyn": "7AzkXh8Z398jgDxKy1l0BwRyaF3oyfJLFwgoqwWhEoyUnwgU9GGEcVovkwy3eE99XDG4UiwExW14DwPxSFEW2O9xicG4EnwkUC9z8Kew",
        # "__req": "c",
        # "fb_dtsg": "AQEXZ88yyvpL:AQGGE92I6xw9",
        # "ttstamp": "265816988905656121121118112765865817171695750735412011957",
        # "__rev": "2333461"
    }

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!
    data_text.update(header_info)

    data = urllib.urlencode(data_text)
    url = "https://www.facebook.com/ajax/mercury/thread_info.php"

    print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    compressed = StringIO.StringIO(response.read())
    decompressedFile = gzip.GzipFile(fileobj=compressed)


    outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
    messages_data = decompressedFile.read()
    messages_data = messages_data[9:]
    json_data = json.loads(messages_data)
    if json_data is not None and json_data['payload'] is not None:
        try:
            messages = json_data['payload']['actions'] + messages
            timestamp = int(json_data['payload']['actions'][0]['timestamp']) - 1
        except KeyError:
            pass #no more messages
    else:
        print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
        print "Data Dump:"
        print json_data
        time.sleep(error_timeout)
        continue
    outfile.write(messages_data)
    outfile.close()
    command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
    os.system(command)
    offset = offset + limit
    time.sleep(general_timeout)

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
