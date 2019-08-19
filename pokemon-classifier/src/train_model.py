from fastai import ImageDataBunch

from model import ConvNeuralNet

data = ImageDataBunch.from_csv(planet, folder='train', size=128, suffix='.jpg', label_delim=' ',
    ds_tfms=get_transforms(flip_vert=True, max_lighting=0.1, max_zoom=1.05, max_warp=0.))