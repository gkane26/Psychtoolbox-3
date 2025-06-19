# Psychtoolbox-3 Python Screen Module - Installation Guide

## Quick Installation

### 1. Install System Dependencies

First, install the required system libraries:

```bash
# Graphics and X11 libraries (required for Screen module)
sudo apt install libx11-6 libgl1-mesa-glx libglu1-mesa-dev libxext-dev \
                 libx11-xcb-dev libxcb-dri3-dev libxcb-present-dev \
                 libxcb-sync-dev libxcomposite-dev libxfixes-dev \
                 libxrandr-dev libxxf86vm-dev libpciaccess-dev libxi-dev

# Audio libraries (required for PsychPortAudio module)
sudo apt install portaudio19-dev libasound2-dev

# USB libraries (required for PsychHID module)
sudo apt install libusb-1.0-0-dev
```

### 2. Install from GitHub Release

Install directly from the GitHub release:

```bash
# Install the cross-version compatible wheel (Python 3.7+)
pip install https://github.com/your-username/psychtoolbox-screen-py/releases/download/v3.0.19.16/psychtoolbox-3.0.19.16-cp37-abi3-linux_x86_64.whl

# Or install the Python 3.11 specific wheel
pip install https://github.com/your-username/psychtoolbox-screen-py/releases/download/v3.0.19.16/psychtoolbox-3.0.19.16-cp311-cp311-linux_x86_64.whl
```

### 3. Quick Test

Test that everything works:

```python
import psychtoolbox.Screen as Screen
from psychtoolbox.screen import PTBScreen

# Skip sync tests for development (optional)
Screen('Preference', 'SkipSyncTests', 1)

# Create screen interface
screen = PTBScreen()

# Get available screens
screens = screen.screens()
print(f"Available screens: {screens}")

# Test version
version = screen.get_version()
print(f"Screen version: {version['version']}")

print("✓ Installation successful!")
```

## Basic Usage Example

```python
from psychtoolbox.screen import PTBScreen
import psychtoolbox.Screen as Screen
import time

# Skip sync tests for development
Screen('Preference', 'SkipSyncTests', 1)

# Create screen interface
screen = PTBScreen()

# Open a window
window, rect = screen.open_window(
    screen_number=0, 
    color=[128, 128, 128],  # Gray background
    rect=[0, 0, 800, 600]   # Window size
)

# Draw some shapes
screen.fill_rect(window, color=[255, 0, 0], rect=[100, 100, 200, 200])  # Red rectangle
screen.fill_oval(window, color=[0, 255, 0], rect=[300, 100, 400, 200])  # Green oval

# Present the stimulus
screen.flip(window)

# Wait and clean up
time.sleep(2.0)
screen.close(window)
```

## Available Modules

All major Psychtoolbox modules are included:

- ✅ **Screen**: Graphics and visual stimulus presentation
- ✅ **PsychPortAudio**: High-quality audio I/O
- ✅ **GetSecs**: High-precision timing
- ✅ **WaitSecs**: Precise delays
- ✅ **PsychHID**: Human interface device support
- ✅ **IOPort**: I/O port access

## Troubleshooting

**Data type errors**: Colors and rectangles should be passed as lists:
```python
# Correct
screen.fill_rect(window, color=[255, 0, 0], rect=[100, 100, 200, 200])

# Avoid numpy arrays for colors/rects - the wrapper handles conversion automatically
```

**X11/Display issues**: Set the display environment:
```bash
export DISPLAY=:0
```

**Sync test failures**: For development, skip sync tests:
```python
Screen('Preference', 'SkipSyncTests', 1)
```

---

For complete build instructions and advanced usage, see [`README_PYTHON_SCREEN.md`](README_PYTHON_SCREEN.md).
