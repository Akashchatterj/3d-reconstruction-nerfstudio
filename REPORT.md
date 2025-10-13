# 3D Reconstruction Assignment - Technical Report

## Executive Summary

This report documents the complete process of 3D reconstruction from monocular video using Nerfstudio's nerfacto pipeline. The project successfully demonstrates the entire workflow from video processing to point cloud export, with detailed analysis of challenges encountered and solutions implemented.

---

## 1. Introduction

### 1.1 Objective
The primary objective was to reconstruct a 3D scene from a monocular video using Neural Radiance Fields (NeRF) technology, specifically using the Nerfstudio framework with the nerfacto method.

### 1.2 Methodology Overview
The reconstruction pipeline consists of five main stages:
1. Video processing and frame extraction
2. Camera pose estimation using COLMAP
3. NeRF model training with nerfacto
4. Bounding box optimization
5. Point cloud export

---

## 2. Setup and Installation

### 2.1 Environment Configuration

**System Specifications:**
- Operating System: Linux Ubentu
- GPU: RTX 4080 Super 
- CUDA Version: [Version]
- Python Version: [Version]

### 2.2 Installation Process

**Challenges Encountered:**
- colmap_to_json() TypeError.
- COLMAP installation required additional dependencies and showed compatibility issues on Windows OS.
- Encountered CUDA and PyTorch version mismatches, causing GPU initialization failures.
- Installation was overall more error-prone on Windows due to missing environment variables and path issues.

**Solutions Applied:**
- Removed deprecated argument camera_model="OPENCV" from the function call.
- Switched to a Linux environment, where dependencies installed smoothly and GPU drivers were configured automatically.
- Reinstalled CUDA and PyTorch with compatible versions as per Nerfstudio documentation.
- Verified installation using test commands (ns-train --help and ns-process-data --help) to ensure the setup was working correctly before running experiments.

**Time Required:** Approximately 3 hours for complete setup

---

## 3. Task 1: Video Processing

### 3.1 Input Video Characteristics

| Property | Value |
|----------|-------|
| Resolution | 1080x1920 |
| Duration |  19.99 seconds |
| Frame Rate |  29.97 fps |
| Format | MOV |
| Camera Movement | Circular |

### 3.2 Processing Configuration

```bash
ns-process-data video \
  --data YOUR_VIDEO.mp4 \
  --output-dir YOUR_OUTPUT_DIR \
  --num-frames-target 70
```

**Parameters Selected:**
- **num-frames-target: 120** - Chosen because to provide dense coverage of the 360° camera trajectory (3° spacing between frames) while maintaining computational efficiency. This ensures sufficient overlap for COLMAP feature matching and adequate training data for NeRF convergence.
- Processing method: COLMAP (default)

### 3.3 Results

**Output Generated:**
- Total frames extracted: 120
- COLMAP sparse reconstruction: Success
- Transform file generated: Yes

**Observations:**
- Frame quality: Excellent
- Feature detection: Initially, COLMAP detected and matched features in only 2 frames due to limited camera motion and low texture in the video. After downgrading to COLMAP 3.8 and using the Sequential Matcher, feature detection improved, matching all frames successfully for accurate pose estimation.
- Processing time: 60 minutes

**Challenges:**
- Very few feature matches were detected — only 2 frames matched successfully due to limited camera movement and low texture in the video.
- The short video length and repetitive background further reduced distinct keypoints for COLMAP to track.

**Solutions:**
- Downgraded to COLMAP 3.8, which provided more stable and effective feature matching.
  
---

## 4. Task 2: Pose Estimation Analysis

### 4.1 Visualization Results

The camera pose visualization script generated two critical views:

#### 4.1.1 Perspective View Analysis

![Perspective View](outputs/visualizations/camera_poses_side_views.png)

**Observations:**
- Camera trajectory: Shows a clean, elliptical path around the object.
- Coverage: Complete 360° coverage with cameras evenly distributed around the entire circumference of the scene.
- Pose distribution: Even - cameras are uniformly spaced along the trajectory with consistent angular separation of approximately 3° between frames.

**Quality Indicators:**
-  Smooth elliptical trajectory without erratic jumps or outliers.
-  Complete 360° loop with start and end positions aligned.
-  Consistent camera-to-object distance (only 7% variance).
-  No pose estimation failures - all 120 frames successfully registered.
-  All camera orientations pointing toward the scene center.
-  Slight elliptical distortion instead of perfect circle (minor impact, not a real problem).

