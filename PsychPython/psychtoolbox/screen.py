"""Pythonic wrapper for Psychtoolbox Screen functions

This module provides a more Pythonic interface to the Screen module,
keeping the MATLAB-style workflow where windows are just references.

Example usage::

    from psychtoolbox.screen import PTBScreen

    # Create a screen interface
    screen = PTBScreen()

    # Open a window (returns window pointer like MATLAB)
    window_ptr, rect = screen.open_window(screen_number=0, color=[128, 128, 128])

    # Create and draw textures (pass window pointer like MATLAB)
    texture = screen.make_texture(window_ptr, image_matrix)
    screen.draw_texture(window_ptr, t        # Process lenient
        if lenient is not None:
            lenient = float(lenient[0]) if hasattr(lenient, "__len__") else float(lenient)ure)
    screen.flip(window_ptr)

    # Clean up
    screen.close(window_ptr)
    # or close all
    screen.close_all()

(c) 2025 - Licensed under MIT license.
"""

import atexit
import numpy as np
from pathlib import Path
import yaml
from . import Screen


def _is_instantiated(val):
    if not val:
        if val is None:
            return False
        elif hasattr(val, "__len__"):
            return len(val) > 0
    return True


def _coerce_to_float(val, check_length=None):
    if _is_instantiated(val):
        if check_length is not None:
            if not hasattr(val, "__len__") or len(val) != check_length:
                raise ValueError(f"Argument must be a list of length {check_length}")

        if hasattr(val, "__len__"):
            val = [float(x) for x in val]
        else:
            val = float(val)
    else:
        val = []

    return val


