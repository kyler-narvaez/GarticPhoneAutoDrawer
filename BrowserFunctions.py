from playwright.sync_api import sync_playwright

class BrowserFunctions:
    def __init__(self):
        self.playwright_instance = sync_playwright().start()
        self.browser = None
        self.page = None

    def OpenBrowser(self):
        self.browser = self.playwright_instance.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def CloseBrowser(self):
        self.browser.close()
        self.playwright_instance.stop()

    def StartDrawing(self):
        #get canvas to paint
        box = self.page.locator('[class*="drawingContainer"] canvas').last.bounding_box(timeout=5000)
        if box is None:
            print("No canvas found — are you on the drawing screen?")
            return
        
        print(box)
    
        self.page.mouse.move(box["x"]+3, box["y"]+3)
        self.page.mouse.down()
        self.page.mouse.up()

        self.page.mouse.move(box["x"]+box["width"]//2, box["y"]+box["height"]//2)
        self.page.mouse.down()
        self.page.mouse.move(box["x"]+box["width"]//2 + 30, box["y"]+box["height"]//2+50)
        self.page.mouse.up()