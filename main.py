import BrowserFunctions

def main():

    bf = BrowserFunctions.BrowserFunctions()

    bf.OpenBrowser()

    bf.page.goto("https://garticphone.com")

    while True:
        cmd = input("Press Enter to draw, or type 'q' to quit: ")
        if cmd.strip().lower() == 'q':
            break
        bf.StartDrawing()
        print("Done drawing.")
        
    bf.CloseBrowser() #Done


if __name__ == "__main__":
    main()