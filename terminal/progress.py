#!/usr/bin/env python
import os


def get_terminal_width():
    "Borrowed from the py lib."
    try:
        import termios
        import fcntl
        import struct
        call = fcntl.ioctl(0, termios.TIOCGWINSZ,
                           struct.pack('hhhh', 0, 0, 0, 0))
        _, width = struct.upack('hhhh', call)[:2]
        return width
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        # Fallback
        return int(os.environ.get('COLUMNS', 80))


class Progress(object):
    def __init__(self, marker='#', left='', fill=' '):
        self.marker = marker
        self.left = left
        if len(fill) == 0:
            # TODO
            raise
        self.fill = fill
        self.width = get_terminal_width()

    def bar_text(self, current, total, right=''):
        if current > total:
            # TODO
            raise
        marker = int(current * self.width / float(total)) * self.marker
        to_fill = self.width - len(self.left) - len(right) - len(marker)
        fill = ((to_fill - 1) / len(self.fill) + 1) * self.fill
        fill = fill[:to_fill]
        return '%s%s%s%s' % (self.left, marker, fill, right)
