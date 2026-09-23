from PIL import Image
import numpy as np

def load_image(path):
    img = Image.open(path)

    #convert to float and normalize to [0, 1]
    if img.dtype != np.float32:
        img = np.array(img, dtype=np.float32) / 255.0

    return img

def scale_image(img_height, img_width, max_height, max_width):
    # Calculate the scaling factor to fit the image within the max dimensions
    scale = min(max_height / img_height, max_width / img_width)

    # Calculate the new dimensions
    new_height = int(img_height * scale)
    new_width = int(img_width * scale)

    #center img to canvas
    y_offset = (max_height - new_height) // 2
    x_offset = (max_width - new_width) // 2

    return scale, x_offset, y_offset