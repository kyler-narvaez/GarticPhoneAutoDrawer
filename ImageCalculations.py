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

def convert_to_grayscale(img_arr):
    # convert to grayscale
    img_gray = img_arr.mean(axis=2).astype(np.float32) / 255.0
    return img_gray

def create_mask(img, threshold=0.5):
    mask = img < threshold #draw darker pixels
    return mask


def get_draw_points(img_path, canvas_width, canvas_height, threshold=0.5, step_count=5):
    img = load_image(img_path)
    
    _, new_width, new_height, x_offset, y_offset = find_scale_and_offsets(img.shape[0], img.shape[1], canvas_width, canvas_height)
    img_resized = resize_image(img, new_width, new_height)

    gray_img = convert_to_grayscale(img_resized)
    mask = create_mask(gray_img, threshold=threshold)

    points = []
    for y in range(0, mask.shape[0], step_count):
        for x in range(0, mask.shape[1], step_count):
            if mask[y, x]:
                points.append((x + x_offset, y + y_offset))

    return points
    

if __name__ == "__main__":
    # Example usage
    points =get_draw_points("./images/test_img.png", 800, 600, threshold=0.5, step_count=12)

    print(f"Number of points to draw: {len(points)}")
    print(points)
