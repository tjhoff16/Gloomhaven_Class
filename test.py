import json

with open("class_cache.json", 'r') as f:
    class_dict = json.loads(f.read())
    for k,v in class_dict['classes'].items():
        print (k)
