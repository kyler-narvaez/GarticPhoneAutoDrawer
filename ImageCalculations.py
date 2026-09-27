from PIL import Image
import numpy as np
import cv2
from skimage.morphology import skeletonize

def load_image(path):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print(f"Error: The file at '{path}' does not exist.")
        return

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
    if img_arr.dtype != np.uint8:
        img_arr = (np.clip(img_arr, 0, 1) * 255).astype(np.uint8)
    img = Image.fromarray(img_arr)
    img.save(path)

def save_contours_as_image(contours, width, height, path, thickness=1):
    canvas = np.ones((height, width), dtype=np.uint8) * 255  # white background
    for contour in contours:
        pts = contour.reshape(-1, 1, 2).astype(np.int32)
        cv2.polylines(canvas, [pts], isClosed=False, color=0, thickness=thickness)
    save_image(canvas, path)

def convert_to_grayscale(img_arr):
    # convert to grayscale
    img_gray = img_arr.mean(axis=2).astype(np.float32) / 255.0
    return img_gray

def create_mask(img, threshold=0.5):
    mask = img < threshold #draw darker pixels
    return mask

def get_draw_points(img_path, canvas_width, canvas_height, threshold=0.5,step_count=5):
    img = load_image(img_path)

    if img is None: return
    
    _, new_width, new_height, x_offset, y_offset = find_scale_and_offsets(img.shape[0], img.shape[1], canvas_height, canvas_width)
    img_resized = resize_image(img, new_width, new_height)

    gray_img = convert_to_grayscale(img_resized)
    save_image(gray_img, './gray.png')
    mask = create_mask(gray_img, threshold=threshold)
    save_image(mask, './mask.png')

    points = []
    for y in range(0, new_height, step_count):
        for x in range(0, new_width, step_count):
            if mask[y, x]:
                r, g, b = img_resized[y, x]
                points.append((x + x_offset, y + y_offset, (int(r), int(g), int(b))))
                

    return points
    
def get_contours(skeleton):
    # Convert boolean mask to uint8
    skeleton = (skeleton * 255).astype(np.uint8)
    # Find contours using OpenCV
    contours, _ = cv2.findContours(skeleton, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def simplify_contours(contours, epsilon_factor=0.01, min_length=15, small_area_threshold=500, small_epsilon_factor=0.002):
    simplified_contours = []
    for c in contours:
        length = cv2.arcLength(c, closed=True)
        if length < min_length:
            continue
        area = cv2.contourArea(c)
        factor = small_epsilon_factor if area < small_area_threshold else epsilon_factor
        epsilon = factor * length
        simplified = cv2.approxPolyDP(c, epsilon, closed=True)
        simplified_contours.append(simplified.reshape(-1, 2))
    return simplified_contours


def get_draw_strokes(img_path, canvas_width, canvas_height, epsilon_factor=0.01, canny_low=50, canny_high=150, fill_area_ratio=0.5, min_length=15):
    img = load_image(img_path)
    if img is None:
        return

    _, new_width, new_height, x_offset, y_offset = find_scale_and_offsets(
        img.shape[0], img.shape[1], canvas_height, canvas_width
    )
    img_resized = resize_image(img, new_width, new_height)

    gray_img = convert_to_grayscale(img_resized)
    gray_uint8 = (gray_img * 255).astype(np.uint8)
    save_image(gray_img, './gray.png')

    # replaces create_mask/threshold — edges instead of brightness, polarity-agnostic
    edges = cv2.Canny(gray_uint8, canny_low, canny_high)
    edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    save_image(edges_closed, './edges.png')

    contours, hierarchy = cv2.findContours(edges_closed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    simplified_contours = []
    for c in contours:
        length = cv2.arcLength(c, closed=True)
        if length < min_length:
            continue

        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        fill_ratio = area / max(w * h, 1)

        if fill_ratio > fill_area_ratio:
            # filled region — use its outline directly, no skeletonize needed
            epsilon = epsilon_factor * length
            simplified = cv2.approxPolyDP(c, epsilon, closed=True)
            simplified_contours.append(simplified.reshape(-1, 2))
        else:
            # thin/line-like — build a small mask of just this contour, skeletonize that alone
            local_mask = np.zeros((new_height, new_width), dtype=np.uint8)
            cv2.drawContours(local_mask, [c], -1, 255, thickness=cv2.FILLED)
            local_skeleton = skeletonize(local_mask.astype(bool))

            line_contours = get_contours(local_skeleton)  # your existing sknw-based function
            line_simplified = simplify_contours(line_contours, epsilon_factor=epsilon_factor, min_length=min_length)
            simplified_contours.extend(line_simplified)

    save_contours_as_image(simplified_contours, new_width, new_height, './simp_conts.png')

    offset_contours = []
    for contour in simplified_contours:
        offset_contour = [(x + x_offset, y + y_offset) for (x, y) in contour]
        offset_contours.append(offset_contour)

    return offset_contours
if __name__ == "__main__":
    # Example usage
    points = get_draw_points("./images/test_img.png", 800, 600, threshold=0.5, step_count=12)

    print(f"Number of points to draw: {len(points)}")
    print(points)
