import sys
import os
import numpy as np
import imp
import math
import random
from datetime import datetime
import shutil
from preprocess import preprocess
from multiprocessing import Process, Queue

def import_file(full_path_to_module, name='module.name'):
    if full_path_to_module is None:
        print('Configuration file not added as an argument')
        sys.exit(1)
    if not os.path.isfile(full_path_to_module):
        print('{} does not exist. Please check.'.format(full_path_to_module))
        sys.exit(1)
    module_obj = imp.load_source(name, full_path_to_module)
    
    return module_obj

def create_log_dir(config, config_file, name):
    subdir = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    log_dir = os.path.join(os.path.expanduser(config.log_base_dir), name, subdir)
    if not os.path.isdir(log_dir):  # Create the log directory if it doesn't exist
        os.makedirs(log_dir)
    shutil.copyfile(config_file, os.path.join(log_dir,'config.py'))

    return log_dir

class DataClass():
    def __init__(self, class_name, indices, label):
        self.class_name = class_name
        self.indices = list(indices) # indices of images with this label
        self.label = label
        return

    def get_samples(self, num_samples_per_class, exception=None):
        indices_temp = self.indices[:]
        if exception is not None:
            indices_temp.remove(exception)
        indices = []
        iterations = int(np.ceil(1.0*num_samples_per_class / len(indices_temp)))#type: ignore
        # iterations = 1

        counter = 0
        while counter < iterations:
            sample_indices = np.random.permutation(indices_temp)#type: ignore
            indices.append(sample_indices)
            counter = counter + 1
        indices = np.concatenate(indices, axis=0)[:num_samples_per_class]
        # indices = indices[:min(indices.size, num_samples_per_class)]
        return indices

    def build_clusters(self, cluster_size):
        permut_indices = np.random.permutation(self.indices)#type: ignore
        cutoff = (permut_indices.size // cluster_size) * cluster_size
        clusters = np.reshape(permut_indices[:cutoff], [-1, cluster_size])
        clusters = list(clusters)
        if permut_indices.size > cutoff:
            last_cluster = permut_indices[cutoff:]
            clusters.append(last_cluster)
        return clusters

    def cutoff_samples(self, num_samples):
        cutoff = min(len(self.indices), num_samples)
        self.indices = self.indices[:cutoff]

class Dataset():

    def __init__(self, ddict=None, path=None):
        self.traindict = None
        self.testdict = None
        self.total_num_classes = None
        self.training_num_classes = None
        self.classes = None
        self.images = None
        self.labels = None
        self.index_queue = None
        self.queue_idx = None
        self.cluster_queue = None
        self.cluster_queue_idx = None
        self.batch_queue = None
        self.class_weights = None
        self.set_list = None

        if path is not None:
            self.images, self.labels, self.total_num_classes, self.set_list = self.init_from_path(path)
            self.images = np.array(self.images, dtype=np.object)
        
        if ddict is not None:
            self.images, self.labels, self.total_num_classes, self.set_list = init_from_dict(ddict)
            self.images = np.array(self.images, dtype=np.object)
            self.labels = np.array(self.labels, dtype=np.int32)
            self.init_classes()
        
        print(self.labels)

    def clear(self):
        del self.classes
        self.__init__()

    # Create the training set by specifying 
    def init_from_path(self, path):
        path = os.path.expanduser(path)
        imagelist = []
        labels = []
        set_list = []
        
        for sealId in os.listdir(path):
            sealPath = os.path.join(path, sealId)
            for photo in os.listdir(sealPath):
                photoPath = os.path.join(sealPath, photo)
                if photo.endswith(('.jpg', '.jpeg', '.png')):
                    labels.append(sealId)
                    imagelist.append(str(photoPath))
                    set_list.append(photoPath + " " + sealId)
        return imagelist, labels, len(set(labels)), set_list

    def init_from_list(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        lines = [line.strip().split(' ') for line in lines]
        assert len(lines)>0 and len(lines[0])==2
        self.total_num_classes = max(int(line[1]) for line in lines)
        lines = lines[1:] #start at index 1
        images = [line[0] for line in lines]
        labels = [int(line[1]) for line in lines]
        self.images = np.array(images, dtype=np.object)
        self.labels = np.array(labels, dtype=np.int32)
        self.init_classes()



    def init_classes(self):
        dict_classes = {}
        classes = []
        for i, label in enumerate(self.labels):#type: ignore
            if not label in dict_classes:
                dict_classes[label] = [i]
            else:
                dict_classes[label].append(i)
        for label, indices in dict_classes.items():
            classes.append(DataClass(str(label), indices, label))
        self.classes = np.array(classes, dtype=np.object)
        self.training_num_classes = len(classes)
       
    def init_index_queue(self, random=True):
        size = self.images.shape[0] #type: ignore
        if random:
            self.index_queue = np.random.permutation(size) #type: ignore
        else:
            self.index_queue = np.arange(size)
        self.queue_idx = 0

    def pop_index_queue(self, num, random=True):
        if self.index_queue is None:
            self.init_index_queue(random)
        result = []
        while num >= len(self.index_queue) - self.queue_idx:#type: ignore
            result.extend(self.index_queue[self.queue_idx:])#type: ignore
            num -= len(self.index_queue) - self.queue_idx#type: ignore
            self.init_index_queue(random)
            self.queue_idx = 0
        result.extend(self.index_queue[self.queue_idx : self.queue_idx+num])#type: ignore
        self.queue_idx += num
        return result

    def init_cluster_queue(self, cluster_size):
        assert type(cluster_size) == int
        self.cluster_queue = []
        for dataclass in self.classes:#type: ignore
            self.cluster_queue.extend(dataclass.build_clusters(cluster_size))
        random.shuffle(self.cluster_queue)
    
        self.cluster_queue = [idx for cluster in self.cluster_queue for idx in cluster]
        self.cluster_queue_idx = 0

        
    def pop_cluster_queue(self, num_clusters, cluster_size):
        if self.cluster_queue is None:
            self.init_cluster_queue(cluster_size)
        result = []
        while num_clusters >= len(self.cluster_queue) - self.cluster_queue_idx:#type: ignore
            result.extend(self.cluster_queue[self.cluster_queue_idx:])#type: ignore
            num_clusters -= len(self.cluster_queue) - self.cluster_queue_idx#type: ignore
            self.init_cluster_queue(cluster_size)
        result.extend(self.cluster_queue[self.cluster_queue_idx : self.cluster_queue_idx+num_clusters])#type: ignore
        self.cluster_queue_idx += num_clusters
        return result

    def get_batch(self, batch_size):
        indices_batch = self.pop_index_queue(batch_size, True)

        image_batch = self.images[indices_batch]#type: ignore
        label_batch = self.labels[indices_batch]#type: ignore
        return image_batch, label_batch

    def get_batch_classes(self, batch_size, num_classes_per_batch):
        # classes_batch = np.random.permutation(self.training_num_classes)[:num_classes_per_batch]
        # classes_batch = self.sample_classes_by_weight(num_classes_per_batch)

        #indices_root = self.pop_index_queue(num_classes_per_batch)
        #classes_batch = self.labels[indices_root]

        assert batch_size % num_classes_per_batch == 0
        num_samples_per_class = int(batch_size / num_classes_per_batch)

        indices_batch = self.pop_cluster_queue(batch_size, num_samples_per_class)

        #ndices_batch = [indices_root]
        #for i, class_id in enumerate(classes_batch):
        #    indices_batch.append(self.classes[class_id].get_samples(num_samples_per_class, indices_root[i]))
           
        # indices_batch = np.concatenate(indices_batch, axis=0)
        image_batch = self.images[indices_batch]#type: ignore
        label_batch = self.labels[indices_batch]#type: ignore
        return image_batch, label_batch

   # Multithreading preprocessing images
    def start_batch_queue(self, config, is_training, maxsize=16, num_threads=1): 
        self.batch_queue = Queue(maxsize=maxsize)
        def batch_queue_worker():
            while True:
                if config.template_batch:
                    image_path_batch, label_batch = \
                        self.get_batch_classes(config.batch_size, config.num_classes_per_batch)
                else:
                    image_path_batch, label_batch = self.get_batch(config.batch_size)
                image_batch = preprocess(image_path_batch, config, is_training)
                self.batch_queue.put((image_batch, label_batch))#type: ignore

        for i in range(num_threads):
            worker = Process(target=batch_queue_worker)
            worker.daemon = True
            worker.start()
    
    
    def pop_batch_queue(self):
        batch = self.batch_queue.get(block=True, timeout=60)#type: ignore
        return batch

def init_from_dict(ddict):
    imagelist = []
    labels = []
    set_list = []

    total_num_classes = len(ddict.keys())
    for i, key in enumerate(ddict.keys()):
        for photopath in ddict[key]:
            labels.append(i)
            imagelist.append(str(photopath))
            set_list.append(photopath + " " + str(key))
    return imagelist, labels, total_num_classes, set_list

# Calulate the shape for creating new array given (w,h)
''' Run various functions as defined in the config preprocess '''
def get_updated_learning_rate(global_step, config):
    if config.learning_rate_strategy == 'step':
        max_step = -1
        learning_rate = 0.0
        for step, lr in config.learning_rate_schedule.items():
            if global_step >= step and step > max_step:
                learning_rate = lr
                max_step = step
        if max_step == -1:
            raise ValueError('cannot find learning rate for step %d' % global_step)
    elif config.learning_rate_strategy == 'cosine':
        initial = config.learning_rate_schedule['initial']
        interval = config.learning_rate_schedule['interval']
        end_step = config.learning_rate_schedule['end_step']
        step = math.floor(float(global_step) / interval) * interval
        assert step <= end_step
        learning_rate = initial * 0.5 * (math.cos(math.pi * step / end_step) + 1)
    return learning_rate#type: ignore

''' Used to show information while training the network '''
def display_info(epoch, step, duration, watch_list):
    sys.stdout.write('[%d][%d] time: %2.2f' % (epoch+1, step+1, duration))
    for item in watch_list.items():
        if type(item[1]) in [np.float32, np.float64]:
            sys.stdout.write('   %s: %2.3f' % (item[0], item[1]))
        elif type(item[1]) in [np.int32, np.int64, np.bool]:
            sys.stdout.write('   %s: %d' % (item[0], item[1]))
    sys.stdout.write('\n')


