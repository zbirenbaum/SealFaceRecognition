import splitrewrite2 as sp

sp1 = sp.DataSplitter(photodir='photos', kfold=5, openset=True)
sp1.printtrainsetbyfold()
