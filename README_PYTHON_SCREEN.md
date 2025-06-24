# Psychtoolbox-3 Python Screen Module - Installation Guide

## Installation

### 1. System Dependencies

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

### 2. Install package from GitHub Release

#### Build from source

```
gh repo clone gkane26/Psychtoolbox-3
cd Psychtoolbox-3
git checkout Psychtoolbox-3.0.19-pyscreen
pip install .
```

#### Install from wheel (on GitHub release)

Not yet implemented...


## Basic Usage Example

```python
from psychtoolbox.screen import PTBScreen
import psychtoolbox.Screen as Screen
from psychtoolbox import WaitSecs

# Create screen interface
screen = PTBScreen()

# Set a screen preference: skip sync tests
screen.preference('SkipSyncTests', 1)

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
WaitSecs(2.0)
screen.close(window)
screen.close_all()
```

## Available Modules

All major Psychtoolbox modules are included:

- ✅ **Screen**: Graphics and visual stimulus presentation
- ✅ **PsychPortAudio**: High-quality audio I/O
- ✅ **GetSecs**: High-precision timing
- ✅ **WaitSecs**: Precise delays
- ✅ **PsychHID**: Human interface device support
- ✅ **IOPort**: I/O port access
