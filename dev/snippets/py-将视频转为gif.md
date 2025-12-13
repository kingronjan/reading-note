require python >= 3.9

```python
from moviepy.editor import *
from PIL import Image

# clip = (VideoFileClip("<video-filepath>").resize((488, 225), Image.LANCZOS))
clip = (VideoFileClip("<video-filepath>").subclip(t_start=5, t_end=12).resize(0.5, Image.LANCZOS))

clip.write_gif("<gif-filepath>", fps=15)

```