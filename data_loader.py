import os
import logging
import h5py
import numpy as np

logging.basicConfig(filename='loader.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

class BatchIterator:
    def __init__(self, 
                 file, 
                 batch_size,
                 epochs,
                 shuffle=True):
        self._batch_size = batch_size
        self._file = file
        self._epochs = epochs
        self._shuffle = shuffle
        self._imgs = []
        self._masks = []
        self._names = []

        """read dataset """
        if os.path.exists(self._file):
            with h5py.File(self._file, 'r') as hf:
                self._size = len(hf.keys())
                for key in hf.keys():
                    sample = hf[key]
                    img = np.array(sample['img'])
                    mask = np.array(sample['mask'])
                    self._names.append(sample.name[1:])
                    self._imgs.append(img)
                    self._masks.append(mask)
        else: 
            logging.warning(self._file + ' does not exist ! ')
            self._size = 0

        """ initialized status """
        self._num_batches_per_epoch = int((self._size - 1)/self._batch_size) + 1
        self._current_epoch = 0
        self._current_batch = 0

    def next(self):
        """Generates a batch for a dataset."""
        if (self._current_epoch < self._epochs):
            # Shuffle the data each time
            shuffle_indices = np.arange(self._size)
            if self._shuffle:
                shuffle_indices = np.random.permutation(shuffle_indices)

            start_index = self._current_batch * self._batch_size
            end_index = min((self._current_batch + 1) * self._batch_size, self._size)

            # Generates a batch
            print('generating batch '+ str(self._current_batch + 1) +  ' of epoch ' + str(self._current_epoch + 1))

            batch_indices = sorted(list(shuffle_indices[start_index:end_index]))
            batch = {}
            batch['name'] = []
            batch['img'] = []
            batch['mask'] = []
            for b in batch_indices:
                batch['name'].append(self._names[b])
                batch['img'].append(self._imgs[b])
                batch['mask'].append(self._masks[b])

            # update status
            if (self._current_batch < self._num_batches_per_epoch):
                self._current_batch += 1
            if (self._current_batch == self._num_batches_per_epoch):
                self._current_epoch += 1
                self._current_batch = 0

            return batch
        else:
            return None

            

            