class PTBScreen:
    """Screen interface class providing pythonic access to Screen functions"""

    DISPLAY_MAPPING_CONFIG = Path("~/.Psychtoolbox/display_mapping.yaml").expanduser()

    def __init__(self):
        atexit.register(self.close_all)

        if PTBScreen.DISPLAY_MAPPING_CONFIG.is_file():
            with open(PTBScreen.DISPLAY_MAPPING_CONFIG, "r") as f:
                self.display_mapping = yaml.safe_load(f)
        else:
            self.display_mapping = {}

    # No complex helper function needed - just use default arguments!

    def get_version(self):
        """Get Screen module version information"""
        return Screen("Version")

    def version(self):
        """Get Screen module version information (alias for get_version)"""
        return self.get_version()

    def screens(self, physical_displays=None):
        """Get list of available screen numbers"""
        if physical_displays is not None:
            return Screen("Screens", physical_displays)
        return Screen("Screens")

    def windows(self):
        """Get list of open window pointers"""
        return Screen("Windows")

    def preference(self, preference_name, *args):
        """Get or set Screen preferences

        Args:
            preference_name: Name of preference to get/set
            *args: Optional new value(s) for the preference

        Returns:
            Old value of the preference
        """
        return Screen("Preference", preference_name, *args)

    def open_window(
        self,
        screen_number,
        color=[],
        rect=[],
        pixel_size=[],
        num_buffers=[],
        stereo_mode=[],
        multisample=[],
        imaging_mode=[],
        special_flags=[],
        client_rect=[],
        fb_override_rect=[],
        vrr_params=[],
    ):
        """Open a new onscreen window (like MATLAB Screen('OpenWindow', ...))

        Args:
            screen_number: Screen to open window on
            color: Background color [R, G, B] or [R, G, B, A]
            rect: Window rectangle [left, top, right, bottom]
            pixel_size: Pixel depth in bits
            num_buffers: Number of buffers for page flipping
            stereo_mode: Stereo display mode
            multisample: Multisample anti-aliasing samples
            imaging_mode: Imaging pipeline mode
            special_flags: Special flags for window creation
            client_rect: Client area rectangle
            fb_override_rect: Framebuffer override rectangle
            vrr_params: Variable refresh rate parameters

        Returns:
            Tuple of (window_ptr, rect) - window_ptr is used for subsequent calls
        """

        screen_number_int = int(screen_number)
        if self.display_mapping:
            if screen_number_int in self.display_mapping.keys():
                self.preference(
                    "ScreenToHead",
                    float(screen_number),
                    float(self.display_mapping[screen_number_int]["head"]),
                    float(self.display_mapping[screen_number_int]["crtc"]),
                )

        color = _coerce_to_float(color)
        rect = _coerce_to_float(rect, check_length=4)
        pixel_size = _coerce_to_float(pixel_size)
        num_buffers = _coerce_to_float(num_buffers)
        stereo_mode = _coerce_to_float(stereo_mode)
        multisample = _coerce_to_float(multisample)
        imaging_mode = _coerce_to_float(imaging_mode)
        special_flags = _coerce_to_float(special_flags)
        client_rect = _coerce_to_float(client_rect, check_length=4)
        fb_override_rect = _coerce_to_float(fb_override_rect, check_length=4)
        vrr_params = _coerce_to_float(vrr_params)

        return Screen(
            "OpenWindow",
            screen_number,
            color,
            rect,
            pixel_size,
            num_buffers,
            stereo_mode,
            multisample,
            imaging_mode,
            special_flags,
            client_rect,
            fb_override_rect,
            vrr_params,
        )

    # def open_offscreen_window(
    #     self,
    #     parent_window_or_screen,
    #     color=[],
    #     rect=[],
    #     pixel_size=[],
    #     special_flags=[],
    #     multisample=[],
    # ):
    #     """Open a new offscreen window (like MATLAB Screen('OpenOffscreenWindow', ...))

    #     Args:
    #         parent_window_or_screen: Parent window pointer or screen number
    #         color: Background color [R, G, B] or [R, G, B, A]
    #         rect: Window rectangle [left, top, right, bottom]
    #         pixel_size: Pixel depth in bits
    #         special_flags: Special flags for window creation
    #         multisample: Multisample anti-aliasing samples

    #     Returns:
    #         Tuple of (window_ptr, rect) - window_ptr is used for subsequent calls
    #     """
    #     # Convert color to proper numpy array format if provided
    #     if color and len(color) > 0:
    #         color = np.array(color, dtype=np.uint8)

    #     # Convert rect to proper format if provided
    #     if rect and len(rect) > 0:
    #         rect = np.array(rect, dtype=np.float64)

    #     return Screen(
    #         "OpenOffscreenWindow",
    #         parent_window_or_screen,
    #         color,
    #         rect,
    #         pixel_size,
    #         special_flags,
    #         multisample,
    #     )

    def close(self, window_ptr):
        """Close a specific window (like MATLAB Screen('Close', window_ptr))

        Args:
            window_ptr: Window pointer to close
        """
        return Screen("Close", window_ptr)

    def close_all(self):
        """Close all windows and textures (like MATLAB Screen('CloseAll'))"""
        return Screen("CloseAll")

    def make_texture(
        self,
        window_ptr,
        image_matrix,
        optimize_angle=0,
        special_flags=0,
        float_precision=[],
        texture_orientation=0,
        texture_shader=0,
    ):
        """Create a texture from an image matrix (like MATLAB Screen('MakeTexture', ...))

        Args:
            window_ptr: Window pointer where texture will be used
            image_matrix: Image data as numpy array
            optimize_angle: Optimize for drawing at this angle
            special_flags: Special flags for texture creation
            float_precision: Float precision for texture ([] for default)
            texture_orientation: Texture orientation
            texture_shader: Texture shader to use

        Returns:
            texture_index: Texture reference for use in draw_texture
        """
        image_matrix = np.array(image_matrix, dtype=np.float32).tolist()
        optimize_angle = _coerce_to_float(optimize_angle)
        special_flags = _coerce_to_float(special_flags)
        float_precision = _coerce_to_float(float_precision)
        texture_orientation = _coerce_to_float(texture_orientation)
        texture_shader = _coerce_to_float(texture_shader)

        return Screen(
            "MakeTexture",
            window_ptr,
            image_matrix,
            optimize_angle,
            special_flags,
            float_precision,
            texture_orientation,
            texture_shader,
        )

    def draw_texture(
        self,
        window_ptr,
        texture_index,
        source_rect=[],
        dest_rect=[],
        rotation_angle=[],
        filter_mode=[],
        global_alpha=[],
        modulate_color=[],
        texture_shader=[],
        special_flags=[],
        aux_parameters=[],
    ):
        """Draw a texture to the window (like MATLAB Screen('DrawTexture', ...))

        Args:
            window_ptr: Window pointer to draw on
            texture_index: Texture index to draw
            source_rect: Source rectangle [left, top, right, bottom]
            dest_rect: Destination rectangle [left, top, right, bottom]
            rotation_angle: Rotation angle in degrees
            filter_mode: Texture filtering mode
            global_alpha: Global alpha transparency
            modulate_color: Color modulation [R, G, B] or [R, G, B, A]
            texture_shader: Texture shader to use
            special_flags: Special flags for drawing
            aux_parameters: Auxiliary parameters
        """
        source_rect = _coerce_to_float(source_rect, check_length=4)
        dest_rect = _coerce_to_float(dest_rect, check_length=4)
        rotation_angle = _coerce_to_float(rotation_angle)
        filter_mode = _coerce_to_float(filter_mode)
        global_alpha = _coerce_to_float(global_alpha)
        modulate_color = _coerce_to_float(modulate_color)
        texture_shader = _coerce_to_float(texture_shader)
        special_flags = _coerce_to_float(special_flags)
        aux_parameters = _coerce_to_float(aux_parameters)

        return Screen(
            "DrawTexture",
            window_ptr,
            texture_index,
            source_rect,
            dest_rect,
            rotation_angle,
            filter_mode,
            global_alpha,
            modulate_color,
            texture_shader,
            special_flags,
            aux_parameters,
        )

    def draw_textures(
        self,
        window_ptr,
        texture_indices,
        source_rects=[],
        dest_rects=[],
        rotation_angles=[],
        filter_modes=[],
        global_alphas=[],
        modulate_colors=[],
        texture_shader=[],
        special_flags=[],
        aux_parameters=[],
    ):
        """Draw multiple textures efficiently (like MATLAB Screen('DrawTextures', ...))

        Args:
            window_ptr: Window pointer to draw on
            texture_indices: List of texture indices to draw
            source_rects: Source rectangles for each texture
            dest_rects: Destination rectangles for each texture
            rotation_angles: Rotation angles for each texture
            filter_modes: Filter modes for each texture
            global_alphas: Global alpha values for each texture
            modulate_colors: Color modulations for each texture
            texture_shader: Texture shader to use
            special_flags: Special flags for drawing
            aux_parameters: Auxiliary parameters
        """

        texture_indices = _coerce_to_float(texture_indices)
        source_rects = [_coerce_to_float(rect, check_length=4) for rect in source_rects]
        dest_rects = [_coerce_to_float(rect, check_length=4) for rect in dest_rects]
        rotation_angles = _coerce_to_float(rotation_angles)
        filter_modes = _coerce_to_float(filter_modes)
        global_alphas = _coerce_to_float(global_alphas)
        modulate_colors = [_coerce_to_float(color) for color in modulate_colors]
        texture_shader = _coerce_to_float(texture_shader)
        special_flags = _coerce_to_float(special_flags)
        aux_parameters = _coerce_to_float(aux_parameters)

        return Screen(
            "DrawTextures",
            window_ptr,
            texture_indices,
            source_rects,
            dest_rects,
            rotation_angles,
            filter_modes,
            global_alphas,
            modulate_colors,
            texture_shader,
            special_flags,
            aux_parameters,
        )

    def flip(self, window_ptr, when=[], dont_clear=[], dont_sync=[], multiflip=[]):
        """Flip the front and back buffers (like MATLAB Screen('Flip', ...))

        Args:
            window_ptr: Window pointer to flip
            when: When to flip (timestamp)
            dont_clear: Don't clear after flip
            dont_sync: Don't sync to VBL
            multiflip: Multiflip count

        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        when = _coerce_to_float(when)
        dont_clear = _coerce_to_float(dont_clear)
        dont_sync = _coerce_to_float(dont_sync)
        multiflip = _coerce_to_float(multiflip)

        return Screen("Flip", window_ptr, when, dont_clear, dont_sync, multiflip)

    def flip_async_begin(
        self, window_ptr, when=[], dont_clear=[], dont_sync=[], multiflip=[]
    ):
        """Begin asynchronous flip (like MATLAB Screen('AsyncFlipBegin', ...))

        Args:
            window_ptr: Window pointer to flip
            when: When to flip (timestamp)
            dont_clear: Don't clear after flip
            dont_sync: Don't sync to VBL
            multiflip: Multiflip count

        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        when = _coerce_to_float(when)
        dont_clear = _coerce_to_float(dont_clear)
        dont_sync = _coerce_to_float(dont_sync)
        multiflip = _coerce_to_float(multiflip)

        return Screen(
            "AsyncFlipBegin", window_ptr, when, dont_clear, dont_sync, multiflip
        )

    def flip_async_end(self, window_ptr):
        """End asynchronous flip (like MATLAB Screen('AsyncFlipEnd', ...))

        Args:
            window_ptr: Window pointer

        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        return Screen("AsyncFlipEnd", window_ptr)

    def flip_async_check_end(self, window_ptr):
        """Check if asynchronous flip has ended (like MATLAB Screen('AsyncFlipCheckEnd', ...))

        Args:
            window_ptr: Window pointer

        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        return Screen("AsyncFlipCheckEnd", window_ptr)

    def wait_until_async_flip_certain(self, window_ptr):
        """Wait until async flip is certain to happen (like MATLAB Screen('WaitUntilAsyncFlipCertain', ...))

        Args:
            window_ptr: Window pointer

        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, swapCertainTime)
        """
        return Screen("WaitUntilAsyncFlipCertain", window_ptr)

    def drawing_finished(self, window_ptr, dont_clear=[], sync=[]):
        """Wait for drawing operations to finish (like MATLAB Screen('DrawingFinished', ...))

        Args:
            window_ptr: Window pointer
            dont_clear: Don't clear after finish
            sync: Sync mode

        Returns:
            Time elapsed
        """
        dont_clear = _coerce_to_float(dont_clear)
        sync = _coerce_to_float(sync)
        return Screen("DrawingFinished", window_ptr, dont_clear, sync)

    # Drawing primitives - all take window_ptr as first argument like MATLAB
    def fill_rect(self, window_ptr, color=[], rect=[]):
        """Fill a rectangle with color (like MATLAB Screen('FillRect', ...))"""
        color = _coerce_to_float(color)
        rect = _coerce_to_float(rect, check_length=4)
        Screen("FillRect", window_ptr, color, rect)

    def frame_rect(self, window_ptr, color=[], rect=[], pen_width=[]):
        """Draw rectangle outline (like MATLAB Screen('FrameRect', ...))"""
        color = _coerce_to_float(color)
        rect = _coerce_to_float(rect, check_length=4)
        pen_width = _coerce_to_float(pen_width)
        Screen("FrameRect", window_ptr, color, rect, pen_width)

    def fill_oval(self, window_ptr, color=[], rect=[], perfect_up_to_max_diameter=[]):
        """Fill an oval with color (like MATLAB Screen('FillOval', ...))"""
        color = _coerce_to_float(color)
        rect = _coerce_to_float(rect, check_length=4)
        perfect_up_to_max_diameter = _coerce_to_float(perfect_up_to_max_diameter)
        Screen("FillOval", window_ptr, color, rect, perfect_up_to_max_diameter)

    def frame_oval(
        self,
        window_ptr,
        color=[],
        rect=[],
        pen_width=[],
        pen_height=[],
        pen_mode=[],
    ):
        """Draw oval outline (like MATLAB Screen('FrameOval', ...))"""
        color = _coerce_to_float(color)
        rect = _coerce_to_float(rect, check_length=4)
        pen_width = _coerce_to_float(pen_width)
        pen_height = _coerce_to_float(pen_height)
        pen_mode = _coerce_to_float(pen_mode)
        Screen("FrameOval", window_ptr, color, rect, pen_width, pen_height, pen_mode)

    def draw_line(
        self,
        window_ptr,
        color=[],
        from_h=[],
        from_v=[],
        to_h=[],
        to_v=[],
        pen_width=[],
    ):
        """Draw a line (like MATLAB Screen('DrawLine', ...))"""
        color = _coerce_to_float(color)
        from_h = _coerce_to_float(from_h)
        from_v = _coerce_to_float(from_v)
        to_h = _coerce_to_float(to_h)
        to_v = _coerce_to_float(to_v)
        pen_width = _coerce_to_float(pen_width)

        Screen("DrawLine", window_ptr, color, from_h, from_v, to_h, to_v, pen_width)

    def draw_dots(
        self,
        window_ptr,
        xy,
        size=[],
        color=[],
        center=[],
        dot_type=[],
        lenient=[],
    ):
        """Draw dots/points efficiently (like MATLAB Screen('DrawDots', ...))

        Args:
            window_ptr: Window pointer to draw on
            xy: 2xN array of [x, y] coordinates
            size: Dot size(s)
            color: Dot color(s)
            center: Center coordinates
            dot_type: Type of dots to draw
            lenient: Lenient mode

        Returns:
            Tuple of dot size limits
        """
        xy = xy.T if xy.shape[0] != 2 else xy
        xy = xy.astype(np.float32).tolist()

        # Process arguments using the helper function
        size = _coerce_to_float(size)
        color = _coerce_to_float(color)
        center = _coerce_to_float(center)
        dot_type = _coerce_to_float(dot_type)
        lenient = _coerce_to_float(lenient)

        return Screen(
            "DrawDots", window_ptr, xy, size, color, center, dot_type, lenient
        )

    def draw_lines(
        self,
        window_ptr,
        xy,
        width=[],
        colors=[],
        center=[],
        smooth=[],
        lenient=[],
    ):
        """Draw lines efficiently (like MATLAB Screen('DrawLines', ...))

        Args:
            window_ptr: Window pointer to draw on
            xy: 4xN array of [x1, y1, x2, y2] coordinates
            width: Line width(s)
            colors: Line color(s)
            center: Center coordinates
            smooth: Smooth lines
            lenient: Lenient mode

        Returns:
            Tuple of line width limits
        """
        if xy.shape[0] != 2:
            raise ValueError(
                f"xy must be a 2xN array of coordinates, got shape {xy.shape}"
            )

        xy = [[float(v) for v in row] for row in xy]

        # Process arguments using the helper function
        width = _coerce_to_float(width)
        colors = _coerce_to_float(colors)
        center = _coerce_to_float(center)
        smooth = _coerce_to_float(smooth)
        lenient = _coerce_to_float(lenient)

        return Screen(
            "DrawLines", window_ptr, xy, width, colors, center, smooth, lenient
        )

    # # Text drawing - all take window_ptr as first argument like MATLAB
    # def draw_text(
    #     self,
    #     window_ptr,
    #     text,
    #     x=None,
    #     y=None,
    #     color=None,
    #     background_color=None,
    #     y_position_is_baseline=None,
    #     swap_text_direction=None,
    # ):
    #     """Draw text to the window (like MATLAB Screen('DrawText', ...))

    #     Args:
    #         window_ptr: Window pointer to draw on
    #         text: Text string to draw
    #         x: X position
    #         y: Y position
    #         color: Text color
    #         background_color: Background color
    #         y_position_is_baseline: Y position is baseline
    #         swap_text_direction: Swap text direction

    #     Returns:
    #         Tuple of (newX, newY, textHeight)
    #     """
    #     args = [window_ptr, text]
    #     if x is not None:
    #         args.append(float(x))
    #     if y is not None:
    #         args.append(float(y))
    #     if color is not None:
    #         if hasattr(color, "__len__"):
    #             color = list(color)
    #             color = [float(c) for c in color]
    #         else:
    #             color = float(color)
    #         args.append(color)
    #     if background_color is not None:
    #         if hasattr(background_color, "__len__"):
    #             background_color = list(background_color)
    #             background_color = [float(c) for c in background_color]
    #         else:
    #             background_color = float(background_color)
    #         args.append(background_color)
    #     if y_position_is_baseline is not None:
    #         args.append(float(y_position_is_baseline))
    #     if swap_text_direction is not None:
    #         args.append(float(swap_text_direction))

    #     return Screen("DrawText", *args)

    # def text_bounds(
    #     self,
    #     window_ptr,
    #     text,
    #     x=[],
    #     y=[],
    #     y_position_is_baseline=[],
    #     swap_text_direction=[],
    # ):
    #     """Get text bounding rectangle (like MATLAB Screen('TextBounds', ...))"""
    #     x = _coerce_to_float(x)
    #     y = _coerce_to_float(y)
    #     y_position_is_baseline = _coerce_to_float(y_position_is_baseline)
    #     swap_text_direction = _coerce_to_float(swap_text_direction)
    #     return Screen(
    #         "TextBounds",
    #         window_ptr,
    #         text,
    #         x,
    #         y,
    #         y_position_is_baseline,
    #         swap_text_direction,
    #     )

    # # Text formatting - all take window_ptr as first argument like MATLAB
    # def text_size(self, window_ptr, size=[]):
    #     """Get or set text size (like MATLAB Screen('TextSize', ...))"""
    #     size = _coerce_to_float(size)
    #     return Screen("TextSize", window_ptr, size)

    # def text_font(self, window_ptr, font_name_or_number=[], text_style=[]):
    #     """Get or set text font (like MATLAB Screen('TextFont', ...))"""
    #     font_name_or_number = (
    #         _coerce_to_float(font_name_or_number)
    #         if type(font_name_or_number) is int
    #         else font_name_or_number
    #     )
    #     text_style = _coerce_to_float(text_style)
    #     return Screen("TextFont", window_ptr, font_name_or_number, text_style)

    # def text_color(self, window_ptr, color=[]):
    #     """Get or set text color (like MATLAB Screen('TextColor', ...))"""
    #     color = _coerce_to_float(color)
    #     return Screen("TextColor", window_ptr, color)

    # def text_background_color(self, window_ptr, color=[]):
    #     """Get or set text background color (like MATLAB Screen('TextBackgroundColor', ...))"""
    #     color = _coerce_to_float(color)
    #     return Screen("TextBackgroundColor", window_ptr, color)

    # Image operations - all take window_ptr as first argument like MATLAB
    def get_image(
        self, window_ptr, rect=[], buffer_name=[], float_precision=0, num_channels=3
    ):
        """Get image from window as numpy array (like MATLAB Screen('GetImage', ...))

        Args:
            window_ptr: Window pointer to read from
            rect: Rectangle to capture
            buffer_name: Buffer to read from
            float_precision: Float precision
            num_channels: Number of channels

        Returns:
            Image as numpy array
        """
        rect = _coerce_to_float(rect, check_length=4)
        buffer_name = _coerce_to_float(buffer_name)
        float_precision = _coerce_to_float(float_precision)
        num_channels = _coerce_to_float(num_channels)
        return Screen(
            "GetImage", window_ptr, rect, buffer_name, float_precision, num_channels
        )

    def put_image(self, window_ptr, image_array, rect=[]):
        """Put image array into window (like MATLAB Screen('PutImage', ...))

        Args:
            window_ptr: Window pointer to write to
            image_array: Image data as numpy array
            rect: Destination rectangle
        """
        image_array = np.array(image_array, dtype=np.float32).tolist()
        rect = _coerce_to_float(rect, check_length=4)
        Screen("PutImage", window_ptr, image_array, rect)

    # Window information functions
    def window_kind(self, window_ptr):
        """Get window kind (like MATLAB Screen(window_ptr, 'WindowKind'))"""
        return Screen(window_ptr, "WindowKind")

    def is_offscreen(self, window_ptr):
        """Check if window is offscreen (like MATLAB Screen(window_ptr, 'IsOffscreen'))"""
        return Screen(window_ptr, "IsOffscreen")

    def window_size(self, window_ptr, real_fb_size=0):
        """Get window size (like MATLAB Screen('WindowSize', ...))"""
        real_fb_size = _coerce_to_float(real_fb_size, check_length=2)
        return Screen("WindowSize", window_ptr, real_fb_size)

    def pixel_size(self, window_ptr):
        """Get pixel size (like MATLAB Screen('PixelSize', ...))"""
        return Screen("PixelSize", window_ptr)

    def get_flip_interval(self, window_ptr, num_samples=[], std_dev=[], timeout=[]):
        """Get monitor flip interval (like MATLAB Screen('GetFlipInterval', ...))"""
        num_samples = _coerce_to_float(num_samples)
        std_dev = _coerce_to_float(std_dev)
        timeout = _coerce_to_float(timeout)
        return Screen("GetFlipInterval", window_ptr, num_samples, std_dev, timeout)

    # Gamma and color functions
    def read_normalized_gamma_table(
        self, window_ptr_or_screen_number, physical_display=[]
    ):
        """Read normalized gamma table (like MATLAB Screen('ReadNormalizedGammaTable', ...))"""
        physical_display = _coerce_to_float(physical_display)
        return Screen(
            "ReadNormalizedGammaTable", window_ptr_or_screen_number, physical_display
        )

    def load_normalized_gamma_table(
        self,
        window_ptr_or_screen_number,
        table,
        load_on_next_flip=[],
        physical_display=[],
        ignore_errors=[],
    ):
        """Load normalized gamma table (like MATLAB Screen('LoadNormalizedGammaTable', ...))"""
        load_on_next_flip = _coerce_to_float(load_on_next_flip)
        physical_display = _coerce_to_float(physical_display)
        ignore_errors = _coerce_to_float(ignore_errors)
        return Screen(
            "LoadNormalizedGammaTable",
            window_ptr_or_screen_number,
            table,
            load_on_next_flip,
            physical_display,
            ignore_errors,
        )

    # Other utility functions
    def rect(self, window_ptr_or_screen_number, real_fb_size=0):
        """Get rectangle (like MATLAB Screen('Rect', ...))"""
        real_fb_size = _coerce_to_float(real_fb_size, check_length=2)
        return Screen("Rect", window_ptr_or_screen_number, real_fb_size)


# Convenience functions that don't require a PTBScreen instance
def get_screens():
    """Get list of available screens"""
    return Screen("Screens")


def get_version():
    """Get Screen module version"""
    return Screen("Version")
