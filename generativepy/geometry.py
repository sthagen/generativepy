# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
import cairo
import math

from generativepy.drawing import LEFT, BASELINE, CENTER, RIGHT, BOTTOM, TOP


class Shape():

    def __init__(self, ctx):
        self.ctx = ctx

    def add(self):
        raise NotImplementedError()

    def fill(self, color=None):
        self.ctx.new_path()
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
        self.ctx.fill()
        return self

    def stroke(self, color=None, line_width=1):
        self.ctx.new_path()
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
            self.ctx.set_line_width(line_width)
        self.ctx.stroke()
        return self

    def fill_stroke(self, fill_color, stroke_colour, line_width=1):
        self.ctx.new_path()
        self.add()
        self.ctx.set_source_rgba(*fill_color)
        self.ctx.fill_preserve()
        self.ctx.set_source_rgba(*stroke_colour)
        self.ctx.set_line_width(line_width)
        self.ctx.stroke()
        return self

class Rectangle(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def add(self):
        self.ctx.rectangle(self.x, self.y, self.width, self.height)
        return self

    def of_corner_size(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        return self


def rectangle(ctx, x, y, width, height):
    Rectangle(ctx).of_corner_size(x, y, width, height).add()

# TODO create Text object
def text(ctx, txt, x, y, font=None, size=None, color=None, alignx=LEFT, aligny=BASELINE, flip=False):
    '''
    Draw text using ths supplied ctx
    :param ctx: The context
    :param txt: The text, string
    :param x: x position
    :param y: y position
    :param font: font name, string
    :param size: text size
    :param color: text colour, Color
    :param alignx: x alignment
    :param aligny: y alignemen
    :param flip: True to flip the text (for maths drawing)
    :return:
    '''
    if font:
        ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    if size:
        ctx.set_font_size(size)

    if color:
        ctx.set_source_rgba(*color)

    xb, yb, width, height, dx, dy = ctx.text_extents(txt)

    x -= xb
    if alignx == CENTER:
        x -= width / 2
    elif alignx == RIGHT:
        x -= width

    if aligny == CENTER:
        dy = -yb / 2
    elif aligny == BOTTOM:
        dy = -(yb + height)
    elif aligny == TOP:
        dy = -yb

    if flip:
        ctx.move_to(x, y - dy)
        ctx.save()
        ctx.scale(1, -1)
        ctx.show_text(txt)
        ctx.restore()
    else:
        ctx.move_to(x, y + dy)
        ctx.show_text(txt)


# TODO create Line object
def line(ctx, a, b):
    '''
    Create a line segment in the ctx
    :param ctx:
    :param a: start point
    :param b: end point
    :return:
    '''
    ctx.move_to(*a)
    ctx.line_to(*b)

# TODO create Polygon object
def polygon(ctx, points, closed=True):
    '''
    Create a polygon in ths ctx
    :param ctx:
    :param points:
    :param closed:
    :return:
    '''
    first = True
    for p in points:
        if first:
            ctx.move_to(*p)
            first = False
        else:
            ctx.line_to(*p)
    if closed:
        ctx.close_path()


def angle_marker(ctx, a, b, c, count=1, radius=8, gap=2, right_angle=False):
    '''
    Draw an angle marker
    :param ctx: Context
    :param a:
    :param b:
    :param c:
    :param count:
    :param radius:
    :param gap:
    :param rightangle:
    :return:
    '''
    ang1 = math.atan2(a[1] - b[1], a[0] - b[0])
    ang2 = math.atan2(c[1] - b[1], c[0] - b[0])
    ctx.new_path()
    if right_angle:
        radius /= 2
        v = (math.cos(ang1), math.sin(ang1));
        pv = (math.cos(ang2), math.sin(ang2));
        polygon(ctx, [(b[0] + v[0] * radius, b[1] + v[1] * radius),
                      (b[0] + (v[0] + pv[0])*radius, b[1] + (v[1]+pv[1])*radius),
                      (b[0] + pv[0]*radius, b[1] + pv[1]*radius)], False)
    elif count==2:
        ctx.arc(b[0], b[1], radius - gap / 2, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius + gap / 2, ang1, ang2)
    elif count == 3:
        ctx.arc(b[0], b[1], radius - gap, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius + gap, ang1, ang2)
    else:
        ctx.arc(b[0], b[1], radius, ang1, ang2)

def tick(ctx, a, b, count=1, length=4, gap=1):

    # Midpoint of line
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    if count==1:
        pos = (pmid[0], pmid[1])
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2),
             (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2),
             (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0], pmid[1])
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))

def paratick(ctx, a, b, count=1, length=4, gap=1):

    def draw(x, y, ox1, oy1, ox2, oy2):
        line(ctx, (x, y), (x + ox1, y + oy1))
        line(ctx, (x, y), (x + ox2, y + oy2))

    # Midpoint ofgline
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    if count==1:
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)