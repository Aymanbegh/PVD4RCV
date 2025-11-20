import os
import cv2
import argparse
import json
from tqdm import tqdm
from typing import List
import re

# --- CONFIGURATION ---
frame_format = "{video}_{dist}_lvl{lvl}_frame_{num:04d}.jpg"
severity_levels = [1, 2, 3, 4]

# --- Argument parser for command line arguments ---
parser = argparse.ArgumentParser(description="Extract frames from a video and rename them based on distortions and levels.")
parser.add_argument('--input-dir', type=str, default='C:/Users/beghd/Downloads/distorted_video/distorted_video', help="Directory containing the distorted videos. Default is './Distorted'.")
parser.add_argument('--output-dir', type=str, default='./dist', help="Directory where extracted frames will be saved. Default is './Frames'.")
parser.add_argument('--name-txt', type=str, default='name_txt_.txt', help="Path to the 'name_txt.txt' file containing the video names. Default is 'name_txt.txt'.")
parser.add_argument('--distortion-dir', type=str, default='./distortion_type_', help="Directory containing distortion files for each video. Default is './DistortionType'.")
args = parser.parse_args()

# --- Create output directory ---
os.makedirs(args.output_dir, exist_ok=True)

# --- Lire les noms des vidéos à partir du fichier spécifié ---
name_txt_path = args.name_txt
if not os.path.exists(name_txt_path):
    print(f"❌ '{name_txt_path}' file not found.")
    exit()

with open(name_txt_path, "r") as f:
    video_names = [line.strip() for line in f if line.strip()]

# --- Fonction pour lire les distorsions d'un fichier pour chaque vidéo ---
def read_distortions_for_video(video_name: str, distortion_dir: str):
    distortion_file = os.path.join(distortion_dir, f"{video_name}.txt")
    if os.path.exists(distortion_file):
        with open(distortion_file, "r") as f:
            distortions = [line.strip() for line in f if line.strip()]
        return distortions
    else:
        print(f"⚠️ Distortion file not found for {video_name}: {distortion_file}")
        return []

# --- Traitement des vidéos ---
for video_name in video_names:
    # Lire les distorsions pour chaque vidéo
    distortions = read_distortions_for_video(video_name, args.distortion_dir)
    if not distortions:
        print(f"⚠️ No distortions found for {video_name}. Skipping.")
        continue

    print(f"▶️ Processing: {video_name}.mp4 with distortions: {distortions}")
    for dist in distortions:
        for level in severity_levels:
            path = os.path.join(args.input_dir, video_name)
            video_path = os.path.join(path,f"{video_name}_{dist}_{level}.mp4")
            print(video_path)  # Optionnel, juste pour vérifier le chemin généré
            if not os.path.exists(video_path):
                print(f"❌ Video not found: {video_path}")
                continue

            # Charger la vidéo
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"❌ Unable to open video: {video_path}")
                continue

            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_idx += 1

                # Pour chaque distorsion et niveau, enregistrer une version de la frame
                # for dist in distortions:
                frame_name = frame_format.format(
                    video=video_name,
                    dist=dist,
                    lvl=level,
                    num=frame_idx
                )
                output_path = os.path.join(args.output_dir, frame_name)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                cv2.imwrite(output_path, frame)

        cap.release()
        print(f"✅ {frame_idx} frames extracted and renamed for {video_name}\n")

print("🎉 Extraction and renaming completed.")
