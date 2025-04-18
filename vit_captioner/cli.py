"""
cli.py - Command-line interface for the ViT Captioner package
"""

import argparse
import os
import sys
import traceback
import cv2
from .keyframes.extractor import KeyFrameExtractor
from .keyframes.matcher import VideoKeyframeMatcher
from .captioning.image import ImageCaptioner
from .captioning.video import VideoToCaption
from .utils.visualization import visualize_keyframes, visualize_timeline

def extract_keyframes(args):
    """Extract keyframes from a video"""
    try:
        extractor = KeyFrameExtractor(args.video_path)
        output_folder = extractor.extract_key_frames(args.video_path, args.num_key_frames)
        
        if output_folder and os.path.exists(output_folder) and args.visualize:
            visualize_keyframes(output_folder)
            
        return output_folder
    except Exception as e:
        traceback.print_exc()
        print(f"Error extracting keyframes: {str(e)}")
        sys.exit(1)

def caption_image(args):
    """Generate caption for an image"""
    try:
        captioner = ImageCaptioner()
        caption = captioner.predict_caption(args.image_path, save_image=True)
        print(f"Caption: {caption}")
    except Exception as e:
        traceback.print_exc()
        print(f"Error captioning image: {str(e)}")
        sys.exit(1)

def caption_video(args):
    """Convert video to captions and generate SRT file"""
    try:
        converter = VideoToCaption(args.video_path, num_frames=args.num_frames)
        converter.convert()
    except Exception as e:
        traceback.print_exc()
        print(f"Error captioning video: {str(e)}")
        sys.exit(1)

def find_timestamps(args):
    """Find matching timestamps for keyframes"""
    try:
        matcher = VideoKeyframeMatcher(args.video_path, args.keyframes_folder)
        if matcher.load_video_to_array():
            results = matcher.process_keyframes()
            
            if results and args.visualize:
                # Extract video duration
                cap = cv2.VideoCapture(args.video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = total_frames / fps
                cap.release()
                
                # Extract timestamps and captions (using filenames as captions for now)
                timestamps = [t for _, t, _ in results if t >= 0]
                captions = [os.path.basename(p) for p, t, _ in results if t >= 0]
                
                visualize_timeline(timestamps, captions, duration)
    except Exception as e:
        traceback.print_exc()
        print(f"Error finding timestamps: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the CLI"""
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="ViT-Captioner: Video and Image Captioning Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Parser for the extract command
    extract_parser = subparsers.add_parser("extract", help="Extract keyframes from a video")
    extract_parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file")
    extract_parser.add_argument("-N", "--num_key_frames", type=int, default=7, help="Number of key frames to extract")
    extract_parser.add_argument("-v", "--visualize", action="store_true", help="Visualize the extracted keyframes")
    
    # Parser for the caption-image command
    caption_image_parser = subparsers.add_parser("caption-image", help="Generate caption for an image")
    caption_image_parser.add_argument("-I", "--image_path", type=str, required=True, help="Path to the image file")
    
    # Parser for the caption-video command
    caption_video_parser = subparsers.add_parser("caption-video", help="Convert video to captions")
    caption_video_parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file")
    caption_video_parser.add_argument("-N", "--num_frames", type=int, default=10, help="Number of frames to caption")
    
    # Parser for the find-timestamps command
    find_timestamps_parser = subparsers.add_parser("find-timestamps", help="Find matching timestamps for keyframes")
    find_timestamps_parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file")
    find_timestamps_parser.add_argument("-K", "--keyframes_folder", type=str, required=True, help="Path to the keyframes folder")
    find_timestamps_parser.add_argument("-v", "--visualize", action="store_true", help="Visualize the timestamps on a timeline")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "extract":
        extract_keyframes(args)
    elif args.command == "caption-image":
        caption_image(args)
    elif args.command == "caption-video":
        caption_video(args)
    elif args.command == "find-timestamps":
        find_timestamps(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()