#### 4.1.2 Top View Analysis

![Top View](outputs/visualizations/camera_poses_3d.png)

**Observations:**
- Spatial distribution: Consistent circular motion in the XY plane with uniform angular spacing of approximately 3° between frames.
- Scene coverage: 100% - complete circular coverage with no gaps or blind spots, ensuring all sides of the object are captured from multiple angles.
- Potential blind spots: None identified - the complete 360° trajectory ensures all viewing angles are covered.

### 4.2 Pose Estimation Quality Assessment

**Metrics Considered:**
1. **Reconstruction Coverage:** 100% of scene well-covered with complete 360° camera trajectory providing comprehensive viewpoint sampling.
2. **Pose Accuracy:** Excellent having smooth trajectory with no outliers, consistent camera distances ranging from 3.58 to 3.87 units (only 7% variance), and all orientations properly aligned toward the scene center.
3. **Camera Distribution:** Even with 120 frames uniformly distributed along elliptical path with approximately 3° angular spacing between consecutive frames.

**Overall Assessment:** 
The camera poses demonstrate all key indicators of successful reconstruction including: (1) smooth elliptical trajectory without discontinuities, (2) 100% COLMAP registration success for all 120 frames, (3) correct orientation alignment with all cameras facing the scene center, (4) outstanding distance consistency with only 7% variance, (5) natural smooth height variation pattern, and (6) complete 360° angular coverage eliminating blind spots. This level of quality indicates excellent video capture technique and successful feature matching.

**Impact on NeRF Training:**
- High-quality reconstruction expected with predicted PSNR values exceeding 28 dB, potentially reaching 30+ dB due to the excellent pose quality and complete coverage.
- Fast and stable convergence anticipated due to well-distributed camera poses enabling smooth gradient flow during training, with minimal risk of getting stuck in poor local minima.

---

## 5. Task 3: NeRF Reconstruction

### 5.1 Training Configuration

```bash
ns-train nerfacto \
  --viewer.quit-on-train-completion True \
  --pipeline.model.predict-normals True \
  --vis "viewer+wandb" \
  --data YOUR_OUTPUT_DIR \
  --output-dir YOUR_TRAIN_OUTPUT_DIR
```

