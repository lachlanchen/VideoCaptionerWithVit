# ViT Captioner Examples

This directory contains example scripts that demonstrate how to use the ViT Captioner package.

## Video Captioning Example

The `vit_captioner_video_example.py` script shows how to use the package to:
- Extract frames from a video
- Generate captions for those frames
- Create SRT and JSON subtitle files

### Usage

```bash
python vit_captioner_video_example.py -V /path/to/video.mp4 -N 10 -v
```

### Arguments

- `-V, --video_path`: Path to the video file (required)
- `-N, --num_frames`: Number of frames to extract and caption (default: 10)
- `-v, --verbose`: Show more detailed output

### Example Output

```
Processing video: path/to/video.mp4
Number of frames to extract: 10
Extracting frames: 100%|██████████| 10/10 [00:01<00:00,  8.75it/s]
Generating captions for extracted frames...
Captioning frames: 100%|██████████| 10/10 [00:05<00:00,  1.90it/s]

Conversion completed successfully!
SRT file: path/to/video_caption_20250418_123045.srt
JSON file: path/to/video_caption_20250418_123045.json
Extracted frames: path/to/video_captioning_frames_20250418_123045
```