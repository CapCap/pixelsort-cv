import logging
import cv2
import imutils
import numpy as np

from pixelsortcv.util import crop_to
from pixelsortcv.sorter import sort_image
from pixelsortcv.constants import DEFAULTS
from pixelsortcv.interval import choices as interval_choices
from pixelsortcv.sorting import choices as sorting_choices


def pixelsort(
        image,
        mask_image=None,
        interval_image=None,
        randomness=DEFAULTS["randomness"],
        clength=DEFAULTS["clength"],
        sorting_function=DEFAULTS["sorting_function"],
        interval_function=DEFAULTS["interval_function"],
        lower_threshold=DEFAULTS["lower_threshold"],
        upper_threshold=DEFAULTS["upper_threshold"],
        angle=DEFAULTS["angle"]
):
    original_size = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    mask_image = mask_image if mask_image else np.ones(image.shape)
    if angle and angle != 0:
        image = imutils.rotate(image, angle)
        mask_image = imutils.rotate(mask_image, angle)
        interval_image = imutils.rotate(interval_image, angle)

    logging.debug("Determining intervals...")
    intervals = interval_choices[interval_function](
        image,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        clength=clength,
        interval_image=interval_image,
    )
    logging.debug("Sorting pixels...")
    sorted_pixels = sort_image(
        image.shape,
        image,
        mask_image,
        intervals,
        randomness,
        sorting_choices[sorting_function])

    output_img = _place_pixels(sorted_pixels, mask_image, image, image.shape)
    if angle and angle != 0:
        output_img = imutils.rotate(output_img, -angle)
        # output_img = crop_to(output_img, original_size)

    return output_img


def _place_pixels(pixels, mask, original, size):
    output_img = np.ones(size)
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if not mask[x][y] > 0:
                output_img[x][y] = original[x, y]
            else:
                output_img[x][y] = pixels[y][count]
                count += 1
    return output_img
