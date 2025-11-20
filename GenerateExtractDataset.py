import json
import os
import cv2
from tqdm import tqdm
from typing import List
import re

# --- CONFIGURATION ---

set = "test"
# Chemins à adapter
GLOBAL_JSON_PATH = "./JSON_GLOBAL_FULL/global_annotations.json"
SEQUENCE_LIST_PATH = f"./dataset_config/{set}.txt"  # liste des vidéos à récupérer
DISTORTION_DIR = "./distortion_type_"             # contient les distorsions par vidéo
VIDEOS_DIR = "./distorted_video/distorted_video"                          # dossier contenant les vidéos .mp4  C:/Users/beghd/Downloads/distorted_video/distorted_video
OUTPUT_JSON_PATH = f"./dataset_config/{set}.json"
OUTPUT_FRAMES_DIR = "./dataset_config/filtered_frames"

# Extraction activée ou non
EXTRACT_FRAMES = False

# --- FONCTIONS UTILITAIRES ---

def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def read_txt_lines(path: str) -> List[str]:
    if not os.path.exists(path):
        print(f"⚠️ Fichier introuvable : {path}")
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def extract_frames_from_videos(images, videos_dir, output_dir):
    """
    Extrait les frames correspondant aux images sélectionnées à partir des vidéos .mp4.
    Suppose que :
    - chaque image a un champ "video_name"
    - son "file_name" contient le numéro de frame (ex: frame_0012.jpg)
    """
    os.makedirs(output_dir, exist_ok=True)

    counter = 0
    # Regrouper les images par vidéo
    video_groups = {}
    for img in images:
        video_name = img.get("video_name")
        video_dist = img.get("distortion_type")
        video_level = img.get("severity_level")
        video_name = video_name + "/" + video_name + "_" + str(video_dist) + "_" + str(video_level)
        # video_name = video_name + "_" + video_dist + "_" + video_level
        if not video_name:
            continue
        video_groups.setdefault(video_name, []).append(img)

    for video_name, img_list in video_groups.items():
        video_path = os.path.join(videos_dir, f"{video_name}.mp4")
        if not os.path.exists(video_path):
            print(f"❌ Vidéo introuvable : {video_path}")
            continue

        print(f"🎬 Extraction des frames pour {video_name} ({len(img_list)} images)")

        # Charger la vidéo
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ Impossible d’ouvrir la vidéo : {video_path}")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Trouver les indices de frame à extraire
        frame_indices = []
        for img in img_list:
            # Essaie de trouver un indice dans le nom du fichier (ex: frame_000123.jpg)
            filename = img["file_name"]
            match = re.search(r'_(\d{4})\.jpg$', filename)
            if match:
                digits = match.group(1)
            else:
                digits = None
            # digits = ''.join([c for c in filename if c.isdigit()])
            if digits:
                frame_indices.append(int(digits))
        frame_indices = sorted(set(frame_indices))

        print(f"🔢 Frames à extraire : {len(frame_indices)} / {total_frames}")

        # Lecture séquentielle et extraction
        frame_pos = 0
        next_target = frame_indices.pop(0) if frame_indices else None
        # print("Open tqdm process...")
        with tqdm(total=total_frames, desc=f"📸 {video_name}", unit="frame") as pbar:
            while cap.isOpened():
                if next_target is None:
                    break  # plus rien à extraire → on sort

                ret, frame = cap.read()
                if not ret:
                    print(f"⚠️ Fin de la vidéo atteinte prématurément à la frame {frame_pos}")
                    break

                if counter < 5:
                    print(f'Next_target: {next_target}  Frame Pose: {frame_pos}')
                counter += 1
                if next_target is not None and frame_pos == next_target:
                    if counter < 5:
                        print('Next_target')
                    counter += 1
                    # Trouver toutes les images correspondant à ce numéro
                    matching_imgs = [
                        img for img in img_list
                        if str(next_target) in img["file_name"]
                    ]
                    for img in matching_imgs:
                        out_path = os.path.join(output_dir, img["file_name"])
                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                        cv2.imwrite(out_path, frame)
                        if counter < 5:
                            print(f'img ecrite path: {out_path}')
                        counter += 1
                    # Passer à la prochaine frame cible
                    next_target = frame_indices.pop(0) if frame_indices else None

                frame_pos += 1
                pbar.update(1)

                if next_target is None:
                    break

        cap.release()
        print(f"✅ Extraction terminée pour {video_name}")

# --- CHARGEMENT DU FICHIER GLOBAL ---
print(f"📂 Lecture du fichier global : {GLOBAL_JSON_PATH}")
global_data = load_json(GLOBAL_JSON_PATH)

# --- LECTURE DES SÉQUENCES À EXTRAIRE ---
video_names = read_txt_lines(SEQUENCE_LIST_PATH)
if not video_names:
    print("❌ Aucun nom de séquence trouvé.")
    exit(1)

print(f"▶️ Séquences sélectionnées : {video_names}")

# --- FILTRAGE DES DONNÉES ---
selected_images = []
selected_annotations = []

cpt = 0
for video_name in video_names:
    dist_file = os.path.join(DISTORTION_DIR, f"{video_name}.txt")
    distortion_types = read_txt_lines(dist_file)
    if not distortion_types:
        print(f"⚠️ Pas de distorsions trouvées pour {video_name}")
        continue

    print(f"🎞️ {video_name} : distorsions sélectionnées → {distortion_types}")

    for img in global_data["images"]:
        if img.get("video_name") == video_name and img.get("distortion_type") in distortion_types:
            selected_images.append(img)
            if cpt < 2:
                print(img)
            cpt += 1

selected_img_ids = {img["id"] for img in selected_images}

for ann in global_data["annotations"]:
    if ann["image_id"] in selected_img_ids:
        selected_annotations.append(ann)

print(f"🖼️ Images sélectionnées : {len(selected_images)}")
print(f"🔢 Annotations sélectionnées : {len(selected_annotations)}")

# --- CONSTRUCTION DU NOUVEAU JSON ---
filtered_data = {
    "info": {
        "description": "Subset of global COCO annotations based on selected videos and distortions",
        "version": "1.0",
        "year": 2025
    },
    "licenses": global_data.get("licenses", []),
    "categories": global_data.get("categories", []),
    "images": selected_images,
    "annotations": selected_annotations
}

# --- SAUVEGARDE DU NOUVEAU JSON ---
save_json(filtered_data, OUTPUT_JSON_PATH)
print(f"✅ Fichier JSON filtré sauvegardé : {OUTPUT_JSON_PATH}")

# --- EXTRACTION DES FRAMES (optionnelle) ---
if EXTRACT_FRAMES:
    print("📦 Extraction des frames à partir des vidéos...")
    extract_frames_from_videos(selected_images, VIDEOS_DIR, OUTPUT_FRAMES_DIR)
    print(f"✅ Frames extraites vers : {OUTPUT_FRAMES_DIR}")

print("🎯 Traitement terminé avec succès.")
