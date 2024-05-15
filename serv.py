import socket as sk
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from moviepy.editor import VideoFileClip

def decouper_video_en_images(video_path, output_folder):
    # Assurez-vous que le dossier de sortie existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Charger la vidéo
    video = VideoFileClip(video_path)

    # Parcourir chaque trame de la vidéo
    for i, frame in enumerate(video.iter_frames()):
        # Enregistrer la trame sous forme d'image
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        frame.save_frame(frame_path)

    # Fermer la vidéo
    video.close()

def preprocess_image(file):
    img = image.load_img(file, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def verifie():
    b, c = 0, 0
    model = load_model("model.h5")
    for i in os.listdir("sortie"):
        img = preprocess_image("sortie/" + i)
        b += model.predict(img)[0][0]
        c += 1
    
    if b/c > 0.55:
        return 1
    else:
        return 0

s = sk.gethostbyname(sk.gethostname())
print(s, 1059)
sock = sk.socket()
sock.bind((s, 1059))
sock.listen()

while True:
    d, a = sock.accept()
    with open("video.mp4", "wb") as f:
        while True:
            data = d.recv(4096)
            if not data:
                break
            f.write(data)
    decouper_video_en_images("video.mp4", "sortie")
    x = verifie()
    d.send(str(x).encode())  # Envoyer la réponse en tant que chaîne de caractères
    d.close()  # Fermer le socket accepté après avoir envoyé la réponse
    break

sock.close()
