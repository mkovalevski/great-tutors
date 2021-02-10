from json import dumps, loads
from data import goals, teachers, emoji
# import pprint


dictionary = {'goals': goals, 'emoji': emoji, 'teachers': teachers}

with open('data.json', 'w') as f:
    f.write(dumps(dictionary))

with open('data.json', 'r') as f:
    contents = f.read()

contents = loads(contents)
# pprint.pprint(contents)
