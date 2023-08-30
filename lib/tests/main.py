from pytest import fixture
from prettypic import color_from_image
import os


def get_path(filename):
    return os.path.join(os.path.dirname(__file__), "pics", filename)


@fixture
def image():
    yield ['album1.jpg', 'album2.jpg']


def test_color_generations(image):
    for i in image:
        color = color_from_image(get_path(i))
        assert len(color.color) == 3
        assert len(color.color_as_RGB) > 0
        assert color.color_as_image is not None
        assert color.color_as_image.size == (
            color._imageWidth, color._imageHeight)
