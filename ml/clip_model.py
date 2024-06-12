import cv2
import torch
import numpy as np
from PIL import Image
from transformers import AutoProcessor, CLIPVisionModelWithProjection
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize, InterpolationMode


class CLIPmodel:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = CLIPVisionModelWithProjection.from_pretrained('Searchium-ai/clip4clip-webvid150k').to(self.device)
        self.processor = AutoProcessor.from_pretrained('Searchium-ai/clip4clip-webvid150k')

    def video2image(self, video_path, frame_rate=1.0, size=224):
        def preprocess(size, n_px):
            return Compose([
                Resize(size, interpolation=InterpolationMode.BICUBIC),
                CenterCrop(size),
                lambda image: image.convert("RGB"),
                ToTensor(),
                Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
            ])(n_px)

        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if fps < 1:
            images = np.zeros([3, size, size], dtype=np.float32)
            print('ERROR: problem reading video file: ', video_path)
        else:
            total_duration = (frameCount + fps - 1) // fps
            start_sec, end_sec = 0, total_duration
            interval = fps / frame_rate
            frames_idx = np.floor(np.arange(start_sec * fps, end_sec * fps, interval))
            ret = True
            images = np.zeros([len(frames_idx), 3, size, size], dtype=np.float32)

            for i, idx in enumerate(frames_idx):
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                last_frame = i
                images[i, :, :, :] = preprocess(size, Image.fromarray(frame).convert('RGB'))

            images = images[:last_frame + 1]
        cap.release()
        video_frames = torch.tensor(images)

        return video_frames

    def get_video_embeddings(self, path):
        self.model = self.model.eval()

        video = self.video2image(path).to(self.device)
        visual_output = self.model(video)

        visual_output = visual_output['image_embeds']
        visual_output = visual_output / visual_output.norm(dim=-1, keepdim=True)
        visual_output = torch.mean(visual_output, dim=0)
        visual_output = visual_output / visual_output.norm(dim=-1, keepdim=True)

        return visual_output
