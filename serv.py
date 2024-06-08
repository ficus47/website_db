from flask import Flask, request
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from moviepy.editor import VideoFileClip
import keras
from keras.layers import BatchNormalization

class CustomBatchNormalization(BatchNormalization):
    @classmethod
    def from_config(cls, config):
        # Convert axis from list to int if necessary
        if isinstance(config.get('axis'), list):
            config['axis'] = config['axis'][0]
        return super().from_config(config)

# Register the custom layer
keras.utils.get_custom_objects().update({'BatchNormalization': CustomBatchNormalization})

app = Flask(__name__)

def decouper_video_en_images(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = VideoFileClip(video_path)
    for i, frame in enumerate(video.iter_frames()):
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        video.save_frame(frame_path, t=i / video.fps)
        print(f"Enregistrement de la trame {i + 1}/{video.duration * video.fps}")
    video.close()

def preprocess_image(file):
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def verifie():
    b, c = 0, 0
    model = keras.models.load_model("model_efficientnet.h5")
    for i in os.listdir("sortie"):
        img = preprocess_image("sortie/" + i)
        b += model.predict(img)[0][0]
        c += 1
    
    return 1 if b/c > 0.55 else 0

@app.route('/upload', methods=['GET'])
def handle_video():
    data = request.data
    save_video(data)
    decouper_video_en_images("video.mp4", "sortie")
    result = verifie()
    return str(result)

def save_video(data):
    with open("video.mp4", "wb") as f:
        f.write(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
