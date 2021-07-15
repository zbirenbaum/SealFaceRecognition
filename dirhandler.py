import os
def get_photos_in_dir(path):
    
    extensions = ('png', 'jpg', 'jpeg')
    photolist = [
            str(path) + '/' + filename for filename in os.listdir(path) \
                    if filename.endswith(extensions) \
                    and not filename.startswith('.')]
    return photolist



def get_photo_dirs(path, exclude):
    pathlist = []
    photos_in_dir = get_photos_in_dir(path)
    if len(photos_in_dir) >= exclude:
        return [path]
    else:
        entries = os.listdir(str(path))
        for entry in entries:
            entrypath = path + '/' + entry
            if not entry.startswith(".") and os.path.isdir(entrypath):
                result = get_photo_dirs(entrypath, exclude)
                pathlist.extend(result)
            else:
                continue
    return pathlist

def gen_dict(folderdir, exclude=None):
    if exclude is None:
        exclude=1
    photodirpaths = get_photo_dirs(folderdir, exclude)
#    print(photodirpaths)
    mapdict = {}
    counter = 0
    for path in photodirpaths:
        photos = get_photos_in_dir(path)
        mapdict[counter] = {'name': path, 'photos': photos}
        counter = counter + 1

    return mapdict

#print(gen_dict('2020data',5).keys())

