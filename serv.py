from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from moviepy.editor import VideoFileClip
import asyncio
import websockets
import socket

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
    img = image.load_img(file, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def verifie():
    b, c = 0, 0
    model = load_model("model_image.keras")
    for i in os.listdir("sortie"):
        img = preprocess_image("sortie/" + i)
        b += model.predict(img)[0][0]
        c += 1
    
    return 1 if b/c > 0.55 else 0

async def save_video(data):
    with open("video.mp4", "wb") as f:
        f.write(data)

async def handle_video(websocket, path):
    async for message in websocket:
        await save_video(message)
        decouper_video_en_images("video.mp4", "sortie")
        result = verifie()
        await websocket.send(str(result))

async def main():
    server_ip = socket.gethostbyname(socket.gethostname())
    async with websockets.serve(handle_video, server_ip, 8765, max_size=1024*1024*32):
        print(f"Serveur WebSocket démarré sur {server_ip}:8765")
        await asyncio.Future()

asyncio.run(main())
