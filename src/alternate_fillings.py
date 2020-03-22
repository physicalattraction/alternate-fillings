import cmath
import os.path
import random

import matplotlib.path
import numpy as np
from PIL import Image, ImageDraw

CANVAS_SIZE = 200
MIN_LENGTH = 0.4 * CANVAS_SIZE
MAX_LENGTH = CANVAS_SIZE
MIN_WIDTH = 0.1 * CANVAS_SIZE
MAX_WIDTH = 0.4 * CANVAS_SIZE
NR_RECTANGLES = 6

ALL_RECTANGLES_FULLY_ON_CANVAS = False


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

    def get_random_rectangle(self) -> matplotlib.path.Path:
        random_length = random.uniform(MIN_LENGTH, MAX_LENGTH)
        random_width = random.uniform(MIN_WIDTH, MAX_WIDTH)

        # Get the coordinates without rotation with center at (0,0)
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
        # TODO: It doesn't need to be fully on the screen

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

        polygon = [(p.real, p.imag) for p in (p1, p2, p3, p4)]

        bb_path = matplotlib.path.Path(np.array(polygon))

        return bb_path

    def draw_canvas(self):
        polygons = [self.get_random_rectangle() for _ in range(NR_RECTANGLES)]
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
        self.img.show()

    @staticmethod
    def _rotate_point(point: complex, angle: float) -> complex:
        r, phi = cmath.polar(point)
        return cmath.rect(r, phi + angle)


if __name__ == '__main__':
    af = AlternateFilling()
    af.draw_canvas()
