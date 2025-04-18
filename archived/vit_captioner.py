import os
import matplotlib.pyplot as plt
from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

class ImageCaptioner:
    def __init__(self, model_name="nlpconnect/vit-gpt2-image-captioning"):
        # Load model, tokenizer, and feature extractor
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.feature_extractor = ViTImageProcessor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Configure device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Set generation kwargs
        self.gen_kwargs = {"max_length": 16, "num_beams": 4}

    def predict_caption(self, image_path, save_image=True):
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
                print("Error in saving captioned image: ", str(e))


        return caption

    def save_captioned_image(self, img, caption, image_path):
        # Adjust path to use current directory if it's empty
        output_dir = os.path.dirname(image_path) or '.'
        img_save_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_captioned.jpg')
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.imshow(img)
        plt.title(caption)
        plt.axis("off")
        plt.savefig(img_save_path, bbox_inches="tight")
        plt.clf()
        plt.close()
        print(f"Image saved to {img_save_path}")

# Example usage
if __name__ == "__main__":
    image_path = 'IMG_9421_2024_04_23_07_52_02_COMPLETED_cover_plain.jpg'  # Adjust this path as needed
    captioner = ImageCaptioner()
    caption = captioner.predict_caption(image_path, save_image=True)
    print(f"Caption: {caption}")
