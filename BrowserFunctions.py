from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from ImageCalculations import get_draw_points, get_draw_strokes

class BrowserFunctions:
    def __init__(self):
        self.playwright_instance = sync_playwright().start()
        self.browser = None
        self.page = None
        self.box = None
        self.maxHeight = 0
        self.maxWidth = 0
        self.penSizes = []
        self.colorInput = None

    def OpenBrowser(self):
        self.browser = self.playwright_instance.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def CloseBrowser(self):
        self.browser.close()
        self.playwright_instance.stop()

    def FindCanvas(self):
        try:
            self.box = self.page.locator('[class*="drawingContainer"] canvas').last.bounding_box(timeout=10000)
        except PlaywrightTimeoutError:
            print("Canvas not found — are you on the drawing screen?")
            self.box = None
            return False
        
        if self.box is None:
            print("Canvas locator resolved but returned no box — is it visible?")
            return False
        
        self.maxWidth = self.box["width"]
        self.maxHeight = self.box["height"]
        return True

    def FindPenSizes(self):
        self.penSizes = self.page.locator('button[class*="thickness"]').all()

    def SetPenSize(self, size):
        self.FindPenSizes()
        if (size < 0): size = 0
        elif (size > 4): size = 4
        self.penSizes[size].click()

    def SetPen(self):
        self.page.locator('button[class*="tool pen"]').click()

    def SetEraser(self):
        self.page.locator('button[class*="tool ers"]').click()

    def FindColorInput(self):
        self.colorInput = self.page.locator('input[type="color"]')

    def SetColor(self, rgb):
        if self.colorInput.count() == 0:
            return 

        r, g, b = rgb
        hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"

        self.colorInput.fill(hex_color)

    def MoveMouseOnCanvas(self, x, y, steps=1):
        self.page.mouse.move(self.box["x"] + x, self.box["y"] + y, steps=steps)

    def EraseDrawing(self):
        if not self.FindCanvas():
            return
        self.SetPenSize(4)
        self.SetEraser()
        for row in range(0, int(self.maxHeight), 20):
            self.MoveMouseOnCanvas(0, row)
            self.page.mouse.down()
            self.MoveMouseOnCanvas(self.maxWidth, row)
            self.page.mouse.up()

    def DrawBoxBorder(self):
        if not self.FindCanvas():
            return
        self.SetPen()
        self.MoveMouseOnCanvas(0, 0)
        self.page.mouse.down()
        self.MoveMouseOnCanvas(self.maxWidth, 0)
        self.MoveMouseOnCanvas(self.maxWidth, self.maxHeight)
        self.MoveMouseOnCanvas(0, self.maxHeight)
        self.MoveMouseOnCanvas(0, 0)
        self.page.mouse.up()

    def DrawImageDots(self, img_path="./images/test_img.png", step_count=5, pen_size=2):
        if not self.FindCanvas():
            return
        self.SetPenSize(pen_size)
        self.SetPen()
        self.FindColorInput()
        points = get_draw_points(img_path, self.maxWidth, self.maxHeight, step_count=step_count)

        if not points:
            print("No points to draw — check your image and threshold.")
            return

        for x, y, rgb in points:
            self.SetColor(rgb)
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

    def DrawImageContours(self, img_path="./images/test_img.png", epsilon_factor=0.01, segment_steps=3, mask_thresh=0.5, min_length=15, pen_size=2):
        if not self.FindCanvas():
            return
        self.SetPenSize(pen_size)
        self.SetPen()
        self.FindColorInput()
        self.SetColor((0,0,0)) #black
        strokes = get_draw_strokes(img_path, self.maxWidth, self.maxHeight, epsilon_factor=epsilon_factor, mask_thresh=mask_thresh, min_length=min_length)

        if not strokes:
            print("No strokes to draw — check your image and threshold.")
            return

        # Draw the contours by connecting the points
        for stroke in strokes:
            self.DrawStroke(stroke, segment_steps=segment_steps)
