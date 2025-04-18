"""
utils/visualization.py - Module for visualization utilities
"""

import matplotlib.pyplot as plt
import os
import traceback
import datetime
import json
import numpy as np

def visualize_keyframes(keyframes_folder, captions=None, save_path=None):
    """
    Visualize keyframes in a grid layout.
    
    Args:
        keyframes_folder: Path to the folder containing keyframes
        captions: Optional dictionary mapping frame paths to captions
        save_path: Optional path to save the visualization
        
    Returns:
        Path to the saved visualization
    """
    try:
        import cv2
        from matplotlib.gridspec import GridSpec
        
        # List all keyframes in the folder
        keyframe_files = sorted([f for f in os.listdir(keyframes_folder) if f.endswith('.jpeg')])
        
        if not keyframe_files:
            print("No keyframes found in the folder.")
            return None
            
        # Calculate grid dimensions
        n = len(keyframe_files)
        cols = min(5, n)  # Maximum 5 columns
        rows = (n + cols - 1) // cols
        
        # Create figure
        plt.figure(figsize=(15, 3 * rows))
        gs = GridSpec(rows, cols, figure=plt.gcf())
        
        # Add each keyframe to the grid
        for i, keyframe_file in enumerate(keyframe_files):
            img = cv2.imread(os.path.join(keyframes_folder, keyframe_file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            ax = plt.subplot(gs[i // cols, i % cols])
            ax.imshow(img)
            
            # Add caption if available
            if captions and os.path.join(keyframes_folder, keyframe_file) in captions:
                ax.set_title(captions[os.path.join(keyframes_folder, keyframe_file)], fontsize=10)
            else:
                ax.set_title(keyframe_file, fontsize=10)
                
            ax.axis('off')
            
        plt.tight_layout()
        
        # Save the visualization
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if not save_path:
            save_path = os.path.join(keyframes_folder, f"keyframes_visualization_{timestamp}.png")
            
        plt.savefig(save_path, bbox_inches='tight')
        
        # Save data alongside figure
        if captions:
            data_path = os.path.splitext(save_path)[0] + '_data.json'
            with open(data_path, 'w') as f:
                json.dump(captions, f, indent=4)
            print(f"Visualization data saved to {data_path}")
                
        print(f"Visualization saved to {save_path}")
        return save_path
    except Exception as e:
        traceback.print_exc()
        print(f"Error visualizing keyframes: {str(e)}")
        return None

def visualize_timeline(timestamps, captions, video_duration, save_path=None):
    """
    Visualize keyframe timestamps on a timeline.
    
    Args:
        timestamps: List of timestamp values in seconds
        captions: List of captions corresponding to timestamps
        video_duration: Total duration of the video in seconds
        save_path: Optional path to save the visualization
        
    Returns:
        Path to the saved visualization
    """
    try:
        plt.figure(figsize=(15, 5))
        
        # Create the timeline
        plt.plot([0, video_duration], [0, 0], 'k-', linewidth=2)
        
        # Add timestamp markers
        for i, (timestamp, caption) in enumerate(zip(timestamps, captions)):
            plt.plot([timestamp, timestamp], [-0.2, 0.2], 'r-', linewidth=2)
            plt.text(timestamp, 0.3, f"{timestamp:.2f}s", ha='center', fontsize=10)
            
            # Add caption (truncated if too long)
            if len(caption) > 30:
                caption = caption[:27] + "..."
            plt.text(timestamp, -0.4, caption, ha='center', va='top', fontsize=9, rotation=45)
        
        # Add start and end markers
        plt.text(0, -0.2, "0:00", ha='center', va='top')
        plt.text(video_duration, -0.2, f"{int(video_duration//60)}:{int(video_duration%60):02d}", 
                 ha='center', va='top')
        
        # Set axis limits and hide axes
        plt.xlim(-video_duration*0.05, video_duration*1.05)
        plt.ylim(-2, 1)
        plt.axis('off')
        
        plt.title("Video Timeline with Keyframe Timestamps")
        plt.tight_layout()
        
        # Save the visualization
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if not save_path:
            save_path = f"video_timeline_{timestamp}.png"
            
        plt.savefig(save_path, bbox_inches='tight')
        
        # Save data alongside figure
        data_path = os.path.splitext(save_path)[0] + '_data.json'
        with open(data_path, 'w') as f:
            data = {"timestamps": timestamps, "captions": captions, "video_duration": video_duration}
            json.dump(data, f, indent=4)
        print(f"Timeline data saved to {data_path}")
            
        print(f"Timeline visualization saved to {save_path}")
        return save_path
    except Exception as e:
        traceback.print_exc()
        print(f"Error visualizing timeline: {str(e)}")
        return None