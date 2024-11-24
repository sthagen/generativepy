# generativepy

Generative art and graphing library for creating images and animations.

## Version 24.11 notes
 
* Fix bug is extents for `of_xy_function`.
* Axes.transform_from_graph can accept a point or a sequence of points.

## Version 24.04 notes

3D drawing is likely to change in a future release. The rest of the library is reasonably stable. 

* Most shapes can now optionally accept `FillParameters` and `StrokeParameters` to control fill and stroke styles. This makes it easier to share styles amongst different objects.
* Add scatter plots, including stalk and connected styles.
* Add a basic `Vector3` implementation to `math` module. 
* New `Markers` class to rationalise line markers (ticks, paraticks, parallel markers), adding new markers and allowing position to be controlled.
* New `overlay_nparrays` function in `nparray` module allows two images to be overlaid, treating pure white as transparent.
* Add 3D charts (z against xy) using `povray`. Also added `complex` module to `genpygoodies` to help with plotting complex graphs
* Add `povray` module with capability of drawing 3D shapes using vapory module.
* `Plot` now has a `close` parameter that creates a polygon area based on a section of the curve that can then be filled. This can be the area under the curve, or above the curve, or any area created be extending the curve with additional points.
* Update docstrings of all modules to support autogenerated documentation on generativepy.com

## Usage

generativepy is a library rather an application. It provides useful functions and example code that allow you to
create images and videos by writing simple Python scripts.

The library requires:

* [pycairo](https://pycairo.readthedocs.io/en/latest/index.html).
* NumPy.
* Pillow.
* easy_vector.
* moderngl (only required for 3D imaging).
* MoviePy
* Command line application gifsicle (only needed for GIF creation).
* Commandline applications latex and divpng

Main functionality:

* A simple framework for creating images, image sequences, and gifs, using pycairo.
* Support for bitmap processing using PIL and NumPy.
* Colour module that supports RGB, HSL and CSS colours, transparency, lerping, colormaps.
* A simple tweening module to help with animation.
* Geometry module for drawing shapes.
* A graphing library for plotting 2D functions.
* MovieBuilder supports creating video files from separate scenes.
* Latex formula rendering
* 3D geometry module using moderngl.
* Math modules for vectors, matrices and abstract shapes. 

## Website

Visit [pythoninformer.com](http://www.pythoninformer.com/generative-art/) for details:

* [generativepy reference](http://www.pythoninformer.com/generative-art/generativepy/).
* [generativepy tutorials](http://www.pythoninformer.com/generative-art/generativepy-tutorial/).

There are also some art examples in the Generative Art section of [my blog](https://martinmcbride.org/).

For detailed information of pycairo see the [Computer graphics in Python](https://leanpub.com/computergraphicsinpython) ebook.
