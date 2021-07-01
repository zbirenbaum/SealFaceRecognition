import databuilder as db
#import pandas as pd
db1 = db.DataBuilder("photos")
#print(str(db1.get_photos().get_photo_names()) + " " + str(db1.get_photos().get_photo_paths()))
print(str(db1.get_photos_by_index(0)))
#frame = db1.frame
#subset = frame.loc[:,['paths','photos']]
#for row in subset.index:
#    line = subset.loc[row]
#    lpath = len(line['paths'])
#    lphoto = len(line['photos'])
#    print(str(lpath) + " " + str(lphoto))

#print(frame)
#print(db1.frame)
