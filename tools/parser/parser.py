# coding=utf8

import os, glob, json, re
from pathlib import Path

input_dir = 'input'
output_dir = 'output'

if not os.path.exists(output_dir):
    print("Drag logs into input directory to parse")
    os.makedirs(output_dir)
    os.makedirs(input_dir)

for filename in glob.glob(os.path.join(input_dir, '*.log')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f:
        regex = r"^\[(?P<time>[0-9:]*)\]\s(?P<username>.*)\s\((?P<uid>\d*)\)\:\s(?P<message>.*)$"
        matches = re.finditer(regex, f.read(), re.MULTILINE)

        fname = Path(os.path.basename(filename)).stem
        
        file = open("{dir}\\{filename}.json".format(dir=output_dir,filename=fname), 'w', encoding='utf8')
        blob = []

        for match in matches:
            time = match.group('time')
            username = match.group('username')
            uid = match.group('uid')
            message = match.group('message')


            blob += [{"time": time, "username": username, "uid": uid, "message": message}]


        json.dump(blob, file, ensure_ascii=False)

        file.close()
print("done")