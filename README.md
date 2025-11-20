# PVD4RCV Dataset

*A Photo-realistic Multi-Distortion Video Dataset for Benchmarking and Developing Robust Computer Vision Models*


<p align="center">
  <img width="1491" height="860" alt="DatasetView" src="https://github.com/user-attachments/assets/c2de080a-5c42-4dba-b07c-d5dcdd4e0fad" />
</p>


## 📌 Description

**PVD4RCV** (Photo-realistic Multi-Distortion Video Dataset for Robust Computer Vision) is a unique video database designed for evaluating and developing robust computer vision models.

Unlike traditional datasets where distortions are applied artificially, PVD4RCV incorporates **real physical factors** (scene depth, light interaction, motion dynamics) to generate photo-realistic distortions such as:

* Local and global motion blur
* Local and global defocus blur
* Compression and transmission artifacts
* Noise
* Contrast reduction
* Haze and smoke
* Depth-aware realistic rain

Each sequence is provided with depth maps and annotations to support tasks such as object detection, tracking, and distortion classification.

---

## 📂 Dataset Content

* **24 original videos** (10 seconds each)
* **672 distorted videos** with 4 severity levels
* **Complete annotations**: object bounding boxes and labels
* **Associated depth maps**
* **Resolution**: 1920×1080 (Full HD)
* **Frame rate**: 29.93 – 30 fps
* **Format**: MP4
* **Total size**: ~21.2 GB

## 🧩 Dataset Split — Training / Validation / Test
| Set            | Number of Sequences | Percentage | Description                                                                      |
| :------------- | :-----------------: | :--------: | :------------------------------------------------------------------------------- |
| **Training**   |     16 sequences    |  **≈ 67%** | Used for model training — includes diverse environments and all distortion types |
| **Validation** |     4 sequences     |  **≈ 17%** | Used to tune hyperparameters and monitor model generalization                    |
| **Test**       |     4 sequences     |  **≈ 17%** | Held-out subset for final performance evaluation under unseen conditions         |

🗂 Note:
Each subset contains both original and distorted versions of the videos (all 4 severity levels).
Splitting ensures scene disjointness — i.e., no identical scenes appear across training, validation, and test sets, ensuring a fair robustness evaluation.

### Objects distribution
<img width="3600" height="1800" alt="class_distribution_global" src="https://github.com/user-attachments/assets/509870e1-1a22-4e46-83e8-32b41afec4d2" />


### 🌍 Scenarios included

* Road traffic
* Parking lots
* Stadiums and crowds
* Airports
* Shopping malls
* Urban streets and train stations
* Sea navigation

---

## 🚀 Preparing the PVD4RCV Dataset

Before setting up the GroundTruth structure, make sure to download the complete dataset, which includes:

🧩 Original and distorted videos (all 24 sequences × 4 distortion levels × multiple types)

🌈 Depth maps associated with each video sequence

🗂️ Annotation files (bounding boxes, object classes, and depth map)

You can download the full dataset package from the official link:
👉 Download PVD4RCV Dataset

## 🧰 Step 1 — Extract video frames

Once the dataset is downloaded and extracted locally, run the provided Python script to extract frames from each video sequence and store them in structured folders.

Each frame will be automatically renamed following this convention: **{video_name}_{dist}_lvl{lvl}_{original_frame_name}**
* **video_name**: The name of the video.
* **dist**: The distortion type applied to the video (e.g., rain, blur).
* **lvl**: The severity level of the distortion (e.g., 1, 2, 3, 4).
* **num**: The frame index (e.g., 0001, 0002, etc.).
  
Example:

```
traffic_rain_lvl2_frame_00045.jpg
airport_blur_lvl4_frame_00012.jpg
```

This naming pattern ensures clear identification of the scene, distortion type, and severity level for every frame, making it easy to track and analyze the extracted frames.

**How to Run:**

To run the script, use the following command from the project root:

```
python extract_frames.py --input-dir ./PVD4RCV/Distorted --output-dir ./PVD4RCV/Frames --name-txt ./list_sequences.txt --distortion-dir ./distortion_type_
```

**Where:**
* `--input-dir` specifies the directory containing the distorted videos.
* `--output-dir` specifies the directory where the frames will be saved.
* `--name-txt` specifies the path to the text file containing the list of video names.
* `--distortion-dir` specifies the directory containing the distortion files for each video.

**What this Script Does:**
* Reads the video names from the specified name_txt_.txt file.
* Reads distortion metadata for each video from corresponding .txt files in the distortion-dir.
* Iterates through all videos and distortions for each scene, loading the video using OpenCV (cv2.VideoCapture).
* Extracts individual frames from each video and saves them using the naming pattern described above.
* Preserves scene and distortion metadata, ensuring traceability of the extracted frames.

**Requirements:**
* Python ≥ 3.8
* Required libraries: `opencv-python`, `tqdm`, `os`, `argparse`
(install via `pip install -r requirements.txt` if needed)


## 🧩 Step 2 — Generate a custom JSON subset (optional)

If you want to train or evaluate your models on a subset of the dataset — for example, only a few specific sequences instead of the full training, validation, or test sets — you can use the provided JSON generation script.

This script allows you to:
* Select only the video sequences you wish to include
* Merge their corresponding annotations into a single COCO-style JSON file
* Automatically include the correct file naming (e.g. video_dist_lvl_frame.jpg)
* Save the result as a ready-to-use global_annotations.json

