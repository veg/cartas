

__all__ = ['LinearGradient']


class LinearGradient(object):

    def __init__(self, colors):
        if len(colors) < 2:
            raise ValueError('Linear gradient takes a list of at least 2 colors')
        self._region = 1 / (len(colors) - 1)
        rgb_tuples = []
        for color in colors:
            verified = False
            if isinstance(color, tuple) and len(color) == 3:
                verified = True
                rgb_tuples.append(color)
            elif isinstance(color, str) and len(color.strip()) == 7:
                verified = True
                rgb_tuples.append(LinearGradient._html2rgb(color))
            else:
                raise ValueError('LinearGradient takes html color codes or rgb 3-tuples')
        self._colors = rgb_tuples

    def __call__(self, x):
        assert 0 <= x <= 1, "x must be between 0 and 1, inclusive"
        idx = int(x // self._region)
        # how far between colors are we
        percent = (x - idx * self._region) / self._region
        # grab the two colors we care about
        colorA = self._colors[idx]
        # if there's nothing but the last color, just use that
        if idx + 1 >= len(self._colors):
            rgb = colorA
        else:
            colorB = self._colors[idx + 1]
            # interpolate the color
            rgb = tuple(colorA[i] + percent * (colorB[i] - colorA[i]) for i in range(3))
        return LinearGradient._rgb2html(rgb)

    @staticmethod
    def _rgb2html(rgb):
        assert isinstance(rgb, tuple) and len(rgb) == 3, "_rgb2html takes an rgb 3-tuple"
        # %02x is a 0-padded 2-digit hex value
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def _html2rgb(html):
        html = html.strip()
        assert html[0] == '#' and len(html) == 7, "input '%s' is not an html color code" % html
        return tuple(int(n, 16) for n in (html[1:3], html[3:5], html[5:]))
