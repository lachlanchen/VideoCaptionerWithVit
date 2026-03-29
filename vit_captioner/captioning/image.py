"""
captioning/image.py - Module for generating captions for images using ViT-GPT2 model
"""

import os
import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import torch
import numpy as np
import traceback
import random
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import warnings

# Filter out transformer warnings
warnings.filterwarnings("ignore", category=UserWarning, 
                       message="Some weights of the model checkpoint.*")

class ImageCaptioner:
    # Class variable to track if warnings have been displayed
    _showed_warnings = False
    
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
            caption_data_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_caption_data.txt')
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the caption data separately
            with open(caption_data_path, 'w') as f:
                f.write(caption)
            
            try:
                if isinstance(img, Image.Image):
                    base_image = img.convert("RGBA")
                else:
                    base_image = Image.fromarray(img).convert("RGBA")

                overlay = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                font = ImageFont.load_default()
                wrap_width = max(20, base_image.width // 12)
                wrapped_caption = textwrap.fill(caption, width=wrap_width)
                padding = 12
                spacing = 4

                try:
                    bbox = draw.multiline_textbbox((0, 0), wrapped_caption, font=font, spacing=spacing)
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    _text_width, text_height = draw.multiline_textsize(
                        wrapped_caption,
                        font=font,
                        spacing=spacing,
                    )

                box_height = text_height + (padding * 2)
                box_top = max(0, base_image.height - box_height)
                draw.rectangle(
                    (0, box_top, base_image.width, base_image.height),
                    fill=(0, 0, 0, 160),
                )
                draw.multiline_text(
                    (padding, box_top + padding),
                    wrapped_caption,
                    fill=(255, 255, 255, 255),
                    font=font,
                    spacing=spacing,
                )

                composed = Image.alpha_composite(base_image, overlay).convert("RGB")
                composed.save(img_save_path, quality=95)
                print(f"Image saved to {img_save_path}")
                print(f"Caption data saved to {caption_data_path}")
            except Exception as e:
                # If caption overlay fails, save the original image instead.
                if isinstance(img, Image.Image):
                    img.save(img_save_path)
                    print(f"Saved original image to {img_save_path} (caption overlay failed: {str(e)})")
                else:
                    raise e
                
        except Exception as e:
            traceback.print_exc()
            print(f"Error saving captioned image: {str(e)}")
