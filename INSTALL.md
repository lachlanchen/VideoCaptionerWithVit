# Installation and Usage Guide

## Installation Steps

### Option 1: Install from local source

1. Clone or download the repository
```bash
git clone https://github.com/your-username/vit-captioner.git
cd vit-captioner
```

2. Install the package in development mode
```bash
pip install -e .
```

### Option 2: Create and install a pip package

1. Build the package
```bash
python setup.py sdist bdist_wheel
```

2. Install the package
```bash
pip install dist/vit_captioner-0.1.*.tar.gz
```

## Quick Start Guide

### Extract keyframes from a video:
```bash
vit-captioner extract -V /path/to/video.mp4 -N 10 -v
```

### Generate caption for an image:
```bash
vit-captioner caption-image -I /path/to/image.jpg
```

### Convert video to captions:
```bash
vit-captioner caption-video -V /path/to/video.mp4 -N 10
```

### Find matching timestamps for keyframes:
```bash
vit-captioner find-timestamps -V /path/to/video.mp4 -K /path/to/keyframes_folder -v
```

## Advanced Usage

### Python API Examples

#### Extract keyframes:
```python
from vit_captioner.keyframes.extractor import KeyFrameExtractor

# Create extractor and extract keyframes
extractor = KeyFrameExtractor("/path/to/video.mp4")
output_folder = extractor.extract_key_frames("/path/to/video.mp4", num_key_frames=10)

# Visualize the extracted keyframes
from vit_captioner.utils.visualization import visualize_keyframes
visualize_keyframes(output_folder)
```

#### Generate caption for an image:
```python
from vit_captioner.captioning.image import ImageCaptioner

# Create captioner and generate caption
captioner = ImageCaptioner()
caption = captioner.predict_caption("/path/to/image.jpg", save_image=True)
print(f"Caption: {caption}")
```

#### Convert video to captions:
```python
from vit_captioner.captioning.video import VideoToCaption

# Create converter and generate captions
converter = VideoToCaption("/path/to/video.mp4", num_frames=10)
converter.convert()
```

#### Find matching timestamps for keyframes:
```python
from vit_captioner.keyframes.matcher import VideoKeyframeMatcher
import cv2

# Create matcher and find timestamps
matcher = VideoKeyframeMatcher("/path/to/video.mp4", "/path/to/keyframes_folder")
matcher.load_video_to_array()
results = matcher.process_keyframes()

# Visualize the timestamps on a timeline
from vit_captioner.utils.visualization import visualize_timeline

# Get video duration
cap = cv2.VideoCapture("/path/to/video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps
cap.release()

# Extract timestamps and captions
timestamps = [t for _, t, _ in results if t >= 0]
captions = [os.path.basename(p) for p, t, _ in results if t >= 0]

# Visualize timeline
visualize_timeline(timestamps, captions, duration)
```

## Package Structure

```
vit-captioner/
├── README.md
├── LICENSE
├── setup.py
├── MANIFEST.in
├── vit_captioner/
│   ├── __init__.py
│   ├── cli.py
│   ├── keyframes/
│   │   ├── __init__.py
│   │   ├── extractor.py 
│   │   └── matcher.py
│   ├── captioning/
│   │   ├── __init__.py
│   │   ├── image.py
│   │   └── video.py
│   └── utils/
│       ├── __init__.py
│       └── visualization.py
```

## Dependencies

- Python 3.6+
- OpenCV
- PyTorch
- Transformers
- Katna (for keyframe extraction)
- Matplotlib
- tqdm (for progress bars)
- Pillow (PIL)
- NumPy