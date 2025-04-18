"""
captioning/image.py - Module for generating captions for images using ViT-GPT2 model
"""

import os
import matplotlib.pyplot as plt
from PIL import Image
import torch
import numpy as np
import traceback
import random
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

class ImageCaptioner:
    def __init__(self, model_name="nlpconnect/vit-gpt2-image-captioning"):
        try:
            # Set random seed for reproducibility
            random.seed(23)
            torch.manual_seed(23)
            np.random.seed(23)
            
            # Load model, tokenizer, and feature extractor
            self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
            self.feature_extractor = ViTImageProcessor.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Configure device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            # Set generation kwargs
            self.gen_kwargs = {"max_length": 16, "num_beams": 4}
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error initializing ImageCaptioner: {str(e)}")

    def predict_caption(self, image_path, save_image=True):
        """
        Generate a caption for an image using the ViT-GPT2 model.
        
        Args:
            image_path: Path to the image file
            save_image: Whether to save the captioned image
            
        Returns:
            caption: Generated caption for the image
        """
        try:
            # Load and process image
            image = Image.open(image_path).convert("RGB")
            
            # Process image and generate captions
            pixel_values = self.feature_extractor(images=[image], return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            
            output_ids = self.model.generate(pixel_values, **self.gen_kwargs)
            captions = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
            caption = captions[0].strip()

            if save_image:
                try:
                    self.save_captioned_image(image, caption, image_path)
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error in saving captioned image: {str(e)}")

            return caption
        except Exception as e:
            traceback.print_exc()
            print(f"Error predicting caption: {str(e)}")
            return "Error generating caption"

    def save_captioned_image(self, img, caption, image_path):
        """
        Save the image with its caption overlaid.
        
        Args:
            img: PIL Image object
            caption: Caption text
            image_path: Path to original image
        """
        try:
            # Adjust path to use current directory if it's empty
            output_dir = os.path.dirname(image_path) or '.'
            img_save_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_captioned.jpg')
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            plt.figure(figsize=(10, 10))
            plt.imshow(img)
            plt.title(caption)
            plt.axis("off")
            plt.savefig(img_save_path, bbox_inches="tight")
            
            # Save the caption data alongside the figure
            caption_data_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_caption_data.txt')
            with open(caption_data_path, 'w') as f:
                f.write(caption)
                
            plt.clf()
            plt.close()
            print(f"Image saved to {img_save_path}")
            print(f"Caption data saved to {caption_data_path}")
        except Exception as e:
            traceback.print_exc()
            print(f"Error saving captioned image: {str(e)}")