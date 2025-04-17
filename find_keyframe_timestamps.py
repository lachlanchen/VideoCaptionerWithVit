import cv2
import numpy as np
import os
import concurrent.futures

class VideoKeyframeMatcher:
    def __init__(self, video_path, keyframes_folder):
        self.video_path = video_path
        self.keyframes_folder = keyframes_folder
        self.video_array = None
        self.fps = None

    def load_video_to_array(self):
        """Load the video into a 3D numpy array."""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file")
        
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray_frame)
        
        cap.release()
        self.video_array = np.stack(frames, axis=0)

    def find_matching_frame(self, keyframe_path):
        """Find the best matching frame for a given keyframe using cross-correlation."""
        keyframe = cv2.imread(keyframe_path, cv2.IMREAD_GRAYSCALE)
        if keyframe is None:
            raise Exception("Error loading keyframe")

        # Calculate normalized cross-correlation and find the best match
        best_frame_index = -1
        max_corr = -np.inf
        for i, frame in enumerate(self.video_array):
            corr = np.corrcoef(frame.ravel(), keyframe.ravel())[0, 1]
            if corr > max_corr:
                max_corr = corr
                best_frame_index = i

        best_time = best_frame_index / self.fps
        return keyframe_path, best_time, max_corr

    def process_keyframes(self):
        """Process keyframes in parallel and find the best matching time stamps."""
        keyframe_files = sorted([f for f in os.listdir(self.keyframes_folder) if not f.startswith(".") and f.endswith('.jpeg')])
        keyframe_paths = [os.path.join(self.keyframes_folder, kf) for kf in keyframe_files]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.find_matching_frame, keyframe_paths))

        # Sort results by time and print
        results.sort(key=lambda x: x[1])  # Sort by timestamp
        for path, time, correlation in results:
            print(f"{os.path.basename(path)} best matches with time {time:.2f} seconds (Correlation: {correlation:.4f})")

        return results

if __name__ == "__main__":
    base_dir = os.path.expanduser("~/Projects/vit-gpt2-image-captioning")
    video_name = "IMG_9421_2024_04_23_07_52_02_COMPLETED.mov"
    video_path = os.path.join(base_dir, video_name)
    keyframes_folder = os.path.join(base_dir, os.path.splitext(video_name)[0] + "_key_frame_output")

    matcher = VideoKeyframeMatcher(video_path, keyframes_folder)
    matcher.load_video_to_array()
    matcher.process_keyframes()

