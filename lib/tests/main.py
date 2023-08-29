from pytest import fixture
from prettyPic import color_from_image


@fixture
def image():
    yield ["./pics/album1.jpg", "./pics/album2.jpg"]


def test_color_generations(image):
    color = color_from_image(image)
    assert len(color.color) == 3
    assert len(color.color_as_RGB) > 0
    assert color.color_as_image is not None
    assert color.color_as_image.size == (color.imageWidth, color.imageHeight)
