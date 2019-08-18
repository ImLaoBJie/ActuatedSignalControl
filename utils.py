from xml.etree.ElementTree import ElementTree
import wx
from pubsub import pub
import threading
import time


def read_tlLogic(target: str):
    # Read and copy ASC.net.xml
    file_path = 'ASC.net.xml'
    tree = ElementTree()
    tree.parse(file_path)
    # get parent
    root = tree.getroot()

    phase_parameter = []

    for tll in root.iter('tlLogic'):
        if tll.attrib['id'] == target:
            for phase in tll.iter('phase'):
                phase_parameter.append(float(phase.attrib['duration']))
            break

    return phase_parameter


class MajorRoadWindows(wx.Frame):
    def __init__(self, parent, title):
        super(MajorRoadWindows, self).__init__(parent, title=title, size=(400, 600), pos=wx.Point(100, 100))
        self.InitUI()
        self.phase = []
        self.phase_init()
        pub.subscribe(self.get_update, 'update')

    def phase_init(self):
        self.phase = []
        for index in range(6):
            self.phase.append(False)

    def InitUI(self):
        self.Bind(wx.EVT_PAINT, self.flowchart)
        self.Show(True)

    def Diamond(self, dc, x, y, a, b, act, text):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        if act:
            dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))
        else:
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        p1 = wx.Point(x, y + b)
        p2 = wx.Point(x + a, y)
        p3 = wx.Point(x + 2 * a, y + b)
        p4 = wx.Point(x + a, y + 2 * b)
        dc.DrawPolygon([p1, p2, p3, p4])
        dc.DrawText('\n' + text, x + 1.5 * a, y + b)

    def Arrow(self, dc, sx, sy, ex, ey, arrow=True):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        dc.DrawLine(sx, sy, ex, ey)
        if arrow:
            dc.DrawCircle(ex, ey, 2)

    def Rectangle(self, dc, x, y, width, height, act, text):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        if act:
            dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))
        else:
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        dc.DrawRectangle(x, y, width, height)
        dc.DrawText(text, x + 1.1 * width, y + height * 0.6)

    def get_update(self, index):
        index = int(index)
        self.phase_init()
        self.phase[index] = True
        # time.sleep(PAUSE)
        self.Refresh()

    def flowchart(self, evt):
        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        self.Arrow(dc, 50, 10, 50, 50)
        self.Rectangle(dc, 30, 50, 40, 50, self.phase[0], 'Main road green!')
        self.Arrow(dc, 50, 100, 50, 150)
        self.Diamond(dc, 30, 150, 20, 25, self.phase[1], '<= MIN_GREEN_TIME_MAJOR?')
        self.Arrow(dc, 50, 200, 50, 250)
        dc.DrawText('YES', 25, 220)
        self.Diamond(dc, 30, 250, 20, 25, self.phase[2], 'Detector\nis triggered?')
        self.Arrow(dc, 50, 300, 50, 350)
        dc.DrawText('NO', 25, 320)
        self.Rectangle(dc, 30, 350, 40, 50, self.phase[3], 'Minor road green!')
        self.Arrow(dc, 50, 400, 50, 450)
        self.Rectangle(dc, 30, 450, 40, 50, self.phase[4], 'Minor road is\nchanged to red!')

        self.Arrow(dc, 30, 475, 10, 475, False)
        self.Arrow(dc, 10, 475, 10, 30, False)
        self.Arrow(dc, 10, 30, 50, 30)

        self.Arrow(dc, 70, 175, 100, 175, False)
        dc.DrawText('NO', 75, 150)
        self.Arrow(dc, 100, 175, 100, 30, False)
        self.Arrow(dc, 100, 30, 50, 30)

        dc.DrawText('YES', 75, 255)
        self.Arrow(dc, 70, 275, 100, 275)
        self.Diamond(dc, 100, 250, 20, 25, self.phase[5], '>= MAX_GREEN_TIME_MAJOR?')
        self.Arrow(dc, 120, 300, 120, 375, False)
        dc.DrawText('YES', 85, 355)
        self.Arrow(dc, 120, 375, 70, 375)

        self.Arrow(dc, 120, 250, 120, 30, False)
        dc.DrawText('NO', 125, 230)
        self.Arrow(dc, 120, 30, 50, 30)


