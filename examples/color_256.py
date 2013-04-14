import sys
from terminal import Color

def _pad(i):
    i = str(i)
    return i + ' ' * (5 - len(i))


print('System colors')
for i in range(16):
    c = Color('  ')
    c.bgcolor = i
    if i == 8:
        print('')
    sys.stdout.write(str(c))

print('\n\nBackground')
for green in range(6):
    for red in range(6):
        for blue in range(6):
            c = Color('  ')
            c.bgcolor = 16 + red * 36 + green * 6 + blue
            sys.stdout.write(str(c))
    print('')


print('\nGrayscale')
for i in range(232, 256):
    c = Color('  ')
    c.bgcolor = i
    sys.stdout.write(str(c))

print('\n\nColors')
for i in range(256):
    if i != 0 and i % 16 == 0:
        print('')

    c = Color(_pad(i))
    c.fgcolor = i
    sys.stdout.write(str(c))

print('')
