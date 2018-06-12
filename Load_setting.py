import json, pprint
import codecs

with open('setting.json') as data_file:
    data = json.load(data_file)

with codecs.open("language\\"+"ko"+".json", 'r', 'utf-8-sig') as data_file:
    lang = json.load(data_file)

def langa(language):
    with codecs.open("language\\"+language+".json", 'r', 'utf-8-sig') as data_file:
        lang = json.load(data_file)

#print(data["bot"][0]["token"])
#print(data["bot"][1]["prefix"])
#print(lang["ko"][0])
#print(lang["ko"][1])