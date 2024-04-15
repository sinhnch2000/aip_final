import json
t = open(r"C:\Users\HP\Desktop\Capstone\data\raw\SGD1\val.json")
train = json.load(t)
for i in range(0,len(train)-2):
    if train[i]['id_dialogue'] != train[i+1]['id_dialogue']:
        train[i]['label'] = "NONE"

path_save = r'C:\Users\HP\Downloads\val_convert_int.json'
with open(path_save, 'w') as f:
  json.dump(train, f, indent=4)


