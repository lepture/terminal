#!/usr/bin/env python
import os


def get_terminal_width():
    """Borrowed from the py lib."""
    try:
        import termios
        import fcntl
        import struct
        call = fcntl.ioctl(0, termios.TIOCGWINSZ,
                           struct.pack('hhhh', 0, 0, 0, 0))
        height, width = struct.unpack('hhhh', call)[:2]
        terminal_width = width
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        # FALLBACK
        terminal_width = int(os.environ.get('COLUMNS', 80)) - 1
    return terminal_width


class Progress(object):
    def __init__(self, marker='#', left='', right='', fill=' '):
        self.marker = marker
        self.left = left
        self.right = right
        if len(fill) != 1:
            raise ValueError('You must a char.')
        self.fill = fill
        self.width = get_terminal_width()

    def __call__(self, current, total, blank='', status=''):
        if current > total:
            raise ValueError("current can't be larger than total.")
        count = len(blank) + len(status) + len(self.left) + len(self.right)

        marker = int((self.width - count) / float(total) * current) * \
                self.marker
        if len(marker) >= self.width - count:
            marker = marker[:self.width - count]

        bar = blank + self.left + marker + self.right
        text = status.rjust(self.width, self.fill)
        text = text.replace(self.fill * len(bar), bar, 1)
        return text
