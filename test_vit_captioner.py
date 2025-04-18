#!/usr/bin/env python
# test_vit_captioner_enhanced.py - Enhanced test script for vit-captioner with performance metrics

import os
import argparse
import traceback
import datetime
import time
import shutil
import warnings
from tqdm import tqdm

# Filter out transformer warnings
warnings.filterwarnings("ignore", message="Some weights of the model checkpoint.*")

def test_command_line(video_path="data/pork.mp4", num_frames=5, verbose=True):
    """
    Test the vit-captioner package using command line
    
    Args:
        video_path: Path to the test video
        num_frames: Number of frames to extract
        verbose: Whether to show verbose output
    
    Returns:
        success: Boolean indicating success, processing time, output paths
    """
    print("Testing vit-captioner using command line...")
    
    verbose_flag = "-v" if verbose else ""
    cmd = f"vit-captioner caption-video -V {video_path} -N {num_frames} {verbose_flag}"
    
    print(f"Running command: {cmd}")
    start_time = time.time()
    result = os.system(cmd)
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    # Find the output files based on timestamp pattern
    base_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Look for output files with timestamp in their names
    srt_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) 
                if f.startswith(f"{base_name}_caption_") and f.endswith(".srt")]
    json_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) 
                 if f.startswith(f"{base_name}_caption_") and f.endswith(".json")]
    frame_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) 
                 if os.path.isdir(os.path.join(base_dir, d)) and 
                 d.startswith(f"{base_name}_key_frame_output_")]
    
    # Sort by creation time to get the latest files
    srt_file = sorted(srt_files, key=os.path.getctime)[-1] if srt_files else None
    json_file = sorted(json_files, key=os.path.getctime)[-1] if json_files else None
    frame_dir = sorted(frame_dirs, key=os.path.getctime)[-1] if frame_dirs else None
    
    outputs = {
        "srt_file": srt_file,
        "json_file": json_file,
        "frame_dir": frame_dir
    }
    
    if result == 0:
        print(f"Command line test PASSED! Processing time: {processing_time:.2f} seconds")
        for key, value in outputs.items():
            if value:
                print(f"  {key}: {value}")
        return True, processing_time, outputs
    else:
        print(f"Command line test FAILED! Processing time: {processing_time:.2f} seconds")
        return False, processing_time, outputs

def test_python_api(video_path="data/pork.mp4", num_frames=5, verbose=True):
    """
    Test the vit-captioner package using Python API
    
    Args:
        video_path: Path to the test video
        num_frames: Number of frames to extract
        verbose: Whether to show verbose output
        
    Returns:
        success: Boolean indicating success, processing time, output paths
    """
    try:
        print("\nTesting vit-captioner using Python API...")
        
        # Import the module
        from vit_captioner.captioning.video import VideoToCaption
        
        print(f"Processing video: {video_path}")
        print(f"Number of frames to extract: {num_frames}")
        
        # Create timestamp for output directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"test_results_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the converter and process the video
        start_time = time.time()
        converter = VideoToCaption(video_path, num_frames=num_frames, verbose=verbose)
        
        # Convert the video to captions
        success = converter.convert()
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        outputs = {
            "srt_file": converter.output_srt,
            "json_file": converter.output_json,
            "frame_dir": os.path.dirname(converter.extract_frames_katna()[0]) if converter.extract_frames_katna() else converter.frames_dir
        }
        
        if success:
            print(f"\nPython API test PASSED! Processing time: {processing_time:.2f} seconds")
            for key, value in outputs.items():
                print(f"  {key}: {value}")
            
            # Copy the outputs to our test results directory for reference
            for key, path in outputs.items():
                if path and os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.copytree(path, os.path.join(output_dir, os.path.basename(path)), 
                                       dirs_exist_ok=True)
                    else:
                        shutil.copy(path, output_dir)
            
            print(f"\nResults copied to: {output_dir}")
            return True, processing_time, outputs
        else:
            print(f"\nPython API test FAILED! Processing time: {processing_time:.2f} seconds")
            return False, processing_time, outputs
        
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {str(e)}")
        return False, 0, {}

