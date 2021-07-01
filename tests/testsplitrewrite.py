import splitrewrite2 as sp
#import generatesets as gs

sp1 = sp.DataSplitter(photodir='photos', kfold=5, openset=True)
sp1.printtrainsetbyfold()

#gs
