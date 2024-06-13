import cv2
import numpy as np
import face_recognition


class FaceFounder():
    def __init__(self):
        pass

    def from_file(self, video_path):
        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
        images = self.get_frames(cap)
        unique = self.get_unique(images)
        return unique

    def get_frames(self, cap):
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        images = []
        if fps < 1:
            print('ERROR: problem reading video file: ')
        else:
            total_duration = (frameCount + fps - 1) // fps
            start_sec, end_sec = 0, total_duration
            interval = fps
            frames_idx = np.floor(np.arange(start_sec * fps, end_sec * fps, interval))
            ret = True

            for i, idx in enumerate(frames_idx):
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                images.append(frame)

        cap.release()
        return frame

    def get_frames_polnostju(self, fp):
        cap = cv2.VideoCapture(fp, cv2.CAP_FFMPEG)

        success, frame = cap.read()

        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_duration = (frameCount + fps - 1) // fps

        frame_interval = max([2, total_duration / 6])

        images = []
        count = 0

        while success:
            if count % int(frame_interval * fps) == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                images.append(frame)
            success, frame = cap.read()
            count += 1
        cap.release()

        return images

    def get_unique(self, images, video_id):
        face_locations = [face_recognition.face_locations(img) for img in images]

        face_encodings = []
        for i in range(len(images)):
            for f in face_recognition.face_encodings(images[i], face_locations[i]):
                face_encodings.append(f)

        diff_encodings = []
        enc_counter = []
        for e in face_encodings:
            found = False
            mask = face_recognition.compare_faces(diff_encodings, e)
            if True not in mask:
                diff_encodings.append(e)
                enc_counter.append(1)
            else:
                ind = mask.index(True)
                diff_encodings[ind] += e
                diff_encodings[ind] /= 2
                enc_counter[ind] += 1

        enc_pairs = [[diff_encodings[i], enc_counter[i]] for i in range(len(enc_counter))]
        enc_pairs.sort(key=lambda x: x[1])
        data = []
        for i, enc in enumerate(reversed(enc_pairs)):
            data.append([video_id, enc[0], i])

        return data

    def process_file(self, fp, vid):
        images = self.get_frames_polnostju(fp)
        return self.get_unique(images, vid)
