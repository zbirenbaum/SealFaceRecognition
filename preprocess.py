import numpy as np
import scipy.misc as misc
from PIL import Image
from pdb import set_trace as bp

def preprocess(images, config, is_training=False):
    # Load images first if they are file paths
    if type(images[0]) == str:
        image_paths = images
        images = []
        assert (config.channels==1 or config.channels==3)
        mode = 'RGB' if config.channels==3 else 'I'
        print('Prepocessing images ...')
        for idx, image_path in enumerate(image_paths):
            images.append(misc.imread(image_path, mode=mode))
        print('Done preprocessing images ...\n')
            
        images = np.stack(images, axis=0) # a = b if true else 

    # Process images
    f = {
        'resize': resize,
        'random_crop': random_crop,
        'center_crop': center_crop,
        'random_flip': random_flip,
        'standardize': standardize_images,
        'random_downsample': random_downsample,
    }
    proc_funcs = config.preprocess_train if is_training else config.preprocess_test

    for name, args in proc_funcs:
        images = f[name](images, *args)
    if len(images.shape) == 3:
        images = images[:,:,:,None]
    return images

def get_new_shape(images, size):
    w, h = tuple(size)
    shape = list(images.shape)
    shape[1] = h
    shape[2] = w
    shape = tuple(shape)
    return shape

def random_crop(images, size):
    n, _h, _w = images.shape[:3]
    w, h = tuple(size)
    shape_new = get_new_shape(images, size)
    assert (_h>=h and _w>=w)

    images_new = np.ndarray(shape_new, dtype=images.dtype)

    y = np.random.randint(low=0, high=_h-h+1, size=(n))
    x = np.random.randint(low=0, high=_w-w+1, size=(n))

    for i in range(n):
        images_new[i] = images[i, y[i]:y[i]+h, x[i]:x[i]+w]

    return images_new

def center_crop(images, size):
    n, _h, _w = images.shape[:3]
    w, h = tuple(size)
    assert (_h>=h and _w>=w)

    y = int(round(0.5 * (_h - h)))
    x = int(round(0.5 * (_w - w)))

    images_new = images[:, y:y+h, x:x+w]

    return images_new

def random_flip(images):
    images_new = images
    flips = np.random.rand(images_new.shape[0])>=0.5
    
    for i in range(images_new.shape[0]):
        if flips[i]:
            images_new[i] = np.fliplr(images[i])

    return images_new

def resize(images, size):

    n, _h, _w = images.shape[:3]
    print('(n: {}, _h: {}, _w: {})'.format(n, _h, _w))
    w, h = tuple(size)
    shape_new = get_new_shape(images, size)

    images_new = np.ndarray(shape_new, dtype=images.dtype)
    print(images_new.shape)

    for i in range(n):
        images_new[i] = np.array(misc.imresize(images[i],(h,w)))

    return images_new

''' Normalize images to ensure pixels have a uniform data distribution for faster convergence while training the network '''
def standardize_images(images, standard):
    channels = 3 if images[0].shape == (112,112,3) else 1
    if standard=='mean_scale':
        mean = 127.5
        std = 128.0
    elif standard=='scale':
        mean = 0.0
        std = 255.0
    elif standard=='deb':
        if channels == 3:
            mean = np.mean(images,axis=(1,2,3)).reshape([-1,1,1,1])
            std = np.std(images, axis=(1,2,3)).reshape([-1,1,1,1])
        else:
            mean = np.mean(images,axis=(1,2)).reshape([-1,1,1,1])
            std = np.std(images, axis=(1,2)).reshape([-1,1,1,1])
    images_new = images.astype(np.float32)
    images_new = (images_new - mean) / std
    return images_new

''' Reduce overrepresented classes '''
def random_downsample(images, min_ratio):
    n, _h, _w = images.shape[:3]
    images_new = images
    ratios = min_ratio + (1-min_ratio) * np.random.rand(images_new.shape[0])

    for i in range(images_new.shape[0]):
        w = int(round(ratios[i] * _w))
        h = int(round(ratios[i] * _h))
        images_new[i,:h,:w] = misc.imresize(images[i], (h,w))
        images_new[i] = misc.imresize(images_new[i,:h,:w], (_h,_w))
        
    return images_new