🧭 **How to use it**
**1.** Create a text file named `list_sequences.txt` containing the list of sequences to include, e.g.:

```
traffic
airport
mall
```
**2.** Place this file at the root of your project (or next to the script).

**3.** Run the script:

```
python generate_extract_dataset.py --set <dataset_name> --global-json-path <path_to_set_annotations.json> --sequence-list-path <path_to_sequence_list.txt> --distortion-dir <path_to_distortion_files> --videos-dir <path_to_videos> --output-json-path <path_to_save_filtered_json> --output-frames-dir <path_to_save_frames> --extract-frames
```

Exemple:
```
python generate_extract_dataset.py --set test --global-json-path ./{set}.json --sequence-list-path ./dataset_config/{set}.txt --distortion-dir ./distortion_type_ --videos-dir ./distorted_video/distorted_video --output-json-path ./dataset_config/{output}.json --output-frames-dir ./dataset_config/filtered_frames --extract-frames
```

📁 **Output**
A COCO-compatible annotation file containing:
* Only the selected sequences
* All associated distortions and severity levels
* Updated image paths following the convention:

```
{video_name}_{dist}_lvl{lvl}_{frame_name}.jpg
```

This allows you to customize your training or validation datasets without needing to regenerate or load the entire PVD4RCV dataset each time.

## 🗂️ Dataset Structure

The dataset is organized in a clear directory structure to facilitate access to original videos, distorted versions, and corresponding ground-truth data.
 addition to the video and depth data, **all annotations are provided in two complementary formats** to ensure compatibility with most computer vision frameworks:

- **COCO format**: JSON files following the COCO dataset structure, including bounding boxes, segmentation masks (if applicable), and category IDs consistent with the **COCO label indexing**.  
- **YOLO format**: Plain-text `.txt` files containing normalized bounding box coordinates and class indices following the **YOLO label convention**. Each video frame has its own corresponding `.txt` annotation file.

This dual-format annotation setup allows users to directly integrate PVD4RCV into common training pipelines such as **Detectron2**, **MMDetection**, or **Ultralytics YOLO** without additional preprocessing.


```
PVD4RCV/
│
├── distorted_video/ # 672 distorted videos grouped by type & severity
│ ├── Sequence1/
│ │ ├── Sequence1_DistortionType_DistorsionLevel.mp4
│ │ └── ...
│ ├── Sequence2/
│ ├── Sequence3/
│ └── ../
│
├── GroundTruth/ # Truth value directory (annotations)
│ ├── annotations/ # video sequence
│ │ ├── train.json # json annotations of the train set
│ │ ├── validation.json # json annotations of the validation set
│ │ ├── yolo/ # Contain yolo format annotations
│ │
│ │ │ ├── Sequence/ # Per-frame object annotations
│ │ │ │ ├── frame_000.txt
│ │ │ │ └── ...
│ │ │ ├── ...
│ │ │ 
│ │ ├── tracking/ # Per-frame object annotations
│ │ │ ├── Sequence.json/ # Tracking annotations by sequence
│ │ │ ├── ...
│ │ │ ├── yolo/ # Per-frame object annotations
│ │ │ │ ├── Sequence/ # Per-frame object annotations
│ │ │ │ │ ├── frame_000.txt
│ │ │ │ │ └── ...
│ │ │ │ ├── ...
│ │ ├── yolo_shakiness/ # Contain yolo format annotation for shakiness distortions
│ │ │ 
│ ├── depth/ # depth map annotations
│ │ ├── Sequence/ # Per-frame object annotations
│ │ │ ├── frame_000.png
│ │ │ └── ...
│ │ └── ...
│ │ 
```
---

### 📘 Description of the *GroundTruth* folder

The **GroundTruth/** directory contains all the reference data used for model evaluation and training:

- **BoundingBoxes/** → JSON files and txt files with per-frame bounding boxes and object IDs  
  *(format: frame, object_id, class, x_min, y_min, x_max, y_max)*  
- **Depth map** → Depth map of each sequences   

---

## 🔧 Main Applications

PVD4RCV can be used for:

* **Robust Object Detection**: evaluating detection under degraded conditions
* **Visual Tracking**: testing robustness of tracking algorithms
* **Distortion Classification**: training/testing distortion recognition models
* **Scene Understanding**: benchmarking scene analysis in complex environments
* **Depth Estimation**: evaluating monocular depth estimation with ground-truth maps

---

## 📊 Key Features

✅ Photo-realistic distortions based on physical models
✅ Multiple severity levels for each distortion type
✅ Large diversity of real-world scenarios
✅ Includes annotations and depth maps
✅ Suitable for benchmarking and training deep learning models

---


## 📊 Benchmark

Coming soon...

---

## 📥 Access and Download

👉 [Download Link] (insert official link here)

---

## 📜 Citation

If you use this dataset, please cite the associated paper:

```
@inproceedings{pvd4rcv2025,
  title={PVD4RCV: A Photo-realistic Multi-Distortion Video Dataset for Benchmarking and Developing Robust Computer Vision Models},
  booktitle={IEEE VCIP},
  year={2025}
}
```

---

## 👥 Authors & Contributions

* [List of article authors]
* Project presented at **IEEE VCIP 2025**

---

