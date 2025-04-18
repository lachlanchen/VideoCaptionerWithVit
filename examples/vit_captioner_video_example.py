#!/usr/bin/env python
# examples/vit_captioner_video_example.py - Example script showing usage similar to original vit_captioner_video.py

import argparse
import os
import traceback
from tqdm import tqdm
from vit_captioner.captioning.video import VideoToCaption

def main():
    """
    Example script demonstrating how to use the VideoToCaption class
    to generate captions for video frames. This mimics the original
    functionality of vit_captioner_video.py.
    """
    parser = argparse.ArgumentParser(description="Convert video to captions using ViT model")
    parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file")
    parser.add_argument("-N", "--num_frames", type=int, default=10, help="Number of frames to caption")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output")
    args = parser.parse_args()

    try:
        print(f"Processing video: {args.video_path}")
        print(f"Number of frames to extract: {args.num_frames}")
        
        # Create the converter and process the video
        converter = VideoToCaption(args.video_path, num_frames=args.num_frames)
        
        # Convert the video to captions
        success = converter.convert()
        
        if success:
            print("\nConversion completed successfully!")
            print(f"SRT file: {converter.output_srt}")
            print(f"JSON file: {converter.output_json}")
            print(f"Extracted frames: {converter.frames_dir}")
        else:
            print("\nConversion failed. Check the error messages above.")
        
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())