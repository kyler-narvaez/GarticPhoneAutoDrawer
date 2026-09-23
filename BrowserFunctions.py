from playwright.sync_api import sync_playwright
from ImageCalculations import get_draw_points, get_draw_strokes

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

    def MoveMouseOnCanvas(self, x, y, steps=1):
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

    def DrawImageDots(self, img_path="./images/test_img.png", threshold=0.5, step_count=5):
        self.FindCanvas()
        points = get_draw_points(img_path, self.maxWidth, self.maxHeight, threshold=threshold, step_count=step_count)

        if not points:
            print("No points to draw — check your image and threshold.")
            return

        for (x, y) in points:
            self.MoveMouseOnCanvas(x, y)
            self.page.mouse.down()
            self.page.mouse.up()

    def DrawStroke(self, points, segment_steps=3):
        if len(points) < 2:
            print("Not enough points to draw a stroke.")
            return
        x0, y0 = points[0]
        self.MoveMouseOnCanvas(x0, y0)
        self.page.mouse.down()
        for (x1, y1) in points[1:]:
            self.MoveMouseOnCanvas(x1, y1, steps=segment_steps)
        self.page.mouse.up()

    def DrawImageContours(self, img_path="./images/test_img.png", canny_low=50, canny_high=150, epsilon_factor=0.01, segment_steps=3, min_length=15):
        self.FindCanvas()
        strokes = get_draw_strokes(img_path, self.maxWidth, self.maxHeight, canny_low=canny_low, canny_high=canny_high, epsilon_factor=epsilon_factor)

        if not strokes:
            print("No strokes to draw — check your image and threshold.")
            return

        # Draw the contours by connecting the points
        for stroke in strokes:
            self.DrawStroke(stroke, segment_steps=segment_steps)
