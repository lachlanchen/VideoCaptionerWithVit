# ViT Captioner

[![PyPI version](https://badge.fury.io/py/vit-captioner.svg)](https://badge.fury.io/py/vit-captioner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for extracting keyframes from videos and generating captions using the ViT-GPT2 model.

## Features

- Extract keyframes from videos using Katna or uniform sampling
- Generate captions for images using the ViT-GPT2 model
- Match keyframes with timestamps in a video
- Convert videos to SRT subtitle files with captions
- Visualize keyframes and timeline data
- Performance optimized with smart resource management
- Thread-safe image processing and visualization

## Installation

```bash
pip install vit-captioner
```

## Command Line Usage

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
vit-captioner caption-video -V /path/to/video.mp4 -N 10 -v
```
The `-v` flag enables verbose output with progress bars.

### Find matching timestamps for keyframes:
```bash
vit-captioner find-timestamps -V /path/to/video.mp4 -K /path/to/keyframes_folder -v
```

## Python API Usage

```python
from vit_captioner.keyframes.extractor import KeyFrameExtractor
from vit_captioner.captioning.image import ImageCaptioner
from vit_captioner.captioning.video import VideoToCaption

# Extract keyframes
extractor = KeyFrameExtractor("/path/to/video.mp4")
extractor.extract_key_frames("/path/to/video.mp4", 10)

# Generate caption for an image
captioner = ImageCaptioner()
caption = captioner.predict_caption("/path/to/image.jpg")

# Convert video to captions
# Note: verbose flag enables progress bars
converter = VideoToCaption("/path/to/video.mp4", num_frames=10, verbose=True)
converter.convert()
```

## Performance Optimizations

- Smart resource management with proper cleanup
- Single model loading for multiple frames (improved memory usage)
- Thread-safe image processing with error fallbacks
- Progress bars for tracking long-running operations
- Limited number of concurrent workers to prevent memory issues

## Requirements

- Python 3.6+
- OpenCV
- PyTorch
- Transformers
- Katna
- Matplotlib
- tqdm

## Source Code

Source code is available on GitHub: [https://github.com/lachlanchen/VideoCaptionerWithVit](https://github.com/lachlanchen/VideoCaptionerWithVit)

## License

MIT