class MinorRoadWindows(wx.Frame):
    def __init__(self, parent, title):
        super(MinorRoadWindows, self).__init__(parent, title=title, size=(350, 650), pos=wx.Point(100, 100))
        self.InitUI()
        self.phase = []
        self.phase_init()
        pub.subscribe(self.get_update, 'update')

    def phase_init(self):
        self.phase = []
        for index in range(5):
            self.phase.append(False)

    def InitUI(self):
        self.Bind(wx.EVT_PAINT, self.flowchart)
        self.Show(True)

    def Diamond(self, dc, x, y, a, b, act, text):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        if act:
            dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))
        else:
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        p1 = wx.Point(x, y + b)
        p2 = wx.Point(x + a, y)
        p3 = wx.Point(x + 2 * a, y + b)
        p4 = wx.Point(x + a, y + 2 * b)
        dc.DrawPolygon([p1, p2, p3, p4])
        dc.DrawText('\n' + text, x + 1.5 * a, y + b)

    def Arrow(self, dc, sx, sy, ex, ey, arrow=True):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        dc.DrawLine(sx, sy, ex, ey)
        if arrow:
            dc.DrawCircle(ex, ey, 2)

    def Rectangle(self, dc, x, y, width, height, act, text):
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0)))
        if act:
            dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))
        else:
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
        dc.DrawRectangle(x, y, width, height)
        dc.DrawText(text, x + 1.1 * width, y + height * 0.6)

    def get_update(self, index):
        index = int(index)
        self.phase_init()
        self.phase[index] = True
        # time.sleep(PAUSE)
        self.Refresh()

    def flowchart(self, evt):
        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        self.Arrow(dc, 50, 10, 50, 50)
        self.Rectangle(dc, 30, 50, 40, 50, self.phase[0], 'Main road green!')
        self.Arrow(dc, 50, 100, 50, 150)
        self.Diamond(dc, 30, 150, 20, 25, self.phase[1], 'Any vehicle on minor road?')
        self.Arrow(dc, 50, 200, 50, 250)
        dc.DrawText('YES', 55, 230)
        self.Rectangle(dc, 30, 250, 40, 50, self.phase[2], 'Minor road green!')
        self.Arrow(dc, 50, 300, 50, 350)
        self.Diamond(dc, 30, 350, 20, 25, self.phase[3], 'Any vehicle on minor road?')
        self.Arrow(dc, 50, 400, 50, 450)
        dc.DrawText('YES', 25, 420)
        self.Diamond(dc, 30, 450, 20, 25, self.phase[4], '>= MAX_GREEN_TIME_MINOR')
        self.Arrow(dc, 50, 500, 50, 550, False)
        dc.DrawText('NO', 25, 520)
        self.Arrow(dc, 50, 550, 10, 550, False)
        self.Arrow(dc, 10, 550, 10, 225, False)
        self.Arrow(dc, 10, 225, 50, 225)

        self.Arrow(dc, 70, 175, 250, 175, False)
        dc.DrawText('NO', 125, 155)
        self.Arrow(dc, 70, 375, 250, 375, False)
        dc.DrawText('NO', 125, 355)
        self.Arrow(dc, 70, 475, 250, 475, False)
        dc.DrawText('YES', 125, 455)
        self.Arrow(dc, 250, 475, 250, 30, False)
        self.Arrow(dc, 250, 30, 50, 30)


class GUIThread(threading.Thread):
    def __init__(self, isMajor, pause):
        threading.Thread.__init__(self)
        self.isMajor = isMajor
        self.windows = None
        self.app = None
        self.setDaemon(True)
        self.pause = pause

    def run(self):
        self.app = wx.App()
        if self.isMajor:
            self.windows = MajorRoadWindows(None, '--Main Road--')
        else:
            self.windows = MinorRoadWindows(None, '--Minor Road--')
        self.app.MainLoop()

    def get_update(self, index):
        time.sleep(self.pause)
        wx.CallAfter(pub.sendMessage, 'update', index=int(index))
