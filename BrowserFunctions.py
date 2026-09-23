from playwright.sync_api import sync_playwright
from ImageCalculations import get_draw_points

class BrowserFunctions:
    def __init__(self):
        self.playwright_instance = sync_playwright().start()
        self.browser = None
        self.page = None
        self.box = None
        self.maxHeight = 0
        self.maxWidth = 0

    def OpenBrowser(self):
        self.browser = self.playwright_instance.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def CloseBrowser(self):
        self.browser.close()
        self.playwright_instance.stop()

    def FindCanvas(self):
        self.box = self.page.locator('[class*="drawingContainer"] canvas').last.bounding_box(timeout=5000)
        if self.box is None:
            print("No canvas found — are you on the drawing screen?")
            return

        self.maxHeight = self.box["height"]
        self.maxWidth = self.box["width"]

        print(self.box)

    def MoveMouseOnCanvas(self, x, y, steps=20):
        self.page.mouse.move(self.box["x"] + x, self.box["y"] + y, steps=steps)

    def StartDrawing(self):
        self.FindCanvas()
        self.MoveMouseOnCanvas(0, 0)
        self.page.mouse.down()
        self.page.mouse.up()

        self.MoveMouseOnCanvas(self.maxWidth//2, self.maxHeight//2)
        self.page.mouse.down()
        self.MoveMouseOnCanvas(self.maxWidth//2 + 30, self.maxHeight//2 + 50)
        self.page.mouse.up()

    def DrawBoxBorder(self):
        self.FindCanvas()
        self.MoveMouseOnCanvas(0, 0)
        self.page.mouse.down()
        self.MoveMouseOnCanvas(self.maxWidth, 0)
        self.MoveMouseOnCanvas(self.maxWidth, self.maxHeight)
        self.MoveMouseOnCanvas(0, self.maxHeight)
        self.MoveMouseOnCanvas(0, 0)
        self.page.mouse.up()

    def DrawImage(self, img_path="./images/test_img.png", threshold=0.5, step_count=5):
        self.FindCanvas()
        points = get_draw_points(img_path, self.maxWidth, self.maxHeight, threshold=threshold, step_count=step_count)

        if not points:
            print("No points to draw — check your image and threshold.")
            return

        for (x, y) in points:
            self.MoveMouseOnCanvas(x, y)
            self.page.mouse.down()
            self.page.mouse.up()
