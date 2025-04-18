"""
keyframes/matcher.py - Module for matching keyframes with timestamps in a video
"""

import cv2
import numpy as np
import os
import concurrent.futures
import traceback
import datetime
from tqdm import tqdm

class VideoKeyframeMatcher:
    def __init__(self, video_path, keyframes_folder):
        self.video_path = video_path
        self.keyframes_folder = keyframes_folder
        self.video_array = None
        self.fps = None

    def load_video_to_array(self):
        """Load the video into a 3D numpy array."""
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise Exception("Error opening video file")
            
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            frames = []
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            for _ in tqdm(range(total_frames), desc="Loading video frames"):
                ret, frame = cap.read()
                if not ret:
                    break
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frames.append(gray_frame)
            
            cap.release()
            self.video_array = np.stack(frames, axis=0)
            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Error loading video: {str(e)}")
            return False

    def find_matching_frame(self, keyframe_path):
        """Find the best matching frame for a given keyframe using cross-correlation."""
        try:
            keyframe = cv2.imread(keyframe_path, cv2.IMREAD_GRAYSCALE)
            if keyframe is None:
                raise Exception(f"Error loading keyframe: {keyframe_path}")

            # Calculate normalized cross-correlation and find the best match
            best_frame_index = -1
            max_corr = -np.inf
            
            for i, frame in enumerate(tqdm(self.video_array, desc=f"Matching {os.path.basename(keyframe_path)}", leave=False)):
                corr = np.corrcoef(frame.ravel(), keyframe.ravel())[0, 1]
                if corr > max_corr:
                    max_corr = corr
                    best_frame_index = i

            best_time = best_frame_index / self.fps
            return keyframe_path, best_time, max_corr
        except Exception as e:
            traceback.print_exc()
            print(f"Error matching frame: {str(e)}")
            return keyframe_path, -1, -1

    def process_keyframes(self):
        """Process keyframes in parallel and find the best matching time stamps."""
        try:
            keyframe_files = sorted([f for f in os.listdir(self.keyframes_folder) if not f.startswith(".") and f.endswith('.jpeg')])
            keyframe_paths = [os.path.join(self.keyframes_folder, kf) for kf in keyframe_files]

            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = list(executor.map(self.find_matching_frame, keyframe_paths))
                for result in futures:
                    results.append(result)

            # Sort results by time and print
            results.sort(key=lambda x: x[1])  # Sort by timestamp
            for path, time, correlation in results:
                if time >= 0:
                    print(f"{os.path.basename(path)} best matches with time {time:.2f} seconds (Correlation: {correlation:.4f})")
                else:
                    print(f"No match found for {os.path.basename(path)}")

            # Save results to CSV
            import csv
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_csv = os.path.join(os.path.dirname(self.keyframes_folder), f"keyframe_timestamps_{timestamp}.csv")
            
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Keyframe', 'Timestamp (seconds)', 'Correlation'])
                for path, time, correlation in results:
                    if time >= 0:
                        writer.writerow([os.path.basename(path), f"{time:.2f}", f"{correlation:.4f}"])
                    else:
                        writer.writerow([os.path.basename(path), "No match", "N/A"])
            
            print(f"Results saved to {output_csv}")
            return results
        except Exception as e:
            traceback.print_exc()
            print(f"Error processing keyframes: {str(e)}")
            return []