"""
keyframes/extractor.py - Module for extracting keyframes from videos
"""

from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os
import argparse
import datetime
import traceback

class KeyFrameExtractor:
    def __init__(self, video_path):
        # Determine the base directory and filename of the video
        base_dir = os.path.dirname(video_path)
        filename = os.path.splitext(os.path.basename(video_path))[0]
        # Path where the key frames will be saved with datetime suffix
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_folder = os.path.join(base_dir, f"{filename}_key_frame_output_{timestamp}")
        
        # Ensure the output directory exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def extract_key_frames(self, video_path, num_key_frames):
        """
        Extract key frames from a video file using Katna library.
        
        Args:
            video_path: Path to the video file
            num_key_frames: Number of key frames to extract
            
        Returns:
            output_folder: Path to the folder containing extracted keyframes
        """
        try:
            # Initialize video processing module
            video_processor = Video()
            # Initialize the disk writer to save key frames
            disk_writer = KeyFrameDiskWriter(location=self.output_folder)
            # Extract key frames
            video_processor.extract_video_keyframes(
                no_of_frames=num_key_frames,
                file_path=video_path,
                writer=disk_writer
            )
            print(f"Key frames extracted and saved in the folder: {self.output_folder}")
            return self.output_folder
        except Exception as e:
            traceback.print_exc()
            print(f"Error extracting key frames: {str(e)}")
            return None