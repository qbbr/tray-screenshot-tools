# tray-screenshot-tools

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)

```bash
$ ./tray-screenshot-tools -h
```

```
usage: tray-screenshot-tools [-h] [--cleanup] [--debug] [--clipboard] [--open-image]

Tray App for take screenshots by @qbbr

optional arguments:
  -h, --help    show this help message and exit
  --cleanup     cleanup SCREENSHOTS_DIR and exit
  --debug       enable debug output to console
  --clipboard   copy image to clipboard after take screenshot
  --open-image  open image after take screenshot

SCREENSHOTS_DIR: ./screenshots
```

## depends

* [python3](https://www.python.org/)
* [wxPython](https://wxpython.org/)
* [python-xlib](https://pypi.org/project/python-xlib/)

## dev

```bash
sudo apt install build-essential libgtk-3-dev python3-venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./tray-screenshot-tools --debug
```
