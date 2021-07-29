from Xlib import X


class XSelect:
    def __init__(self, display):
        # X display
        self.d = display

        # Screen
        self.screen = self.d.screen()

        # Draw on the root window (desktop surface)
        self.window = self.screen.root

        # If only I could get this working...
        # cursor = xobject.cursor.Cursor(self.d, Xcursorfont.crosshair)
        # cursor = self.d.create_resource_object('cursor', Xcursorfont.X_cursor)
        self.cursor = X.NONE

        colormap = self.screen.default_colormap
        color = colormap.alloc_color(0, 0, 0)
        # Xor it because we'll draw with X.GXxor function
        xor_color = color.pixel ^ 0xffffff

        self.gc = self.window.create_gc(
            line_width=1,
            line_style=X.LineSolid,
            fill_style=X.FillOpaqueStippled,
            fill_rule=X.WindingRule,
            cap_style=X.CapButt,
            join_style=X.JoinMiter,
            foreground=xor_color,
            background=self.screen.black_pixel,
            function=X.GXxor,
            graphics_exposures=False,
            subwindow_mode=X.IncludeInferiors,
        )

    def get_mouse_selection(self):
        started = False
        start = dict(x=0, y=0)
        end = dict(x=0, y=0)
        last = None
        drawlimit = 10
        i = 0

        self.window.grab_pointer(self.d, X.PointerMotionMask | X.ButtonReleaseMask | X.ButtonPressMask,
                                 X.GrabModeAsync, X.GrabModeAsync, X.NONE, self.cursor, X.CurrentTime)

        self.window.grab_keyboard(self.d, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

        while True:
            e = self.d.next_event()

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                break

            # Mouse button press
            elif e.type == X.ButtonPress:
                # Left mouse button?
                if e.detail == 1:
                    start = dict(x=e.root_x, y=e.root_y)
                    started = True

                # Right mouse button?
                elif e.detail == 3:
                    return

            # Mouse button release
            elif e.type == X.ButtonRelease:
                end = dict(x=e.root_x, y=e.root_y)
                if last:
                    self.draw_rectangle(start, last)
                break

            # Mouse movement
            elif e.type == X.MotionNotify and started:
                i = i + 1
                if i % drawlimit != 0:
                    continue

                if last:
                    self.draw_rectangle(start, last)

                last = dict(x=e.root_x, y=e.root_y)
                self.draw_rectangle(start, last)

        self.d.ungrab_keyboard(X.CurrentTime)
        self.d.ungrab_pointer(X.CurrentTime)
        self.d.sync()

        coords = self.get_coords(start, end)
        if coords['width'] <= 1 or coords['height'] <= 1:
            return
        return [coords['start']['x'], coords['start']['y'], coords['width'], coords['height']]

    @staticmethod
    def get_coords(start, end):
        safe_start = dict(x=0, y=0)
        safe_end = dict(x=0, y=0)

        if start['x'] > end['x']:
            safe_start['x'] = end['x']
            safe_end['x'] = start['x']
        else:
            safe_start['x'] = start['x']
            safe_end['x'] = end['x']

        if start['y'] > end['y']:
            safe_start['y'] = end['y']
            safe_end['y'] = start['y']
        else:
            safe_start['y'] = start['y']
            safe_end['y'] = end['y']

        return {
            'start': {
                'x': safe_start['x'],
                'y': safe_start['y'],
            },
            'end': {
                'x': safe_end['x'],
                'y': safe_end['y'],
            },
            'width': safe_end['x'] - safe_start['x'],
            'height': safe_end['y'] - safe_start['y'],
        }

    def draw_rectangle(self, start, end):
        coords = self.get_coords(start, end)
        self.window.rectangle(self.gc,
                              coords['start']['x'],
                              coords['start']['y'],
                              coords['end']['x'] - coords['start']['x'],
                              coords['end']['y'] - coords['start']['y']
                              )
