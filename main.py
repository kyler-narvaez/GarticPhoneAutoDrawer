import BrowserFunctions

def main():

    bf = BrowserFunctions.BrowserFunctions()

    bf.OpenBrowser()

    bf.page.goto("https://garticphone.com")

    while True:
        cmd = input("Commands:\n'b' - Draw box border\n'q' - Quit\nPress enter to draw a line\nEnter command: ")

        match cmd.strip().lower():
            case 'q':
                break
            case 'b':
                bf.DrawBoxBorder()
            case 'd':
                img_path = get_img_path()
                threshold = get_float_input('threshold', 0.5)
                step_count = get_int_input('step count', 5)
                bf.DrawImageDots(img_path=img_path, threshold=threshold, step_count=step_count)
            case 's':
                img_path = get_img_path()
                canny_low = get_int_input('canny_low', 50)
                canny_high = get_int_input('canny_high', 150)
                epsilon = get_float_input('epsilon_factor', 0.01)
                segment_steps = get_int_input('segment_steps', 1)
                min_length = get_int_input('min line length', 15)
                bf.DrawImageContours(img_path=img_path,canny_low=canny_low, canny_high=canny_high,epsilon_factor=epsilon,segment_steps=segment_steps)
            case _:
                bf.StartDrawing()
        
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

if __name__ == "__main__":
    main()