#!/usr/bin/env python3
import logging
import wx
import wx.adv
import argparse

import const
from helpers import d, screenshot, cleanup


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.myapp_frame = frame
        self.set_icon(const.TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, const.TRAY_TOOLTIP)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, 'Select Area', -1, self.on_select_area)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Cleanup', -1, self.on_cleanup)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', -1, self.on_exit)
        return menu

    @staticmethod
    def create_menu_item(menu, label, id, func):
        item = wx.MenuItem(menu, id, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    @staticmethod
    def on_left_down(event):
        d('left btn clicked')
        screenshot(fullscreen=True)

    @staticmethod
    def on_select_area(event):
        d('select area')
        screenshot(fullscreen=False)

    @staticmethod
    def on_cleanup(event):
        d('cleanup')
        cleanup()

    def on_exit(self, event):
        d('exit btn clicked')
        self.myapp_frame.Close()


class MyApplication(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, '', size=(1, 1))
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        d('destroy app')
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tray App for take screenshot')
    parser.add_argument('--debug', help='enable debug output to console', action='count', default=0)
    parser.add_argument('--clipboard', help='copy image to clipboard after take screenshot', action='count', default=0)
    parser.add_argument('--open-image', help='open image after take screenshot', action='count', default=0)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    if args.clipboard:
        const.COPY_TO_CLIPBOARD = True

    if args.open_image:
        const.OPEN_IMAGE = True

    MyApp = wx.App()
    MyApplication()
    MyApp.MainLoop()