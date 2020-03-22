import cmath
import os.path
import random
import timeit
from datetime import datetime
from multiprocessing import Pool
from time import sleep
from typing import Tuple

import matplotlib.path
import numpy as np
from PIL import Image

from config import *


def _get_random_rectangle() -> matplotlib.path.Path:
    """
    Return a rectangle with random length, width and orientation, restricted by the configuration
    """

    # Get a rectangle without rotation with center at (0,0)
    random_length = random.uniform(MIN_LENGTH, MAX_LENGTH)
    random_width = random.uniform(MIN_WIDTH, MAX_WIDTH)
    p1 = complex(-random_length / 2, -random_width / 2)
    p2 = complex(random_length / 2, -random_width / 2)
    p3 = complex(random_length / 2, random_width / 2)
    p4 = complex(-random_length / 2, random_width / 2)

    # Rotate the coordinates over a random angle
    random_angle = random.uniform(0, cmath.pi * 2)
    p1 = _rotate_point(p1, random_angle)
    p2 = _rotate_point(p2, random_angle)
    p3 = _rotate_point(p3, random_angle)
    p4 = _rotate_point(p4, random_angle)

    # Shift the polygon such that it is on the screen
    polygon = [p1, p2, p3, p4]
    min_x = min([p.real for p in polygon])
    max_x = max([p.real for p in polygon])
    min_y = min([p.imag for p in polygon])
    max_y = max([p.imag for p in polygon])
    if ALL_RECTANGLES_FULLY_ON_CANVAS:
        shift_in_x = random.uniform(-min_x, CANVAS_SIZE - max_x)
        shift_in_y = random.uniform(-min_y, CANVAS_SIZE - max_y)
    else:
        shift_in_x = random.uniform(0, CANVAS_SIZE)
        shift_in_y = random.uniform(0, CANVAS_SIZE)
    p1 = p1 + complex(shift_in_x, shift_in_y)
    p2 = p2 + complex(shift_in_x, shift_in_y)
    p3 = p3 + complex(shift_in_x, shift_in_y)
    p4 = p4 + complex(shift_in_x, shift_in_y)

    # Return the rectangle as a polygon (Path object)
    polygon = [(p.real, p.imag) for p in (p1, p2, p3, p4)]
    bb_path = matplotlib.path.Path(np.array(polygon))
    return bb_path


def _rotate_point(point: complex, angle: float) -> complex:
    r, phi = cmath.polar(point)
    return cmath.rect(r, phi + angle)


polygons = [_get_random_rectangle() for _ in range(NR_RECTANGLES)]


def _nr_polygons_containing_pixel_function(point: Tuple[int, int]):
    return np.sum([polygon.contains_point(point) for polygon in polygons])


def _now() -> str:
    """
    Return the current date and timestamp in second precision
    """

    return datetime.now().strftime('%y%m%d%H%M%S')


def draw_canvas(nr_processes: int = 10) -> Image:
    points = [(x, y) for x in range(CANVAS_SIZE) for y in range(CANVAS_SIZE)]
    with Pool(nr_processes) as pool:
        nr_polygons_containing_pixel = pool.map(_nr_polygons_containing_pixel_function, points)

    pixel_data = [
        (0, 0, 0) if count % 2 == 1 else (255, 255, 255)
        for count in nr_polygons_containing_pixel
    ]

    img = Image.new('RGB', (CANVAS_SIZE, CANVAS_SIZE), 'white')
    img.putdata(pixel_data)
    return img


def save_img(img: Image):
    """
    Save the image to the image directory with a predefined filename, based on the current timestamp
    """

    # The abspath is necessary in order to be able to run the code as a module
    src_dir: str = os.path.abspath(os.path.dirname(__file__))
    root_dir: str = os.path.dirname(src_dir)
    img_dir: str = os.path.join(root_dir, 'img')

    filename = f'alternate_filling_{_now()}.png'
    full_path = os.path.join(img_dir, filename)
    img.save(full_path)


def draw_multiple_images(nr_images: int = 1, nr_processes: int = 10):
    for _ in range(nr_images):
        start_time = _now()
        img = draw_canvas(nr_processes)
        save_img(img)
        # while _now() == start_time:
        # Since we have seconds in the filename, we shouldn't continue
        # drawing the next earthquake until the second is over
        # sleep(0.01)


if __name__ == '__main__':
    for nr_processes in list(range(1, 11)) + list(range(15, 41, 5)):
        def run():
            return draw_multiple_images(nr_images=1, nr_processes=nr_processes)

        print(nr_processes, timeit.timeit(run, number=5))
