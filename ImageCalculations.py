from PIL import Image
import numpy as np

def load_image(path):
    img = Image.open(path)

    #convert to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')

    img_arr = np.array(img)

    return img_arr

def find_scale_and_offsets(img_height, img_width, max_height, max_width):
    # Calculate the scaling factor to fit the image within the max dimensions
    scale = min(max_height / img_height, max_width / img_width)

    # Calculate the new dimensions
    new_height = int(img_height * scale)
    new_width = int(img_width * scale)

    #center img to canvas
    y_offset = (max_height - new_height) // 2
    x_offset = (max_width - new_width) // 2

    return scale, new_width, new_height, x_offset, y_offset

def resize_image(img_arr, new_width, new_height):
    img = Image.fromarray(img_arr)
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    return np.array(img_resized)

def save_image(img_arr, path):
    img = Image.fromarray(img_arr)
    img.save(path)

if __name__ == "__main__":
    # Example usage
    img = load_image("./images/test_img.png")
    scale, new_width, new_height, x_offset, y_offset = find_scale_and_offsets(img.shape[0], img.shape[1], 500, 500)
    img_resized = resize_image(img, new_width, new_height)
    save_image(img_resized, "./images/resized_img.png")
    print(f"Scale: {scale}, X Offset: {x_offset}, Y Offset: {y_offset}")