**Key Parameters:**
- **Model:** nerfacto (Nerfstudio's generalist method)
- **Normal Prediction:** Enabled (for better geometry)
- **Visualization:** Viewer + W&B logging
- **Training Iterations:** 30,000 

### 5.2 Training Process

**Timeline:**
- Start Time: [Timestamp]
- End Time: [Timestamp]
- Total Duration: 15 minutes

**Hardware Performance:**
- GPU Utilization: 100%
- Peak Memory Usage:  12.5GB
- Temperature: 60 °c

### 5.3 Training Metrics

| Iteration | PSNR (dB) | LPIPS | SSIM | Training Loss |
|-----------|-----------|-------|------|---------------|
| 1,000     | 24.5      | 0.18  | 0.730| 0.020         |
| 5,000     | 29.5      | 0.15  | 0.735| 0.012         |
| 10,000    | 31.5      | 0.13  | 0.740| 0.010         |
| 20,000    | 32.5      | 0.12  | 0.745| 0.009         |
| 30,000    | 33.0      | 0.12  | 0.750| 0.009         |

**Convergence Analysis:**
- Fast initial convergence (most improvement in first 5k iterations).
- Stable training without sudden jumps or instabilities.
- High final PSNR (33 dB) indicates excellent quality.
- Low perceptual loss (LPIPS 0.12) means realistic appearance.

### 5.4 Reconstruction Quality

**Visual Quality Assessment:**

![NeRF Rendering](outputs/visualizations/nerf_render.png)
🎬 [Click to Watch the NeRF Rendering Video](https://raw.githubusercontent.com/Akashchatterj/3d-reconstruction-nerfstudio/main/outputs/visualizations/nerf_render_video.mp4)


**Strengths:**
-  The cylindrical corn structure is precisely reconstructed with complete surface coverage and no holes or missing regions.
-  Golden-yellow corn kernels display natural color variation and authentic material appearance with proper matte finish.
-  Proper shading on corn surface with realistic shadow cast on the platform base.
-  Blue circular base, ArUco markers, and multi-layered structure all accurately captured with sharp edges.

**Weaknesses:**
- Ground plane and distant areas show intentional blur, which is expected NeRF behavior that prioritizes foreground object quality.
- Very subtle softening on extreme fine details (individual kernel ridges), though overall kernel structure remains clear.

**Comparison to Expectations:**
The reconstruction demonstrates photorealistic quality suitable for high-quality visualization, analysis, and potential downstream applications.Appropriate frame count - 120 frames provided sufficient viewpoint sampling density for fine detail capture. Also Full 30,000 iterations allowed complete convergence without premature stopping.

### 5.5 Challenges During Training

#### Challenge 1: [Specific Issue]
**Description:** [Detailed explanation]
**Impact:** [How it affected results]
**Resolution:** [Steps taken to resolve]

#### Challenge 2: [Specific Issue]
**Description:** [Detailed explanation]
**Impact:** [How it affected results]
**Resolution:** [Steps taken to resolve]

---

## 6. Task 4: Bounding Box Optimization

### 6.1 Cropping Strategy

**Approach:**
- Opened viewer at http://localhost:7007
- Analyzed full scene reconstruction
- Identified object of interest boundaries

**Bounding Box Parameters:**
```
OBB Center: [x, y, z]
OBB Rotation: [rx, ry, rz]
OBB Scale: [sx, sy, sz]
```

**Rationale:**
[Explain why these specific parameters were chosen]

### 6.2 Impact on Export

**Benefits of Cropping:**
- Reduced point cloud size by [X%]
- Focused on region of interest
- Eliminated background noise

---

## 7. Task 5: Point Cloud Export

### 7.1 Export Configuration

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

### 7.2 Point Cloud Specifications

| Property | Value |
|----------|-------|
| Total Points | 1,000,000 |
| File Format | PLY (binary) |
| File Size | 27.5 MB |
| Contains Normals | Yes |
| Contains Colors | Yes |

### 7.3 Quality Analysis

![Point Cloud Visualization](outputs/pointcloud.png)

**Geometric Accuracy:**
- [Assessment of 3D shape fidelity]
- [Comparison to original object if possible]

**Point Density:**
- [Uniform/Variable across surface]
- [Adequate for representing details]

**Normal Quality:**
- [Assessment of normal vectors]
- [Impact on downstream rendering]

**Outlier Removal Effectiveness:**
- [How well it cleaned the data]
- [Any remaining noise]

---


## 9. Lessons Learned

### 9.1 Technical Insights

1. **Camera Pose Quality is Critical**
   - [Specific observations about pose-quality relationship]
   
2. **Video Characteristics Matter**
   - [What you learned about input video requirements]

3. **Training Hyperparameters**
   - [Insights about parameter tuning]

### 9.2 Workflow Optimization

**Best Practices Identified:**
- [List effective approaches you discovered]
- [Workflow improvements]

**Pitfalls to Avoid:**
- [Common mistakes and how to prevent them]

---

## 10. Future Improvements

### 10.1 Short-term Enhancements
1. [Specific improvement #1]
2. [Specific improvement #2]
3. [Specific improvement #3]

### 10.2 Advanced Explorations
- Experiment with different NeRF architectures
- Implement custom loss functions
- Explore mesh extraction methods
- [Other advanced topics]

---

## 11. Conclusion

### 11.1 Project Summary

This project successfully demonstrated the complete pipeline for 3D reconstruction from monocular video using Nerfstudio. The key achievements include:

- ✓ [Achievement 1]
- ✓ [Achievement 2]
- ✓ [Achievement 3]

### 11.2 Overall Assessment

**Success Rate:** [X/5 tasks completed successfully]

**Quality Rating:** [Your overall quality assessment]

**Time Investment:** [Total hours spent]

### 11.3 Final Thoughts

[Concluding reflections on the assignment, what you learned, and the value of NeRF technology]

---

## 12. Appendices

### Appendix A: Command Reference
[Quick reference for all commands used]

### Appendix B: Error Log
[Any errors encountered and solutions]

### Appendix C: Resource Links
- [Useful documentation links]
- [Tutorial references]
- [Community resources]

---

**Report Prepared By:** [Your Name]  
**Date:** [Submission Date]  
**Assignment:** 3D Reconstruction with Nerfstudio  
**Total Pages:** [Auto-count]
