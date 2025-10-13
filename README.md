# 3D Reconstruction from Video using Nerfstudio

A complete pipeline for 3D reconstruction from monocular video using Neural Radiance Fields (NeRF) with Nerfstudio's nerfacto method.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Pipeline Workflow](#pipeline-workflow)
- [Results](#results)
- [Challenges & Solutions](#challenges--solutions)
- [Project Structure](#project-structure)
- [References](#references)

## 🎯 Overview

This project demonstrates a complete 3D reconstruction pipeline that:
- Extracts frames from video input
- Estimates camera poses using COLMAP
- Trains a Neural Radiance Field using nerfacto
- Exports a high-quality 3D point cloud

**Key Technologies:** Nerfstudio, COLMAP, NeRF, Open3D, Weights & Biases

## 📦 Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- COLMAP installed
- FFmpeg for video processing

## 🚀 Installation

### 1. Install Nerfstudio

```bash
pip install nerfstudio
```

For detailed installation instructions, visit [Nerfstudio Documentation](https://docs.nerf.studio/quickstart/installation.html)

### 2. Install Additional Dependencies

```bash
pip install open3d wandb
```

### 3. Login to Weights & Biases

```bash
wandb login
```

## 🔄 Pipeline Workflow

### Task 1: Video Processing

Extract frames and estimate camera poses from your video:

```bash
ns-process-data video \
  --data YOUR_VIDEO.mp4 \
  --output-dir YOUR_OUTPUT_DIR \
  --num-frames-target 70
```

**Parameters:**
- `--data`: Path to input video file
- `--output-dir`: Directory for processed data
- `--num-frames-target`: Number of frames to extract (70 recommended)

**Output:** Extracted frames + COLMAP camera pose estimates

---

### Task 2: Camera Pose Visualization

Visualize the estimated camera trajectory:

```bash
python camera_pose_display.py --input_dir YOUR_OUTPUT_DIR
```

**Generates:**
- Perspective view of camera poses
- Top-down view of camera trajectory

These visualizations help assess the quality of pose estimation before training.

---

### Task 3: NeRF Training with Nerfacto

Train the Neural Radiance Field model:

```bash
ns-train nerfacto \
  --viewer.quit-on-train-completion True \
  --pipeline.model.predict-normals True \
  --vis "viewer+wandb" \
  --data YOUR_OUTPUT_DIR \
  --output-dir YOUR_TRAIN_OUTPUT_DIR
```

**Key Parameters:**
- `--viewer.quit-on-train-completion`: Auto-close viewer after training
- `--pipeline.model.predict-normals`: Enable normal prediction for better geometry
- `--vis "viewer+wandb"`: Enable both viewer and W&B logging

**Training Process:**
1. Opens viewer at `http://localhost:7007`
2. Trains for ~30k iterations (default)
3. Logs metrics to Weights & Biases
4. Saves model checkpoints

---

### Task 4: Bounding Box Cropping (Optional)

While training, optimize the export region:

1. Open viewer: `http://localhost:7007`
2. Click **Crop** tool in the viewer
3. Adjust bounding box around object of interest
4. Note the OBB parameters for export

---

### Task 5: Point Cloud Export

Export the trained NeRF as a point cloud:

```bash
ns-export pointcloud \
  --load-config /PATH/TO/YOUR/config.yml \
  --output-dir /PATH/TO/YOUR/exports \
  --num-points 1000000 \
  --remove-outliers True \
  --normal-method open3d \
  --save-world-frame False \
  --obb_center 0.0 0.0 0.0 \
  --obb_rotation 0.0 0.0 0.0 \
  --obb_scale 1.0 1.0 1.0
```

**Parameters:**
- `--num-points`: Number of points (1M recommended)
- `--remove-outliers`: Clean noisy points
- `--normal-method`: Use Open3D for normal estimation
- `--obb_*`: Bounding box parameters from viewer

**Output:** High-quality `.ply` point cloud file

## 📊 Results

### Camera Pose Estimation

| Perspective View | Top View |
|:----------------:|:--------:|
| ![Perspective](outputs/visualizations/camera_poses_3d.png) | ![Top View](outputs/visualizations/camera_poses_side_views.png) |

**Assessment:** The camera poses show [smooth/erratic] trajectory with [good/poor] coverage of the scene. [Add your specific observations]

### NeRF Reconstruction

![NeRF Render](outputs/nerf_render.png)

**Training Metrics:**
- Training Time: XX minutes
- Final PSNR: XX.XX dB
- GPU: [Your GPU Model]

**Quality Assessment:** The reconstruction captures [describe quality - fine details, geometry accuracy, texture fidelity, etc.]

### Point Cloud Export

![Point Cloud](outputs/pointcloud.png)

**Specifications:**
- Points: 1,000,000
- Format: PLY with normals
- File Size: XX MB

[Download Point Cloud](outputs/export.ply)

## 🔧 Challenges & Solutions

### Challenge 1: [Camera Pose Estimation Quality]

**Issue:** [Describe any issues with pose estimation - e.g., "Initial COLMAP reconstruction failed due to insufficient feature matches"]

**Solution:** [How you solved it - e.g., "Increased num-frames-target to 100 and ensured better lighting conditions in the video"]

---

### Challenge 2: [Training Time/GPU Memory]

**Issue:** [e.g., "Training was slow on limited GPU memory"]

**Solution:** [e.g., "Reduced batch size and used mixed precision training"]

---

### Challenge 3: [Point Cloud Quality]

**Issue:** [e.g., "Initial export had many outliers"]

**Solution:** [e.g., "Enabled outlier removal and used tight bounding box cropping"]

---

### General Observations

- **Setup Complexity:** Nerfstudio installation was straightforward but required CUDA toolkit setup
- **COLMAP Dependency:** Pose estimation quality heavily depends on video quality and camera movement
- **Training Duration:** Approximately XX minutes on [GPU model]
- **Memory Usage:** Peak GPU memory: XX GB

## 📁 Project Structure

```
├── README.md
├── camera_pose_display.py      # Pose visualization script
├── data/
│   └── YOUR_VIDEO.mp4          # Input video
├── processed_data/             # Processed frames & poses (Task 1)
│   ├── images/
│   ├── colmap/
│   └── transforms.json
├── outputs/                    # Training outputs (Task 3)
│   ├── nerfacto/
│   │   ├── config.yml
│   │   └── nerfstudio_models/
│   ├── pose_perspective.png    # Pose visualizations (Task 2)
│   └── pose_top.png
├── exports/                    # Point cloud exports (Task 5)
│   └── export.ply
└── report.md                   # Detailed findings
```

## 🎓 Reflections

### What Worked Well
- [Add your observations about what went smoothly]
- The nerfacto pipeline produced high-quality results
- Pose estimation was robust with proper video input

### Areas for Improvement
- [Add suggestions for future improvements]
- Could experiment with different NeRF variants (instant-ngp, etc.)
- Fine-tuning bounding box parameters could improve point cloud quality

### Key Learnings
- [Your key takeaways from the assignment]
- Understanding the importance of camera pose quality for NeRF training
- Trade-offs between point cloud density and file size

## 📚 References

- [Nerfstudio Documentation](https://docs.nerf.studio/)
- [NeRF: Representing Scenes as Neural Radiance Fields](https://www.matthewtancik.com/nerf)
- [Instant Neural Graphics Primitives](https://nvlabs.github.io/instant-ngp/)
- [COLMAP Structure-from-Motion](https://colmap.github.io/)

---

**Author:** [Your Name]  
**Course:** [Course Name/Code]  
**Date:** [Submission Date]  

## 🔗 Quick Links

- [Live Demo](#) (if available)
- [Weights & Biases Dashboard](#) (add your W&B link)
- [Download Full Results](#) (if hosting elsewhere)
