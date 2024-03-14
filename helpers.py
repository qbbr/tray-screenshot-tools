import glob
import os
import time
import const
import sys
import subprocess
import wx
import pyscreenshot as ImageGrab
import logging

from Xlib import display
from XSelect import XSelect


def d(data):
    logging.debug(data)


def get_screen_size() -> (int, int):
    xs = XSelect(display.Display())
    screen = xs.screen
    return screen.width_in_pixels, screen.height_in_pixels


def get_mouse_selection():
    xs = XSelect(display.Display())
    return xs.get_mouse_selection()


def open(path) -> None:
    d('open %s' % path)
    cmd = {'linux': 'xdg-open',
           'win32': 'explorer',
           'darwin': 'open'}[sys.platform]
    subprocess.Popen([cmd, path])


def grab(path, bbox=None) -> None:
    im = ImageGrab.grab(bbox=bbox)
    im.save(path)


def copy_to_clipboard(path) -> None:
    d('copy to clipboard')
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(wx.BitmapDataObject(wx.Bitmap(path)))
        wx.TheClipboard.Close()


def get_path(filename: str) -> str:
    return const.SCREENSHOTS_DIR + '/' + filename + '.png'


def get_count() -> int:
    return len(glob.glob(const.SCREENSHOTS_DIR + '/*.png'))


def cleanup() -> None:
    d('cleanup')
    for f in glob.glob(const.SCREENSHOTS_DIR + '/*.png'):
        d('remove file: ' + f)
        os.remove(f)


def screenshot(fullscreen=False) -> None:
    width, height = get_screen_size()
    bbox = None

    if not fullscreen:
        area = get_mouse_selection()
        if area:
            x, y, width, height = area
            bbox = x, y, x + width, y + height

    filename = time.strftime('%Y-%m-%d_%H%M%S') + '_%dx%d' % (width, height)
    path = get_path(filename)
    d(path)
    grab(path, bbox)

    if const.COPY_TO_CLIPBOARD:
        copy_to_clipboard(path)

    if const.OPEN_IMAGE:
        open(path)
