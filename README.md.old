# VideoCaptionerWithVit

A command-line utility to generate time‑aligned captions for any video by extracting key‑frames (via Katna or OpenCV) and running them through a pre-trained Vision Transformer (ViT) + GPT‑2 image captioning model.

---

## 🚀 Features

- **Key‑frame extraction**  
  - Primary: [Katna](https://github.com/bhattbhavesh91/Katna) for smart saliency-based frames  
  - Fallback: Uniform sampling via OpenCV  
- **Caption generation**  
  - Uses Hugging Face’s [`nlpconnect/vit-gpt2-image-captioning`](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) model under the hood  
- **Multi‑threaded processing** for faster captioning on long videos  
- **Outputs**  
  - `.srt` subtitle file  
  - `.json` with timestamped captions  

---

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/<your‑username>/VideoCaptionerWithVit.git
   cd VideoCaptionerWithVit
   ```
2. Create & activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ Usage

```bash
python vit_captioner_video.py \
  --video_path path/to/your/video.mp4 \
  --num_frames 10
```

- `--video_path` (`-V`): input video file  
- `--num_frames` (`-N`): how many key‑frames to caption (default: 10)

After running, you’ll get:
- `video_captioning_frames/` (extracted frames)
- `video_caption.srt`
- `video_caption.json`

---

## 🔗 Upstream & Inspiration

- **Image captioning model**:  
  [`nlpconnect/vit-gpt2-image-captioning`](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) by NLP Connect  
- **Key‑frame extraction**:  
  [Katna](https://github.com/bhattbhavesh91/Katna) for smart saliency-based sampling  
- **Fallback frame sampling**:  
  OpenCV’s `CAP_PROP_POS_FRAMES` uniform slicing  

---

## 📁 Repo Structure

```
.
├── vit_captioner.py           # wraps ViT-GPT2 model for single-image captions
├── vit_captioner_video.py     # video-to-SRT/JSON pipeline
├── keyframes_extractor.py     # Katna-based key-frame extraction
├── data/                      # (optional) place your test videos here
├── frames_output/             # example output folder
├── requirements.txt           # pip dependencies
└── README.md                  # this file
```

---

## 🤝 Contributing

1. Fork it  
2. Create a feature branch (`git checkout -b feat/YourFeature`)  
3. Commit your changes (`git commit -m 'Add feature'`)  
4. Push to the branch (`git push origin feat/YourFeature`)  
5. Open a Pull Request  

---

## 📄 License

MIT © Lachlan Chen
