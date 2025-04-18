import cv2
import os
import argparse
import json
import concurrent.futures
from vit_captioner import ImageCaptioner  # Make sure this import matches your setup
from keyframes_extractor import KeyFrameExtractor  # Adjust import as necessary
from tqdm import tqdm

class VideoToCaption:
    def __init__(self, video_path, num_frames=10):
        # self.video_path = video_path
        self.original_video_path = video_path
        self.video_path = self.normalize_video_path(video_path)
        
        self.num_frames = num_frames
        self.frames_dir = os.path.splitext(video_path)[0] + "_captioning_frames"
        self.output_srt = os.path.splitext(video_path)[0] + "_caption.srt"
        self.output_json = os.path.splitext(video_path)[0] + "_caption.json"
        os.makedirs(self.frames_dir, exist_ok=True)
        self.duration = None  # Initialize duration


    def normalize_video_path(self, video_path):
        """
        Ensures the video path has a lowercase extension for consistent processing.
        If necessary, creates a symbolic link with the normalized extension.
        """
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

    def extract_frames_katna(self):
        try:
            extractor = KeyFrameExtractor(self.video_path)
            extractor.extract_key_frames(self.video_path, self.num_frames)
            frames = sorted([os.path.join(extractor.output_folder, f) for f in os.listdir(extractor.output_folder) if f.endswith('.jpeg')])
            return frames
        except Exception as e:
            print("Error extracting frames with katna: ", str(e))
            return []

    def extract_frames_uniform(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        self.duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        timestamps = [i * (self.duration / self.num_frames) for i in range(self.num_frames)]
        frames = []
        for i, timestamp in tqdm(enumerate(timestamps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(fps * timestamp))
            ret, frame = cap.read()
            if ret:
                frame_path = os.path.join(self.frames_dir, f"frame_{i:04d}.jpeg")
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
        cap.release()
        return frames

    def extract_frames(self):
        # First try to extract frames using Katna
        frames = self.extract_frames_katna()
        if not frames:
            print("No frames extracted by Katna, falling back to uniform extraction.")
            frames = self.extract_frames_uniform()
        # Calculate timestamps assuming they are evenly distributed
        if self.duration is None:
            cap = cv2.VideoCapture(self.video_path)
            self.duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
            cap.release()
        interval = self.duration / len(frames)
        return [(frame, i * interval, (i + 0.5) * interval) for i, frame in enumerate(frames)]

    def caption_frame(self, frame_data):
        frame_path, _, _ = frame_data
        captioner = ImageCaptioner()
        caption = captioner.predict_caption(frame_path)
        del captioner  # Ensure the instance is deleted after use
        return caption

    def convert(self):
        frames = self.extract_frames()
        srt_entries = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.caption_frame, frame): frame for frame in frames}
            for future in tqdm(concurrent.futures.as_completed(futures)):
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

    def format_time(self, seconds):
        h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), seconds % 60
        ms = int((s - int(s)) * 1000)
        return f"{h:02}:{m:02}:{int(s):02},{ms:03}"

    def save_srt_file(self, srt_entries):
        with open(self.output_srt, 'w') as file:
            for entry in srt_entries:
                file.write(f"{entry['index']}\n")
                file.write(f"{entry['start']} --> {entry['end']}\n")
                file.write(f"{entry['text']}\n\n")

    def save_json_file(self, srt_entries):
        with open(self.output_json, 'w') as file:
            json.dump([{"start": e['start'], "end": e['end'], "text": e['text']} for e in srt_entries], file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert video to captions using ViT model")
    parser.add_argument("-V", "--video_path", type=str, required=True, help="Path to the video file")
    parser.add_argument("-N", "--num_frames", type=int, default=10, help="Number of frames to caption")
    args = parser.parse_args()

    converter = VideoToCaption(args.video_path, num_frames=args.num_frames)
    converter.convert()
