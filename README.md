# PVD4RCV Dataset

*A Photo-realistic Multi-Distortion Video Dataset for Benchmarking and Developing Robust Computer Vision Models*

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

