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
            case 'i':
                img_path = input("Enter image path (default: ./images/test_img.png): ").strip()
                if not img_path:
                    img_path = "./images/test_img.png"
                threshold_input = input("Enter threshold (default: 0.5): ").strip()
                threshold = float(threshold_input) if threshold_input else 0.5
                step_count_input = input("Enter step count (default: 5): ").strip()
                step_count = int(step_count_input) if step_count_input else 5
                bf.DrawImage(img_path=img_path, threshold=threshold, step_count=step_count)
            case _:
                bf.StartDrawing()
        
        print("Done drawing.")
        
    bf.CloseBrowser() #Done


if __name__ == "__main__":
    main()