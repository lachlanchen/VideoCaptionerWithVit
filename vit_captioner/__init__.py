"""
ViT Captioner - A toolkit for video/image captioning using ViT-GPT2
"""
from importlib import import_module

from .version import VERSION
__version__ = VERSION  # Import version from version.py

__all__ = [
    'KeyFrameExtractor',
    'VideoKeyframeMatcher',
    'ImageCaptioner',
    'VideoToCaption',
    'visualize_keyframes',
    'visualize_timeline'
]

_LAZY_IMPORTS = {
    "KeyFrameExtractor": ".keyframes",
    "VideoKeyframeMatcher": ".keyframes",
    "ImageCaptioner": ".captioning",
    "VideoToCaption": ".captioning",
    "visualize_keyframes": ".utils",
    "visualize_timeline": ".utils",
}


def __getattr__(name):
    module_name = _LAZY_IMPORTS.get(name)
    if not module_name:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_name, __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value
