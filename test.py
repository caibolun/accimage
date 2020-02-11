#!/usr/bin/env python
# coding=utf-8
'''
@Author: ArlenCai
@Date: 2020-01-16 00:35:35
@LastEditTime : 2020-02-11 16:48:32
'''
import accimage
import numpy as np
import imageio
import os
import ctypes

ACCIMAGE_SAVE = os.environ.get('ACCIMAGE_SAVE', '')
if len(ACCIMAGE_SAVE) and ACCIMAGE_SAVE.lower() not in {'0', 'false', 'no'}:
    SAVE_IMAGES = True
else:
    SAVE_IMAGES = False

def image_to_np(image):
    """
    Returns:
        np.ndarray: Image converted to array with shape (width, height, channels)
    """
    image_np = np.empty([image.channels, image.height, image.width], dtype=np.uint8)
    image.copyto(image_np)
    image_np = np.transpose(image_np, (1, 2, 0))
    return image_np


def save_image(path, image):
    imageio.imwrite(path, image_to_np(image))


def test_reading_image():
    image = accimage.Image("chicago.jpg")
    save_image('test_reading_image.jpg', image)
    assert image.width == 1920
    assert image.height == 931


def test_resizing():
    image = accimage.Image("chicago.jpg")

    image.resize(size=(200, 200))
    if SAVE_IMAGES:
        save_image('test_resizing.jpg', image)

    assert image.width == 200
    assert image.height == 200

def test_cropping():
    image = accimage.Image("chicago.jpg")

    image.crop(box=(50, 50, 150, 150))
    if SAVE_IMAGES:
        save_image('test_cropping.jpg', image)

    assert image.width == 100
    assert image.height == 100

def test_flipping():
    image = accimage.Image("chicago.jpg")
    original_image_np = image_to_np(image)

    FLIP_LEFT_RIGHT = 0
    image.transpose(FLIP_LEFT_RIGHT)
    if SAVE_IMAGES:
        save_image('test_flipping.jpg', image)

    new_image_np = image_to_np(image)
    assert image.width == 1920
    assert image.height == 931
    np.testing.assert_array_equal(new_image_np[:, ::-1, :], original_image_np)

def test_buffer():
    with open("chicago.jpg", "rb") as fp:
        buf = np.frombuffer(fp.read(), np.uint8)
        image = accimage.Image(buf)
        save_image('test_buffer.jpg', image)
if __name__ == "__main__":
    test_buffer()

