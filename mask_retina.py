from skimage import measure
from skimage.color import rgb2gray
from skimage.morphology import binary_erosion, binary_dilation, selem

from PIL import Image
import numpy as np
from os.path import split, join, splitext
from common import find_images


def create_mask(im_arr, erode=0):

    if im_arr.shape[2] == 3:
        im_arr = rgb2gray(im_arr)

    thresh = 0.05  # threshold_li(im_arr)
    inv_bin = np.invert(im_arr > thresh)
    all_labels = measure.label(inv_bin)

    # Select largest object and invert
    seg_arr = all_labels == 0

    if erode > 0:
        strel = selem.disk(erode, dtype=np.bool)
        seg_arr = binary_erosion(seg_arr, selem=strel)
    elif erode < 0:
        strel = selem.disk(abs(erode), dtype=np.bool)
        seg_arr = binary_dilation(seg_arr, selem=strel)

    return seg_arr.astype(np.bool)


def apply_mask(im, mask):

    im[np.invert(mask.astype(np.bool))] = 0
    return np.transpose(im, (1, 2, 0))


if __name__ == "__main__":

    import sys
    out_dir = sys.argv[2]

    for im_path in find_images(sys.argv[1]):

        im = np.asarray(Image.open(im_path))
        mask = create_mask(im).astype(np.uint8) * 255

        _, file_name = split(im_path)
        name, ext = splitext(file_name)

        Image.fromarray(mask).save(join(out_dir, name + '_mask.gif'))
