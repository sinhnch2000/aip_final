
import json

# Opening JSON file
f = open(r'C:\Users\HP\Downloads\train_schema.json')
b = open(r'C:\Users\HP\Downloads\dev_schema.json')
t = open(r'C:\Users\HP\Downloads\test_schema.json')
# returns JSON object as
# a dictionary
train = json.load(f)
dev = json.load(b)
test = json.load(t)
output = dict()
c = open(r'C:\Users\HP\Downloads\schema.json')
fuse = json.load(c)
for i in fuse:
  domain = i["service_name"].lower()


  for y in i["intents"]:
    intent = y["name"]
    des = y["description"]
    reqSlot = []
    for slot in y['required_slots']:
      reqSlot.append(slot)
    des_dict = dict()
    des_dict[des] = reqSlot
    if domain not in output:
      output[domain] = {}
    output[domain][intent] = des_dict

for i in test:
  domain = i["service_name"].lower()

  for y in i["intents"]:
    intent = y["name"]
    des = y["description"]
    reqSlot = []
    for slot in y['required_slots']:
      reqSlot.append(slot)
    des_dict = dict()
    des_dict[des] = reqSlot
    intent_dict = dict()
    intent_dict[intent] = des_dict
    output.__setitem__(domain, intent_dict)

for i in dev:
  domain = i["service_name"].lower()

  for y in i["intents"]:
    intent = y["name"]
    des = y["description"]
    reqSlot = []
    for slot in y['required_slots']:
      reqSlot.append(slot)
    des_dict = dict()
    des_dict[des] = reqSlot
    if domain not in output:
      output[domain] = {}
    output[domain][intent] = des_dict
for i in train:
  domain = i["service_name"].lower()

  for y in i["intents"]:
    intent = y["name"]
    des = y["description"]
    reqSlot = []
    for slot in y['required_slots']:
      reqSlot.append(slot)
    des_dict = dict()
    des_dict[des] = reqSlot
    if domain not in output:
      output[domain] = {}
    output[domain][intent] = des_dict
path_save = r'C:\Users\HP\Downloads\intent_schema.json'
with open(path_save, 'w') as f:
  json.dump(output, f, indent=4)





