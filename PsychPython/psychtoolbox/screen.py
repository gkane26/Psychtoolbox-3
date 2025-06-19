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
    screen.draw_texture(window_ptr, texture)
    screen.flip(window_ptr)
    
    # Clean up
    screen.close(window_ptr)
    # or close all
    screen.close_all()

(c) 2025 - Licensed under MIT license.
"""

import atexit
import numpy as np
from . import Screen


class PTBScreen:
    """Screen interface class providing pythonic access to Screen functions"""
    
    def __init__(self):
        atexit.register(self.close_all)
    
    # No complex helper function needed - just use default arguments!
    
    
    def get_version(self):
        """Get Screen module version information"""
        return Screen('Version')
    
    def version(self):
        """Get Screen module version information (alias for get_version)"""
        return self.get_version()
    
    def screens(self, physical_displays=None):
        """Get list of available screen numbers"""
        if physical_displays is not None:
            return Screen('Screens', physical_displays)
        return Screen('Screens')
    
    def windows(self):
        """Get list of open window pointers"""
        return Screen('Windows')
    
    def preference(self, preference_name, *args):
        """Get or set Screen preferences
        
        Args:
            preference_name: Name of preference to get/set
            *args: Optional new value(s) for the preference
        
        Returns:
            Old value of the preference
        """
        return Screen('Preference', preference_name, *args)
    
    def open_window(self, screen_number, color=[], rect=[], pixel_size=[], 
                   num_buffers=[], stereo_mode=[], multisample=[],
                   imaging_mode=[], special_flags=[], client_rect=[],
                   fb_override_rect=[], vrr_params=[]):
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
        # Convert color to proper numpy array format if provided
        if color and len(color) > 0:
            color = np.array(color, dtype=np.uint8)
        
        # Convert rect to proper format if provided
        if rect and len(rect) > 0:
            rect = np.array(rect, dtype=np.float64)
        
        return Screen('OpenWindow', screen_number, color, rect, pixel_size, 
                     num_buffers, stereo_mode, multisample, imaging_mode, 
                     special_flags, client_rect, fb_override_rect, vrr_params)
    
    def open_offscreen_window(self, parent_window_or_screen, color=[], rect=[],
                             pixel_size=[], special_flags=[], multisample=[]):
        """Open a new offscreen window (like MATLAB Screen('OpenOffscreenWindow', ...))
        
        Args:
            parent_window_or_screen: Parent window pointer or screen number
            color: Background color [R, G, B] or [R, G, B, A]
            rect: Window rectangle [left, top, right, bottom]
            pixel_size: Pixel depth in bits
            special_flags: Special flags for window creation
            multisample: Multisample anti-aliasing samples
        
        Returns:
            Tuple of (window_ptr, rect) - window_ptr is used for subsequent calls
        """
        # Convert color to proper numpy array format if provided
        if color and len(color) > 0:
            color = np.array(color, dtype=np.uint8)
        
        # Convert rect to proper format if provided
        if rect and len(rect) > 0:
            rect = np.array(rect, dtype=np.float64)
        
        return Screen('OpenOffscreenWindow', parent_window_or_screen, color, rect,
                     pixel_size, special_flags, multisample)
    
    def close(self, window_ptr):
        """Close a specific window (like MATLAB Screen('Close', window_ptr))
        
        Args:
            window_ptr: Window pointer to close
        """
        Screen('Close', window_ptr)
    
    def close_all(self):
        """Close all windows and textures (like MATLAB Screen('CloseAll'))"""
        try:
            Screen('CloseAll')
        except:
            pass  # Ignore errors during cleanup
    
    def make_texture(self, window_ptr, image_matrix, optimize_angle=0, special_flags=0,
                    float_precision=[], texture_orientation=0, texture_shader=0):
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
        return Screen('MakeTexture', window_ptr, image_matrix, optimize_angle, 
                     special_flags, float_precision, texture_orientation, texture_shader)
    
    
    def draw_texture(self, window_ptr, texture_index, source_rect=None, dest_rect=None,
                    rotation_angle=None, filter_mode=None, global_alpha=None,
                    modulate_color=None, texture_shader=None, special_flags=None,
                    aux_parameters=None):
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
        args = [window_ptr, texture_index]
        if source_rect is not None:
            args.append(source_rect)
        if dest_rect is not None:
            args.append(dest_rect)
        if rotation_angle is not None:
            args.append(rotation_angle)
        if filter_mode is not None:
            args.append(filter_mode)
        if global_alpha is not None:
            args.append(global_alpha)
        if modulate_color is not None:
            args.append(modulate_color)
        if texture_shader is not None:
            args.append(texture_shader)
        if special_flags is not None:
            args.append(special_flags)
        if aux_parameters is not None:
            args.append(aux_parameters)
            
        Screen('DrawTexture', *args)
    
    def draw_textures(self, window_ptr, texture_indices, source_rects=None, dest_rects=None,
                     rotation_angles=None, filter_modes=None, global_alphas=None,
                     modulate_colors=None, texture_shader=None, special_flags=None,
                     aux_parameters=None):
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
        args = [window_ptr, texture_indices]
        if source_rects is not None:
            args.append(source_rects)
        if dest_rects is not None:
            args.append(dest_rects)
        if rotation_angles is not None:
            args.append(rotation_angles)
        if filter_modes is not None:
            args.append(filter_modes)
        if global_alphas is not None:
            args.append(global_alphas)
        if modulate_colors is not None:
            args.append(modulate_colors)
        if texture_shader is not None:
            args.append(texture_shader)
        if special_flags is not None:
            args.append(special_flags)
        if aux_parameters is not None:
            args.append(aux_parameters)
            
        Screen('DrawTextures', *args)
    
    def flip(self, window_ptr, when=None, dont_clear=None, dont_sync=None, multiflip=None):
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
        args = [window_ptr]
        if when is not None:
            args.append(when)
        if dont_clear is not None:
            args.append(dont_clear)
        if dont_sync is not None:
            args.append(dont_sync)
        if multiflip is not None:
            args.append(multiflip)
            
        return Screen('Flip', *args)
    
    def flip_async_begin(self, window_ptr, when=None, dont_clear=None, dont_sync=None, multiflip=None):
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
        args = [window_ptr]
        if when is not None:
            args.append(when)
        if dont_clear is not None:
            args.append(dont_clear)
        if dont_sync is not None:
            args.append(dont_sync)
        if multiflip is not None:
            args.append(multiflip)
            
        return Screen('AsyncFlipBegin', *args)
    
    def flip_async_end(self, window_ptr):
        """End asynchronous flip (like MATLAB Screen('AsyncFlipEnd', ...))
        
        Args:
            window_ptr: Window pointer
        
        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        return Screen('AsyncFlipEnd', window_ptr)
    
    def flip_async_check_end(self, window_ptr):
        """Check if asynchronous flip has ended (like MATLAB Screen('AsyncFlipCheckEnd', ...))
        
        Args:
            window_ptr: Window pointer
        
        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos)
        """
        return Screen('AsyncFlipCheckEnd', window_ptr)
    
    def wait_until_async_flip_certain(self, window_ptr):
        """Wait until async flip is certain to happen (like MATLAB Screen('WaitUntilAsyncFlipCertain', ...))
        
        Args:
            window_ptr: Window pointer
        
        Returns:
            Tuple of (VBLTimestamp, StimulusOnsetTime, swapCertainTime)
        """
        return Screen('WaitUntilAsyncFlipCertain', window_ptr)
    
    def drawing_finished(self, window_ptr, dont_clear=None, sync=None):
        """Wait for drawing operations to finish (like MATLAB Screen('DrawingFinished', ...))
        
        Args:
            window_ptr: Window pointer
            dont_clear: Don't clear after finish
            sync: Sync mode
        
        Returns:
            Time elapsed
        """
        args = [window_ptr]
        if dont_clear is not None:
            args.append(dont_clear)
        if sync is not None:
            args.append(sync)
            
        return Screen('DrawingFinished', *args)

    
    # Drawing primitives - all take window_ptr as first argument like MATLAB
    def fill_rect(self, window_ptr, color=None, rect=None):
        """Fill a rectangle with color (like MATLAB Screen('FillRect', ...))"""
        args = [window_ptr]
        if color is not None:
            # Convert color to proper format
            if isinstance(color, (list, tuple)) and len(color) > 0:
                color = np.array(color, dtype=np.uint8)
            args.append(color)
        if rect is not None:
            # Convert rect to proper format
            if isinstance(rect, (list, tuple)) and len(rect) > 0:
                rect = np.array(rect, dtype=np.float64)
            args.append(rect)
        Screen('FillRect', *args)
    
    def frame_rect(self, window_ptr, color=None, rect=None, pen_width=None):
        """Draw rectangle outline (like MATLAB Screen('FrameRect', ...))"""
        args = [window_ptr]
        if color is not None:
            # Convert color to proper format
            if isinstance(color, (list, tuple)) and len(color) > 0:
                color = np.array(color, dtype=np.uint8)
            args.append(color)
        if rect is not None:
            # Convert rect to proper format
            if isinstance(rect, (list, tuple)) and len(rect) > 0:
                rect = np.array(rect, dtype=np.float64)
            args.append(rect)
        if pen_width is not None:
            args.append(pen_width)
        Screen('FrameRect', *args)
    
    def fill_oval(self, window_ptr, color=None, rect=None, perfect_up_to_max_diameter=None):
        """Fill an oval with color (like MATLAB Screen('FillOval', ...))"""
        args = [window_ptr]
        if color is not None:
            # Convert color to proper format
            if isinstance(color, (list, tuple)) and len(color) > 0:
                color = np.array(color, dtype=np.uint8)
            args.append(color)
        if rect is not None:
            # Convert rect to proper format
            if isinstance(rect, (list, tuple)) and len(rect) > 0:
                rect = np.array(rect, dtype=np.float64)
            args.append(rect)
        if perfect_up_to_max_diameter is not None:
            args.append(perfect_up_to_max_diameter)
        Screen('FillOval', *args)
    
    def frame_oval(self, window_ptr, color=None, rect=None, pen_width=None, pen_height=None, pen_mode=None):
        """Draw oval outline (like MATLAB Screen('FrameOval', ...))"""
        args = [window_ptr]
        if color is not None:
            # Convert color to proper format
            if isinstance(color, (list, tuple)) and len(color) > 0:
                color = np.array(color, dtype=np.uint8)
            args.append(color)
        if rect is not None:
            # Convert rect to proper format
            if isinstance(rect, (list, tuple)) and len(rect) > 0:
                rect = np.array(rect, dtype=np.float64)
            args.append(rect)
        if pen_width is not None:
            args.append(pen_width)
        if pen_height is not None:
            args.append(pen_height)
        if pen_mode is not None:
            args.append(pen_mode)
        Screen('FrameOval', *args)
    
    def draw_line(self, window_ptr, color=None, from_h=None, from_v=None, to_h=None, to_v=None, pen_width=None):
        """Draw a line (like MATLAB Screen('DrawLine', ...))"""
        args = [window_ptr]
        if color is not None:
            # Convert color to proper format
            if isinstance(color, (list, tuple)) and len(color) > 0:
                color = np.array(color, dtype=np.uint8)
            args.append(color)
        if from_h is not None:
            args.extend([from_h, from_v, to_h, to_v])
        if pen_width is not None:
            args.append(pen_width)
        Screen('DrawLine', *args)
    
    def draw_dots(self, window_ptr, xy, size=None, color=None, center=None, dot_type=None, lenient=None):
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
        args = [window_ptr, xy]
        if size is not None:
            args.append(size)
        if color is not None:
            args.append(color)
        if center is not None:
            args.append(center)
        if dot_type is not None:
            args.append(dot_type)
        if lenient is not None:
            args.append(lenient)
            
        return Screen('DrawDots', *args)
    
    def draw_lines(self, window_ptr, xy, width=None, colors=None, center=None, smooth=None, lenient=None):
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
        args = [window_ptr, xy]
        if width is not None:
            args.append(width)
        if colors is not None:
            args.append(colors)
        if center is not None:
            args.append(center)
        if smooth is not None:
            args.append(smooth)
        if lenient is not None:
            args.append(lenient)
            
        return Screen('DrawLines', *args)
    
    # Text drawing - all take window_ptr as first argument like MATLAB
    def draw_text(self, window_ptr, text, x=None, y=None, color=None, background_color=None,
                 y_position_is_baseline=None, swap_text_direction=None):
        """Draw text to the window (like MATLAB Screen('DrawText', ...))
        
        Args:
            window_ptr: Window pointer to draw on
            text: Text string to draw
            x: X position
            y: Y position
            color: Text color
            background_color: Background color
            y_position_is_baseline: Y position is baseline
            swap_text_direction: Swap text direction
        
        Returns:
            Tuple of (newX, newY, textHeight)
        """
        args = [window_ptr, text]
        if x is not None:
            args.append(x)
        if y is not None:
            args.append(y)
        if color is not None:
            args.append(color)
        if background_color is not None:
            args.append(background_color)
        if y_position_is_baseline is not None:
            args.append(y_position_is_baseline)
        if swap_text_direction is not None:
            args.append(swap_text_direction)
            
        return Screen('DrawText', *args)
    
    def text_bounds(self, window_ptr, text, x=None, y=None, y_position_is_baseline=None, swap_text_direction=None):
        """Get text bounding rectangle (like MATLAB Screen('TextBounds', ...))"""
        args = [window_ptr, text]
        if x is not None:
            args.append(x)
        if y is not None:
            args.append(y)
        if y_position_is_baseline is not None:
            args.append(y_position_is_baseline)
        if swap_text_direction is not None:
            args.append(swap_text_direction)
            
        return Screen('TextBounds', *args)
    
    # Text formatting - all take window_ptr as first argument like MATLAB
    def text_size(self, window_ptr, size=None):
        """Get or set text size (like MATLAB Screen('TextSize', ...))"""
        args = [window_ptr]
        if size is not None:
            args.append(size)
        return Screen('TextSize', *args)
    
    def text_font(self, window_ptr, font_name_or_number=None, text_style=None):
        """Get or set text font (like MATLAB Screen('TextFont', ...))"""
        args = [window_ptr]
        if font_name_or_number is not None:
            args.append(font_name_or_number)
        if text_style is not None:
            args.append(text_style)
        return Screen('TextFont', *args)
    
    def text_color(self, window_ptr, color=None):
        """Get or set text color (like MATLAB Screen('TextColor', ...))"""
        args = [window_ptr]
        if color is not None:
            args.append(color)
        return Screen('TextColor', *args)
    
    def text_background_color(self, window_ptr, color=None):
        """Get or set text background color (like MATLAB Screen('TextBackgroundColor', ...))"""
        args = [window_ptr]
        if color is not None:
            args.append(color)
        return Screen('TextBackgroundColor', *args)
    
    # Image operations - all take window_ptr as first argument like MATLAB
    def get_image(self, window_ptr, rect=None, buffer_name=None, float_precision=0, num_channels=3):
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
        args = [window_ptr]
        if rect is not None:
            args.append(rect)
        if buffer_name is not None:
            args.append(buffer_name)
        if float_precision != 0:
            args.append(float_precision)
        if num_channels != 3:
            args.append(num_channels)
            
        return Screen('GetImage', *args)
    
    def put_image(self, window_ptr, image_array, rect=None):
        """Put image array into window (like MATLAB Screen('PutImage', ...))
        
        Args:
            window_ptr: Window pointer to write to
            image_array: Image data as numpy array
            rect: Destination rectangle
        """
        args = [window_ptr, image_array]
        if rect is not None:
            args.append(rect)
        Screen('PutImage', *args)
    
    # Window information functions
    def window_kind(self, window_ptr):
        """Get window kind (like MATLAB Screen(window_ptr, 'WindowKind'))"""
        return Screen(window_ptr, 'WindowKind')
    
    def is_offscreen(self, window_ptr):
        """Check if window is offscreen (like MATLAB Screen(window_ptr, 'IsOffscreen'))"""
        return Screen(window_ptr, 'IsOffscreen')
    
    def window_size(self, window_ptr, real_fb_size=0):
        """Get window size (like MATLAB Screen('WindowSize', ...))"""
        return Screen('WindowSize', window_ptr, real_fb_size)
    
    def pixel_size(self, window_ptr):
        """Get pixel size (like MATLAB Screen('PixelSize', ...))"""
        return Screen('PixelSize', window_ptr)
    
    def get_flip_interval(self, window_ptr, num_samples=None, std_dev=None, timeout=None):
        """Get monitor flip interval (like MATLAB Screen('GetFlipInterval', ...))"""
        args = [window_ptr]
        if num_samples is not None:
            args.append(num_samples)
        if std_dev is not None:
            args.append(std_dev)
        if timeout is not None:
            args.append(timeout)
        return Screen('GetFlipInterval', *args)
    
    # Gamma and color functions
    def read_normalized_gamma_table(self, window_ptr_or_screen_number, physical_display=None):
        """Read normalized gamma table (like MATLAB Screen('ReadNormalizedGammaTable', ...))"""
        args = [window_ptr_or_screen_number]
        if physical_display is not None:
            args.append(physical_display)
        return Screen('ReadNormalizedGammaTable', *args)
    
    def load_normalized_gamma_table(self, window_ptr_or_screen_number, table, 
                                   load_on_next_flip=None, physical_display=None, ignore_errors=None):
        """Load normalized gamma table (like MATLAB Screen('LoadNormalizedGammaTable', ...))"""
        args = [window_ptr_or_screen_number, table]
        if load_on_next_flip is not None:
            args.append(load_on_next_flip)
        if physical_display is not None:
            args.append(physical_display)
        if ignore_errors is not None:
            args.append(ignore_errors)
        return Screen('LoadNormalizedGammaTable', *args)
    
    # Other utility functions
    def rect(self, window_ptr_or_screen_number, real_fb_size=0):
        """Get rectangle (like MATLAB Screen('Rect', ...))"""
        return Screen('Rect', window_ptr_or_screen_number, real_fb_size)


# Convenience functions that don't require a PTBScreen instance
def get_screens():
    """Get list of available screens"""
    return Screen('Screens')

def get_version():
    """Get Screen module version"""
    return Screen('Version')