def check_captions_quality(json_file):
    """
    Check the quality of generated captions
    
    Args:
        json_file: Path to the JSON file with captions
        
    Returns:
        metrics: Dictionary with caption quality metrics
    """
    try:
        import json
        
        with open(json_file, 'r') as f:
            captions = json.load(f)
        
        # Basic quality metrics
        caption_lengths = [len(cap['text'].split()) for cap in captions]
        avg_length = sum(caption_lengths) / len(caption_lengths) if caption_lengths else 0
        min_length = min(caption_lengths) if caption_lengths else 0
        max_length = max(caption_lengths) if caption_lengths else 0
        
        # Count captions with common features
        has_person = sum(1 for cap in captions if any(word in cap['text'].lower() 
                                                     for word in ['person', 'man', 'woman', 'people', 'child', 'boy', 'girl']))
        has_object = sum(1 for cap in captions if any(word in cap['text'].lower() 
                                                     for word in ['table', 'chair', 'car', 'dog', 'cat', 'food']))
        
        metrics = {
            "total_captions": len(captions),
            "avg_words_per_caption": avg_length,
            "min_words": min_length,
            "max_words": max_length,
            "captions_with_people": has_person,
            "captions_with_objects": has_object
        }
        
        print("\nCaption Quality Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
            
        return metrics
        
    except Exception as e:
        print(f"Error checking captions quality: {str(e)}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Enhanced test for the vit-captioner package")
    parser.add_argument("-V", "--video", type=str, default="data/pork.mp4", 
                       help="Path to test video (default: data/pork.mp4)")
    parser.add_argument("-N", "--num-frames", type=int, default=5, 
                       help="Number of frames to extract (default: 5)")
    parser.add_argument("--cli-only", action="store_true", help="Only test the command line interface")
    parser.add_argument("--api-only", action="store_true", help="Only test the Python API")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output")
    args = parser.parse_args()
    
    results = {}
    success = True
    
    if not args.api_only:
        cli_success, cli_time, cli_outputs = test_command_line(
            video_path=args.video, 
            num_frames=args.num_frames,
            verbose=args.verbose
        )
        results["cli"] = {
            "success": cli_success,
            "time": cli_time,
            "outputs": cli_outputs
        }
        success = success and cli_success
        
        # Check caption quality if test was successful
        if cli_success and cli_outputs.get("json_file"):
            results["cli"]["quality"] = check_captions_quality(cli_outputs["json_file"])
    
    if not args.cli_only:
        api_success, api_time, api_outputs = test_python_api(
            video_path=args.video, 
            num_frames=args.num_frames,
            verbose=args.verbose
        )
        results["api"] = {
            "success": api_success,
            "time": api_time,
            "outputs": api_outputs
        }
        success = success and api_success
        
        # Check caption quality if test was successful
        if api_success and api_outputs.get("json_file"):
            results["api"]["quality"] = check_captions_quality(api_outputs["json_file"])
    
    print("\n===== TEST SUMMARY =====")
    if "cli" in results:
        print(f"CLI Test: {'PASSED' if results['cli']['success'] else 'FAILED'}")
        print(f"  Processing time: {results['cli']['time']:.2f} seconds")
    
    if "api" in results:
        print(f"API Test: {'PASSED' if results['api']['success'] else 'FAILED'}")
        print(f"  Processing time: {results['api']['time']:.2f} seconds")
    
    if "cli" in results and "api" in results:
        time_diff = abs(results['cli']['time'] - results['api']['time'])
        faster = "CLI" if results['cli']['time'] < results['api']['time'] else "API"
        print(f"Performance difference: {time_diff:.2f} seconds ({faster} was faster)")
    
    if success:
        print("\nAll tests PASSED!")
        return 0
    else:
        print("\nSome tests FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())