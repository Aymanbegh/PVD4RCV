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

🗂️ Annotation files (bounding boxes, object classes, and distortion metadata)

You can download the full dataset package from the official link:
👉 Download PVD4RCV Dataset

## 🧰 Step 1 — Extract video frames

Once the dataset is downloaded and extracted locally, run the provided Python script to extract frames from each video sequence and store them in structured folders.

Each frame will be automatically renamed following this convention: **{video_name}_{dist}_lvl{lvl}_{original_frame_name}**

Example:

```
traffic_rain_lvl2_frame_00045.jpg
airport_blur_lvl4_frame_00012.jpg
```

This ensures clear identification of the scene, distortion type, and severity level for every frame.

Run the script from the project root:

```
python extract_frames.py --input-dir ./PVD4RCV/Distorted --output-dir ./PVD4RCV/Frames
```

**What this script does:**
* Iterates through all distorted video sequences
* Extracts individual frames using OpenCV (cv2.VideoCapture)
* Saves them with the naming pattern above
* Preserves scene and distortion metadata for traceability

**Requirements:**
* Python ≥ 3.8
* Required libraries: opencv-python, tqdm, os, argparse
(install via pip install -r requirements.txt if needed)


## 🗂️ Dataset Structure

The dataset is organized in a clear directory structure to facilitate access to original videos, distorted versions, and corresponding ground-truth data.
 addition to the video and depth data, **all annotations are provided in two complementary formats** to ensure compatibility with most computer vision frameworks:

- **COCO format**: JSON files following the COCO dataset structure, including bounding boxes, segmentation masks (if applicable), and category IDs consistent with the **COCO label indexing**.  
- **YOLO format**: Plain-text `.txt` files containing normalized bounding box coordinates and class indices following the **YOLO label convention**. Each video frame has its own corresponding `.txt` annotation file.

This dual-format annotation setup allows users to directly integrate PVD4RCV into common training pipelines such as **Detectron2**, **MMDetection**, or **Ultralytics YOLO** without additional preprocessing.


```
PVD4RCV/
│
├── Distorted/ # 672 distorted videos grouped by type & severity
│ ├── Sequence1/
│ │ ├── Sequence1_DistortionType_DistorsionLevel.mp4
│ │ └── ...
│ ├── Sequence2/
│ ├── Sequence3/
│ └── ../
│
├── GroundTruth/ # Truth value directory (annotations)
├── Sequence1/ # video sequence
│ ├── BoundingBoxes/ # Per-frame object annotations
│ │ ├── Sequence1.json
│ │ ├── txt/ # Per-frame object annotations
│ │ │ ├── frame_000.txt
│ │ │ └── ...
│ ├── depth/ # depth map annotations
│ │ ├── frame_000.png
│ │ └── ...
│
├── ObjectClasses.txt # List of all object categories
├── SceneMetadata.csv # Scene-level metadata (lighting, motion, etc.)
└── DistortionLabels.csv # Ground-truth mapping: video ↔ distortion type/level
```
---

### 📘 Description of the *GroundTruth* folder

The **GroundTruth/** directory contains all the reference data used for model evaluation and training:

- **BoundingBoxes/** → JSON files with per-frame bounding boxes and object IDs  
  *(format: frame, object_id, class, x_min, y_min, x_max, y_max)*  
- **ObjectClasses.txt** → List of object classes present in the dataset (e.g. car, person, ball, etc.)  
- **SceneMetadata.csv** → Global scene information such as lighting, motion dynamics, and environment type.  
- **DistortionLabels.csv** → Mapping file linking each distorted video to its original reference and distortion parameters (type, severity, frame count).  

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

