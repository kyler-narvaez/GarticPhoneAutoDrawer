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
            case _:
                bf.StartDrawing()
        
        print("Done drawing.")
        
    bf.CloseBrowser() #Done


if __name__ == "__main__":
    main()