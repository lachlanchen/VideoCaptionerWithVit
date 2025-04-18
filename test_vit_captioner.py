#!/usr/bin/env python
# test_vit_captioner.py - Test script to check if vit-captioner package works with pork.mp4

import os
import argparse
import traceback
import datetime
import sys
from tqdm import tqdm

def test_command_line():
    """
    Test the vit-captioner package using command line
    """
    print("Testing vit-captioner using command line...")
    cmd = "vit-captioner caption-video -V data/pork.mp4 -N 5"
    
    print(f"Running command: {cmd}")
    result = os.system(cmd)
    
    if result == 0:
        print("Command line test PASSED!")
        return True
    else:
        print("Command line test FAILED!")
        return False

def test_python_api():
    """
    Test the vit-captioner package using Python API
    """
    try:
        print("\nTesting vit-captioner using Python API...")
        from vit_captioner.captioning.video import VideoToCaption
        
        video_path = "data/pork.mp4"
        print(f"Processing video: {video_path}")
        print(f"Number of frames to extract: 5")
        
        # Create timestamp for output directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"test_results_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the converter and process the video
        converter = VideoToCaption(video_path, num_frames=5)
        
        # Convert the video to captions
        success = converter.convert()
        
        if success:
            print("\nPython API test PASSED!")
            print(f"SRT file: {converter.output_srt}")
            print(f"JSON file: {converter.output_json}")
            print(f"Extracted frames: {converter.frames_dir}")
            
            # Copy the outputs to our test results directory for reference
            import shutil
            shutil.copy(converter.output_srt, output_dir)
            shutil.copy(converter.output_json, output_dir)
            print(f"\nResults copied to: {output_dir}")
            
            return True
        else:
            print("\nPython API test FAILED!")
            return False
        
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test the vit-captioner package")
    parser.add_argument("--cli-only", action="store_true", help="Only test the command line interface")
    parser.add_argument("--api-only", action="store_true", help="Only test the Python API")
    args = parser.parse_args()
    
    success = True
    
    if not args.api_only:
        cli_success = test_command_line()
        success = success and cli_success
    
    if not args.cli_only:
        api_success = test_python_api()
        success = success and api_success
    
    if success:
        print("\nAll tests PASSED!")
        return 0
    else:
        print("\nSome tests FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())