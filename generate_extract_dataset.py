import json
import os
import cv2
from tqdm import tqdm
from typing import List
import re
import argparse

# --- CONFIGURATION ---

# Argument parser
parser = argparse.ArgumentParser(description="Process videos, annotations, and frames based on selected sequences and distortions.")
parser.add_argument('--set', type=str, required=True, help="Name of the dataset to process (e.g. 'test').")
parser.add_argument('--global-json-path', type=str, required=True, help="Path to the global annotations JSON file.")
parser.add_argument('--sequence-list-path', type=str, required=True, help="Path to the text file containing the list of videos to retrieve.")
parser.add_argument('--distortion-dir', type=str, required=True, help="Directory containing distortion files per video.")
parser.add_argument('--videos-dir', type=str, required=True, help="Directory containing the .mp4 videos.")
parser.add_argument('--output-json-path', type=str, required=True, help="Path where the filtered JSON file will be saved.")
parser.add_argument('--output-frames-dir', type=str, required=True, help="Directory where the extracted frames will be saved.")
parser.add_argument('--extract-frames', action='store_true', help="If enabled, extracts frames from the videos.")
args = parser.parse_args()

# Assign variables from arguments
set = args.set
GLOBAL_JSON_PATH = args.global_json_path
SEQUENCE_LIST_PATH = args.sequence_list_path
DISTORTION_DIR = args.distortion_dir
VIDEOS_DIR = args.videos_dir
OUTPUT_JSON_PATH = args.output_json_path
OUTPUT_FRAMES_DIR = args.output_frames_dir
EXTRACT_FRAMES = args.extract_frames

# --- HELPER FUNCTIONS ---

def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def read_txt_lines(path: str) -> List[str]:
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def extract_frames_from_videos(images, videos_dir, output_dir):
    """
    Extracts frames corresponding to the selected images from .mp4 videos.
    Assumes that:
    - each image has a "video_name" field
    - its "file_name" contains the frame number (e.g., frame_0012.jpg)
    """
    os.makedirs(output_dir, exist_ok=True)

    counter = 0
    # Group images by video
    video_groups = {}
    for img in images:
        video_name = img.get("video_name")
        video_dist = img.get("distortion_type")
        video_level = img.get("severity_level")
        video_name = video_name + "/" + video_name + "_" + str(video_dist) + "_" + str(video_level)
        if not video_name:
            continue
        video_groups.setdefault(video_name, []).append(img)

    for video_name, img_list in video_groups.items():
        video_path = os.path.join(videos_dir, f"{video_name}.mp4")
        if not os.path.exists(video_path):
            print(f"❌ Video not found: {video_path}")
            continue

        print(f"🎬 Extracting frames for {video_name} ({len(img_list)} images)")

        # Load the video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ Unable to open video: {video_path}")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Find the frame indices to extract
        frame_indices = []
        for img in img_list:
            filename = img["file_name"]
            match = re.search(r'_(\d{4})\.jpg$', filename)
            if match:
                digits = match.group(1)
            else:
                digits = None
            if digits:
                frame_indices.append(int(digits))
        frame_indices = sorted(set(frame_indices))

        print(f"🔢 Frames to extract: {len(frame_indices)} / {total_frames}")

        # Sequential reading and extraction
        frame_pos = 0
        next_target = frame_indices.pop(0) if frame_indices else None
        with tqdm(total=total_frames, desc=f"📸 {video_name}", unit="frame") as pbar:
            while cap.isOpened():
                if next_target is None:
                    break  # No more frames to extract → exit

                ret, frame = cap.read()
                if not ret:
                    print(f"⚠️ End of video reached prematurely at frame {frame_pos}")
                    break

                if next_target is not None and frame_pos == next_target:
                    matching_imgs = [
                        img for img in img_list
                        if str(next_target) in img["file_name"]
                    ]
                    for img in matching_imgs:
                        out_path = os.path.join(output_dir, img["file_name"])
                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                        cv2.imwrite(out_path, frame)
                    # Move to the next target frame
                    next_target = frame_indices.pop(0) if frame_indices else None

                frame_pos += 1
                pbar.update(1)

                if next_target is None:
                    break

        cap.release()
        print(f"✅ Extraction complete for {video_name}")

# --- LOADING THE GLOBAL FILE ---
print(f"📂 Reading global file: {GLOBAL_JSON_PATH}")
global_data = load_json(GLOBAL_JSON_PATH)

# --- READING SEQUENCES TO EXTRACT ---
video_names = read_txt_lines(SEQUENCE_LIST_PATH)
if not video_names:
    print("❌ No sequence names found.")
    exit(1)

print(f"▶️ Selected sequences: {video_names}")

# --- FILTERING DATA ---
selected_images = []
selected_annotations = []

for video_name in video_names:
    dist_file = os.path.join(DISTORTION_DIR, f"{video_name}.txt")
    distortion_types = read_txt_lines(dist_file)
    if not distortion_types:
        print(f"⚠️ No distortions found for {video_name}")
        continue

    print(f"🎞️ {video_name} : selected distortions → {distortion_types}")

    for img in global_data["images"]:
        if img.get("video_name") == video_name and img.get("distortion_type") in distortion_types:
            selected_images.append(img)

selected_img_ids = {img["id"] for img in selected_images}

for ann in global_data["annotations"]:
    if ann["image_id"] in selected_img_ids:
        selected_annotations.append(ann)

print(f"🖼️ Selected images: {len(selected_images)}")
print(f"🔢 Selected annotations: {len(selected_annotations)}")

# --- BUILDING THE NEW JSON ---
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

# --- SAVING THE NEW JSON ---
save_json(filtered_data, OUTPUT_JSON_PATH)
print(f"✅ Filtered JSON file saved: {OUTPUT_JSON_PATH}")

# --- FRAME EXTRACTION (optional) ---
if EXTRACT_FRAMES:
    print("📦 Extracting frames from the videos...")
    extract_frames_from_videos(selected_images, VIDEOS_DIR, OUTPUT_FRAMES_DIR)
    print(f"✅ Frames extracted to: {OUTPUT_FRAMES_DIR}")

print("🎯 Processing completed successfully.")
