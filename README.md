# prettyPic
A fairly simple image utility library that has one single purpose: to extract the dominant color from an image.

## Installation
```bash
pip install prettyPic
```

## Usage
```python
from prettypic import color_from_image

color = color_from_image('path/to/image.png')
print(color.color)
```
#### Response
```python
color.color # (r, g, b)
color.color_as_image # PIL.Image
color.color_as_rgb # rgb(rrr, ggg, bbb)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
