import BrowserFunctions
import os

IMG_DIR = './images/'

def main():

    bf = BrowserFunctions.BrowserFunctions()

    bf.OpenBrowser()

    bf.page.goto("https://garticphone.com")

    while True:
        cmd = input("Commands:\n'b' - Draw box border"
        "\n'd' - Dots"
        "\n's' - Sketch"
        "\n'e' - Erase"
        "\n'q' - Quit\nPress enter to draw a line\nEnter command: ")

        match cmd.strip().lower():
            case 'q':
                break
            case 'b':
                bf.DrawBoxBorder()
            case 'd':
                files = print_images()
                file_index = get_int_input('File Index', len(files)-1)
                img_path = get_img_path(files, file_index)
                mask_thresh = get_float_input('Mask_Thresh', 1.0)
                step_count = get_int_input('step count', 10)
                pen_size = get_int_input('pen_size', 3)
                bf.DrawImageDots(img_path=img_path, threshold=mask_thresh, step_count=step_count, pen_size=pen_size)
            case 's':
                files = print_images()
                file_index = get_int_input('File Index', len(files)-1)
                img_path = get_img_path(files, file_index)
                epsilon = get_float_input('epsilon_factor', 0.001)
                segment_steps = get_int_input('segment_steps', 1)
                mask_thresh = get_float_input('mask_thresh', 0.5)
                min_length = get_int_input('min line length', 30)
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

def list_images():
    file_types = ('.png', '.jpg', '.jpeg', '.bmp', 'webp')
    files = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(file_types))
    return files

def print_images():
    files = list_images()
    for i, file in enumerate(files):
        print(f'{i}: {file}')
    return files

def get_img_path(files, file_index):
    if (file_index < 0): file_index = 0
    elif (file_index >= len(files)): file_index = len(files)-1

    return IMG_DIR + files[file_index]

def get_float_input(name, default_val=1.0):
    user_input = input(f'Enter {name} (default: {default_val}): ').strip()
    return float(user_input) if user_input else default_val

def get_int_input(name, default_val=1):
    user_input = input(f'Enter {name} (default: {default_val}): ').strip()
    return int(user_input) if user_input else default_val


if __name__ == "__main__":
    main()