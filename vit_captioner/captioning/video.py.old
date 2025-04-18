"""
captioning/video.py - Module for converting videos to captions and generating SRT files
"""

import cv2
import os
import json
import concurrent.futures
import traceback
import datetime
from tqdm import tqdm
from ..keyframes.extractor import KeyFrameExtractor
from .image import ImageCaptioner

class VideoToCaption:
    def __init__(self, video_path, num_frames=10):
        try:
            self.original_video_path = video_path
            self.video_path = self.normalize_video_path(video_path)
            
            self.num_frames = num_frames
            
            # Add timestamp to output directories and files
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.frames_dir = os.path.splitext(video_path)[0] + f"_captioning_frames_{timestamp}"
            self.output_srt = os.path.splitext(video_path)[0] + f"_caption_{timestamp}.srt"
            self.output_json = os.path.splitext(video_path)[0] + f"_caption_{timestamp}.json"
            
            os.makedirs(self.frames_dir, exist_ok=True)
            self.duration = None  # Initialize duration
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error initializing VideoToCaption: {str(e)}")

    def normalize_video_path(self, video_path):
        """
        Ensures the video path has a lowercase extension for consistent processing.
        If necessary, creates a symbolic link with the normalized extension.
        """
        try:
            dirname, filename = os.path.split(video_path)
            basename, ext = os.path.splitext(filename)
            normalized_ext = ext.lower()
            if ext == normalized_ext:
                return video_path  # No change needed

            normalized_filename = basename + normalized_ext
            normalized_path = os.path.join(dirname, normalized_filename)
            if not os.path.exists(normalized_path):
                os.symlink(video_path, normalized_path)
            return normalized_path
        except Exception as e:
            traceback.print_exc()
            print(f"Error normalizing video path: {str(e)}")
            return video_path  # Return original path on error

    def extract_frames_katna(self):
        """Extract keyframes using Katna library"""
        try:
            extractor = KeyFrameExtractor(self.video_path)
            output_folder = extractor.extract_key_frames(self.video_path, self.num_frames)
            if output_folder and os.path.exists(output_folder):
                frames = sorted([os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.jpeg')])
                return frames
            return []
        except Exception as e:
            traceback.print_exc()
            print(f"Error extracting frames with katna: {str(e)}")
            return []

    def extract_frames_uniform(self):
        """Extract frames uniformly across the video duration"""
        try:
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = total_frames / fps
            
            timestamps = [i * (self.duration / self.num_frames) for i in range(self.num_frames)]
            frames = []
            
            for i, timestamp in enumerate(tqdm(timestamps, desc="Extracting frames")):
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(fps * timestamp))
                ret, frame = cap.read()
                if ret:
                    frame_path = os.path.join(self.frames_dir, f"frame_{i:04d}.jpeg")
                    cv2.imwrite(frame_path, frame)
                    frames.append(frame_path)
            cap.release()
            return frames
        except Exception as e:
            traceback.print_exc()
            print(f"Error extracting frames uniformly: {str(e)}")
            return []

    def extract_frames(self):
        """Extract frames from video using Katna or uniform sampling"""
        try:
            # First try to extract frames using Katna
            frames = self.extract_frames_katna()
            if not frames:
                print("No frames extracted by Katna, falling back to uniform extraction.")
                frames = self.extract_frames_uniform()
                
            # Calculate timestamps assuming they are evenly distributed
            if self.duration is None:
                cap = cv2.VideoCapture(self.video_path)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                self.duration = total_frames / fps
                cap.release()
                
            interval = self.duration / len(frames)
            return [(frame, i * interval, (i + 1) * interval) for i, frame in enumerate(frames)]
        except Exception as e:
            traceback.print_exc()
            print(f"Error extracting frames: {str(e)}")
            return []

    def caption_frame(self, frame_data):
        """Generate caption for a single frame"""
        try:
            frame_path, _, _ = frame_data
            captioner = ImageCaptioner()
            caption = captioner.predict_caption(frame_path)
            del captioner  # Ensure the instance is deleted after use
            return caption
        except Exception as e:
            traceback.print_exc()
            print(f"Error captioning frame: {str(e)}")
            return "Error generating caption"

    def convert(self):
        """Convert video to captions and generate SRT file"""
        try:
            frames = self.extract_frames()
            if not frames:
                print("No frames extracted. Aborting conversion.")
                return False
                
            srt_entries = []
            
            print("Generating captions for extracted frames...")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.caption_frame, frame): frame for frame in frames}
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(frames), desc="Captioning frames"):
                    frame_path, start_time, end_time = futures[future]
                    caption = future.result()
                    srt_entries.append({
                        'index': frames.index((frame_path, start_time, end_time)) + 1,
                        'start': self.format_time(start_time),
                        'end': self.format_time(end_time),
                        'text': caption
                    })

            srt_entries.sort(key=lambda x: x['index'])
            self.save_srt_file(srt_entries)
            self.save_json_file(srt_entries)
            
            print(f"Conversion complete. SRT file saved to {self.output_srt}")
            print(f"JSON file saved to {self.output_json}")
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Error converting video to captions: {str(e)}")
            return False

    def format_time(self, seconds):
        """Format time in SRT format: HH:MM:SS,mmm"""
        try:
            h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), seconds % 60
            ms = int((s - int(s)) * 1000)
            return f"{h:02}:{m:02}:{int(s):02},{ms:03}"
        except Exception as e:
            traceback.print_exc()
            print(f"Error formatting time: {str(e)}")
            return "00:00:00,000"

    def save_srt_file(self, srt_entries):
        """Save captions in SRT subtitle format"""
        try:
            with open(self.output_srt, 'w') as file:
                for entry in srt_entries:
                    file.write(f"{entry['index']}\n")
                    file.write(f"{entry['start']} --> {entry['end']}\n")
                    file.write(f"{entry['text']}\n\n")
        except Exception as e:
            traceback.print_exc()
            print(f"Error saving SRT file: {str(e)}")

    def save_json_file(self, srt_entries):
        """Save captions in JSON format"""
        try:
            with open(self.output_json, 'w') as file:
                json.dump([{"start": e['start'], "end": e['end'], "text": e['text']} for e in srt_entries], file, indent=4)
        except Exception as e:
            traceback.print_exc()
            print(f"Error saving JSON file: {str(e)}")