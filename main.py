import BrowserFunctions
import os

def main():

    bf = BrowserFunctions.BrowserFunctions()

    bf.OpenBrowser()

    bf.page.goto("https://garticphone.com")

    while True:
        cmd = input("Commands:\n'b' - Draw box border"
        "\n'd' - Dots"
        "\n's' - Strokes"
        "\n'e' - Erase"
        "\n'q' - Quit\nPress enter to draw a line\nEnter command: ")

        image_picker()

        match cmd.strip().lower():
            case 'q':
                break
            case 'b':
                bf.DrawBoxBorder()
            case 'd':
                img_path = get_img_path()
                threshold = get_float_input('threshold', 0.5)
                step_count = get_int_input('step count', 5)
                pen_size = get_int_input('pen_size', 1)
                bf.DrawImageDots(img_path=img_path, threshold=threshold, step_count=step_count, pen_size=pen_size)
            case 's':
                img_path = get_img_path()
                epsilon = get_float_input('epsilon_factor', 0.01)
                segment_steps = get_int_input('segment_steps', 1)
                mask_thresh = get_float_input('mask_thresh', 0.5)
                min_length = get_int_input('min line length', 10)
                pen_size = get_int_input('pen_size', 1)
                bf.DrawImageContours(img_path=img_path,epsilon_factor=epsilon,
                                     segment_steps=segment_steps,mask_thresh=mask_thresh,
                                     min_length=min_length,pen_size=pen_size)
            case 'e':
                bf.EraseDrawing()
            case _:
                pass
        
        print("Done drawing.")
        
    bf.CloseBrowser() #Done


def get_img_path():
    img_path = input("Enter image path (default: ./images/test_img.png): ").strip()
    if not img_path:
        img_path = "./images/test_img.png"

    return img_path

def get_float_input(name, default_val=1.0):
    user_input = input(f'Enter {name} (default: {default_val}): ').strip()
    return float(user_input) if user_input else default_val

def get_int_input(name, default_val=1):
    user_input = input(f'Enter {name} (default: {default_val}): ').strip()
    return int(user_input) if user_input else default_val

def image_picker():
    image_paths = os.listdir('./images/')
    print("List of current paths:")
    for images in image_paths:
        print('\t./images/' + images)

if __name__ == "__main__":
    main()