from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os
import argparse

class KeyFrameExtractor:
    def __init__(self, video_path):
        # Determine the base directory and filename of the video
        base_dir = os.path.dirname(video_path)
        filename = os.path.splitext(os.path.basename(video_path))[0]
        # Path where the key frames will be saved
        self.output_folder = os.path.join(base_dir, f"{filename}_key_frame_output")
        
        # Ensure the output directory exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def extract_key_frames(self, video_path, num_key_frames):
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

def main():
    parser = argparse.ArgumentParser(description="Extract key frames from video.")
    parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file.")
    parser.add_argument("-N", "--num_key_frames", type=int, default=7, help="Number of key frames to extract.")
    
    args = parser.parse_args()

    extractor = KeyFrameExtractor(args.video_path)
    extractor.extract_key_frames(args.video_path, args.num_key_frames)

if __name__ == "__main__":
    main()
