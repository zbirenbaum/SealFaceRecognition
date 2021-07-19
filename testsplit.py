import traintestsplit as ttsplit

opensetprobes = ttsplit.create_split_probe_dict(dir='data/openset/Mitchell_Field_Singles_1_31Chips', startat=68)
print(opensetprobes)
