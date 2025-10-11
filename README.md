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

### 🌍 Scenarios included

* Road traffic
* Parking lots
* Stadiums and crowds
* Airports
* Shopping malls
* Urban streets and train stations
* Sea navigation

---

## 🗂️ Dataset Structure

The dataset is organized in a clear directory structure to facilitate access to original videos, distorted versions, and corresponding ground-truth data.

```
PVD4RCV/
│
├── Original/ # 24 pristine reference videos (10s each)
│ ├── video_001.mp4
│ ├── video_002.mp4
│ └── ...
│
├── Distorted/ # 672 distorted videos grouped by type & severity
│ ├── MotionBlur/
│ │ ├── Level1/
│ │ │ ├── video_001_lvl1.mp4
│ │ │ └── ...
│ │ ├── Level2/
│ │ └── ...
│ ├── DefocusBlur/
│ ├── Compression/
│ ├── Noise/
│ ├── Haze/
│ └── Rain/
│
├── DepthMaps/ # Corresponding depth maps for each sequence
│ ├── video_001_depth/
│ │ ├── frame_0001.png
│ │ └── ...
│ └── ...
│
└── GroundTruth/ # Truth value directory (annotations)
├── BoundingBoxes/ # Per-frame object annotations
│ ├── video_001.json
│ ├── video_002.json
│ └── ...
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

