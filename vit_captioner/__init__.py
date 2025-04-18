"""
ViT Captioner - A toolkit for video/image captioning using ViT-GPT2
"""
from .version import VERSION
__version__ = VERSION  # Import version from version.py


# __version__ = "0.1.2"

from .keyframes import KeyFrameExtractor, VideoKeyframeMatcher
from .captioning import ImageCaptioner, VideoToCaption
from .utils import visualize_keyframes, visualize_timeline

__all__ = [
    'KeyFrameExtractor',
    'VideoKeyframeMatcher',
    'ImageCaptioner',
    'VideoToCaption',
    'visualize_keyframes',
    'visualize_timeline'
]