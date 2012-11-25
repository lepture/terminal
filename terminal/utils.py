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
