# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
import cairo
import math

from generativepy.drawing import LEFT, CENTER, RIGHT, BOTTOM, MIDDLE, BASELINE, TOP


class Shape():

    def __init__(self, ctx):
        self.ctx = ctx
        self.new_path = True
        self.new_sub_path = True

    def extend_path(self):
        self.new_path = False

    def as_sub_path(self):
        self.new_sub_path = False

    def _do_path_(self):
        if self.new_path:
            self.ctx.new_path()
        elif self.new_sub_path:
            self.ctx.new_sub_path()

    def add(self):
        raise NotImplementedError()

    def fill(self, color=None):
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
        self.ctx.fill()
        return self

    def stroke(self, color=None, line_width=None):
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
        if line_width != None:
            self.ctx.set_line_width(line_width)
        self.ctx.stroke()
        return self

    def fill_stroke(self, fill_color, stroke_colour, line_width=1):
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
        self._do_path_()
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

class Text(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.text = 'text'
        self.position = (0, 0)
        self._size = None
        self._font = None
        self.alignx = LEFT
        self.aligny = BASELINE
        self._flip = False
        self._offset = (0, 0)

    def add(self):
        self._do_path_()
        if self._font:
            self.ctx.select_font_face(self._font, cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
        if self._size:
            self.ctx.set_font_size(self._size)

        x, y = self.position
        x += self._offset[0]
        y += self._offset[1]
        xb, yb, width, height, dx, dy = self.ctx.text_extents(self.text)

        x -= xb
        if self.alignx == CENTER:
            x -= width / 2
        elif self.alignx == RIGHT:
            x -= width

        if self.aligny == CENTER:
            dy = -yb / 2
        elif self.aligny == BOTTOM:
            dy = -(yb + height)
        elif self.aligny == TOP:
            dy = -yb

        if self._flip:
            self.ctx.move_to(x, y - dy)
            self.ctx.save()
            self.ctx.scale(1, -1)
            self.ctx.text_path(self.text)
            self.ctx.restore()
        else:
            self.ctx.move_to(x, y + dy)
            self.ctx.text_path(self.text)
        return self

    def of(self, text, position):
        self.text = text
        self.position = position
        return self

    def font(self, font):
        self._font = font
        return self

    def size(self, size):
        self._size = size
        return self

    def align(self, alignx, aligny):
        self.alignx = alignx
        self.aligny = aligny
        return self

    def align_left(self):
        self.alignx = LEFT
        return self

    def align_center(self):
        self.alignx = CENTER
        return self

    def align_right(self):
        self.alignx = RIGHT
        return self

    def align_right(self):
        self.alignx = RIGHT
        return self

    def align_bottom(self):
        self.aligny = BOTTOM
        return self

    def align_baseline(self):
        self.aligny = BASELINE
        return self

    def align_middle(self):
        self.aligny = MIDDLE
        return self

    def align_top(self):
        self.aligny = TOP
        return self

    def flip(self):
        self._flip = True
        return self

    def offset(self, x=0, y=0):
        self._offset = (x, y)
        return self



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

    shape = Text(ctx).of(txt, (x, y)).align(alignx, aligny)
    if font:
        shape = shape.font(font)
    if size:
        shape = shape.flip()
    if flip:
        shape = shape.flip()

    if color:
        ctx.set_source_rgba(*color)

    shape.add()
    ctx.fill()


class Line(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.start = (0, 0)
        self.end = (0, 0)

    def add(self):
        self._do_path_()
        self.ctx.move_to(*self.start)
        self.ctx.line_to(*self.end)
        return self

    def of_start_end(self, start, end):
        self.start = start
        self.end = end
        return self


def line(ctx, start, end):
    '''
    Create a line segment in the ctx
    :param ctx:
    :param start: start point
    :param end: end point
    :return:
    '''
    Line(ctx).of_start_end(start, end).add()


class Polygon(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.points = []
        self.closed = True

    def add(self):
        self._do_path_()
        first = True
        for p in self.points:
            if first:
                self.ctx.move_to(*p)
                first = False
            else:
                self.ctx.line_to(*p)
        if self.closed:
            self.ctx.close_path()
        return self

    def of_points(self, points):
        self.points = points
        return self

    def open(self):
        self.closed = False
        return self


def polygon(ctx, points, closed=True):
    '''
    Create a polygon in ths ctx
    :param ctx:
    :param points:
    :param closed:
    :return:
    '''
    shape = Polygon(ctx).of_points(points)
    if not closed:
        shape.open()
    shape.add()


class Circle(Shape):

    arc = 1
    sector = 2
    segment = 3

    def __init__(self, ctx):
        super().__init__(ctx)
        self.center = (0, 0)
        self.radius = 0
        self.start_angle = 0
        self.end_angle = 2*math.pi
        self.type = Circle.arc

    def add(self):
        self._do_path_()
        if self.type == Circle.sector:
            self.ctx.move_to(*self.center)
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
            self.ctx.close_path()
        elif self.type == Circle.segment:
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
            self.ctx.close_path()
        else:
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
        return self

    def of_center_radius(self, center, radius):
        self.center = center
        self.radius = radius
        return self

    def as_arc(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.arc
        return self

    def as_sector(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.sector
        return self

    def as_segment(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.segment
        return self

def circle(ctx, center, radius):
    '''
    Create a circle in ths ctx
    :param ctx:
    :param center:
    :param radius:
    :return:
    '''
    Circle(ctx).of_center_radius(center, radius).add()


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