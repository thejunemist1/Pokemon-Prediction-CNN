from fastai import ImageDataBunch
from model import ConvNeuralNet
from fastai.vision import *

import os


HIDDEN_SIZE = 128
BATCH_SIZE = 64
LINEAR_SIZE = 1024
PIXEL_SIZE = 160
test_path = "/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/test/"
train_path = '/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/train'

def get_num_class(path):
    """
    Gives a list of the jpg files in the path directory.
    :param path: path of the directory to look into.
    :return: List of all the files.
    """
    file_count = 0
    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                file_count = + 1
    return file_count


if __name__ == "__main__":

    data = ImageDataBunch.from_csv(train_path, 'poke_file_labels.csv', folder='train', size=BATCH_SIZE, suffix='.jpg', label_delim=' ',
        ds_tfms=get_transforms(flip_vert=True, max_lighting=0.1, max_zoom=1.05, max_warp=0.)) # figure out scaling here from get_transforms(desired size =160x160)
    # figure out how to get num_classes from data - maybe read the csv to get num classes
    num_class = get_num_class(test_path)
    model = ConvNeuralNet(PIXEL_SIZE, HIDDEN_SIZE, BATCH_SIZE, LINEAR_SIZE, num_class)

