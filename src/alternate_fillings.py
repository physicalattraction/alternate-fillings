import cmath
import os.path
import random
from datetime import datetime
from time import sleep

import matplotlib.path
import numpy as np
from PIL import Image, ImageDraw

from config import *


def now() -> str:
    """
    Return the current date and timestamp in second precision
    """

    return datetime.now().strftime('%y%m%d%H%M%S')


class AlternateFilling:
    src_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(src_dir)
    img_dir = os.path.join(root_dir, 'img')

    width: int
    height: int
    img: Image
    draw: ImageDraw

    def __init__(self):
        self.width = CANVAS_SIZE
        self.height = CANVAS_SIZE
        self.img = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def draw_multiple_images(nr_images: int = 1):
        for _ in range(nr_images):
            start_time = now()
            alternate_filling = AlternateFilling()
            alternate_filling.draw_canvas()
            alternate_filling.save_img()
            while now() == start_time:
                # Since we have seconds in the filename, we shouldn't continue
                # drawing the next earthquake until the second is over
                sleep(0.01)

    def draw_canvas(self):
        polygons = [self._get_random_rectangle() for _ in range(NR_RECTANGLES)]
        nr_polygons_containing_pixel = [
            np.sum([polygon.contains_point((x, y)) for polygon in polygons])
            for x in range(self.width)
            for y in range(self.height)
        ]
        pixel_data = [
            (0, 0, 0) if count % 2 == 1 else (255, 255, 255)
            for count in nr_polygons_containing_pixel
        ]
        self.img.putdata(pixel_data)

    def save_img(self):
        """
        Save the image to the image directory with a predefined filename, based on the current timestamp
        """

        filename = f'alternate_filling_{now()}.png'
        full_path = os.path.join(self.img_dir, filename)
        self.img.save(full_path)

    def _get_random_rectangle(self) -> matplotlib.path.Path:
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
        p1 = self._rotate_point(p1, random_angle)
        p2 = self._rotate_point(p2, random_angle)
        p3 = self._rotate_point(p3, random_angle)
        p4 = self._rotate_point(p4, random_angle)

        # Shift the polygon such that it is on the screen
        polygon = [p1, p2, p3, p4]
        min_x = min([p.real for p in polygon])
        max_x = max([p.real for p in polygon])
        min_y = min([p.imag for p in polygon])
        max_y = max([p.imag for p in polygon])
        if ALL_RECTANGLES_FULLY_ON_CANVAS:
            shift_in_x = random.uniform(-min_x, self.width - max_x)
            shift_in_y = random.uniform(-min_y, self.height - max_y)
        else:
            shift_in_x = random.uniform(0, self.width)
            shift_in_y = random.uniform(0, self.height)
        p1 = p1 + complex(shift_in_x, shift_in_y)
        p2 = p2 + complex(shift_in_x, shift_in_y)
        p3 = p3 + complex(shift_in_x, shift_in_y)
        p4 = p4 + complex(shift_in_x, shift_in_y)

        # Return the rectangle as a polygon (Path object)
        polygon = [(p.real, p.imag) for p in (p1, p2, p3, p4)]
        bb_path = matplotlib.path.Path(np.array(polygon))
        return bb_path

    @staticmethod
    def _rotate_point(point: complex, angle: float) -> complex:
        r, phi = cmath.polar(point)
        return cmath.rect(r, phi + angle)


if __name__ == '__main__':
    AlternateFilling.draw_multiple_images(1)
