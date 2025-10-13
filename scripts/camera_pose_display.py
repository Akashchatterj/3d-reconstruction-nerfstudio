import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
from pathlib import Path

def load_transforms(transforms_path):
    """Load transforms.json file"""
    with open(transforms_path, 'r') as f:
        data = json.load(f)
    return data

def extract_camera_poses(transforms_data):
    """Extract camera positions and orientations from transforms"""
    positions = []
    orientations = []
   
    for frame in transforms_data['frames']:
        transform = np.array(frame['transform_matrix'])
       
        # Camera position is the last column (translation)
        position = transform[:3, 3]
        positions.append(position)
       
        # Camera orientation (forward direction) is -z axis
        forward = -transform[:3, 2]
        orientations.append(forward)
   
    return np.array(positions), np.array(orientations)

def visualize_camera_poses_3d(positions, orientations, title="Camera Poses - 3D View"):
    """Create 3D visualization of camera poses"""
    fig = plt.figure(figsize=(15, 10))
   
    # 3D perspective view
    ax1 = fig.add_subplot(121, projection='3d')
   
    # Plot camera positions
    ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                c='red', marker='o', s=100, label='Camera positions')
   
    # Plot camera orientations
    scale = 0.5
    for pos, orient in zip(positions, orientations):
        ax1.quiver(pos[0], pos[1], pos[2],
                  orient[0], orient[1], orient[2],
                  length=scale, color='blue', arrow_length_ratio=0.3)
   
    # Connect cameras with a line to show trajectory
    ax1.plot(positions[:, 0], positions[:, 1], positions[:, 2],
             'g--', alpha=0.5, label='Trajectory')
   
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3D Perspective View')
    ax1.legend()
    ax1.grid(True)
   
    # Top-down view (XY plane)
    ax2 = fig.add_subplot(122)
   
    ax2.scatter(positions[:, 0], positions[:, 1],
                c='red', marker='o', s=100, label='Camera positions')
   
    # Plot orientations in 2D
    for i, (pos, orient) in enumerate(zip(positions, orientations)):
        ax2.arrow(pos[0], pos[1],
                 orient[0]*scale, orient[1]*scale,
                 head_width=0.1, head_length=0.15,
                 fc='blue', ec='blue', alpha=0.7)
        ax2.text(pos[0], pos[1], str(i), fontsize=8)
   
    ax2.plot(positions[:, 0], positions[:, 1],
             'g--', alpha=0.5, label='Trajectory')
   
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Top-Down View (XY plane)')
    ax2.legend()
    ax2.grid(True)
    ax2.axis('equal')
   
    plt.suptitle(title)
    plt.tight_layout()
   
    return fig

def visualize_camera_poses_side_views(positions, orientations):
    """Create side view visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
   
    scale = 0.5
   
    # XZ view (side view)
    ax = axes[0, 0]
    ax.scatter(positions[:, 0], positions[:, 2], c='red', marker='o', s=100)
    for i, (pos, orient) in enumerate(zip(positions, orientations)):
        ax.arrow(pos[0], pos[2], orient[0]*scale, orient[2]*scale,
                head_width=0.1, head_length=0.15, fc='blue', ec='blue', alpha=0.7)
        ax.text(pos[0], pos[2], str(i), fontsize=8)
    ax.plot(positions[:, 0], positions[:, 2], 'g--', alpha=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_title('Side View (XZ plane)')
    ax.grid(True)
    ax.axis('equal')
   
    # YZ view (front view)
    ax = axes[0, 1]
    ax.scatter(positions[:, 1], positions[:, 2], c='red', marker='o', s=100)
    for i, (pos, orient) in enumerate(zip(positions, orientations)):
        ax.arrow(pos[1], pos[2], orient[1]*scale, orient[2]*scale,
                head_width=0.1, head_length=0.15, fc='blue', ec='blue', alpha=0.7)
        ax.text(pos[1], pos[2], str(i), fontsize=8)
    ax.plot(positions[:, 1], positions[:, 2], 'g--', alpha=0.5)
    ax.set_xlabel('Y')
    ax.set_ylabel('Z')
    ax.set_title('Front View (YZ plane)')
    ax.grid(True)
    ax.axis('equal')
   
    # Camera heights over trajectory
    ax = axes[1, 0]
    ax.plot(range(len(positions)), positions[:, 2], 'b-o', label='Height (Z)')
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('Z Position')
    ax.set_title('Camera Height over Trajectory')
    ax.grid(True)
    ax.legend()
   
    # Distance from origin
    ax = axes[1, 1]
    distances = np.linalg.norm(positions, axis=1)
    ax.plot(range(len(positions)), distances, 'g-o', label='Distance from origin')
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('Distance')
    ax.set_title('Camera Distance from Origin')
    ax.grid(True)
    ax.legend()
   
    plt.suptitle('Camera Poses - Multiple Views')
    plt.tight_layout()
   
    return fig

def print_camera_statistics(positions, transforms_data):
    """Print statistics about the camera poses"""
    print("\n" + "="*60)
    print("CAMERA POSE STATISTICS")
    print("="*60)
    print(f"Number of frames: {len(positions)}")
    print(f"\nImage dimensions: {transforms_data['w']} x {transforms_data['h']}")
    print(f"Camera model: {transforms_data.get('camera_model', 'Unknown')}")
    print(f"\nFocal length: fl_x={transforms_data.get('fl_x', 'N/A'):.2f}, fl_y={transforms_data.get('fl_y', 'N/A'):.2f}")
    print(f"Principal point: cx={transforms_data.get('cx', 'N/A'):.2f}, cy={transforms_data.get('cy', 'N/A'):.2f}")
   
    print(f"\n--- Position Statistics ---")
    print(f"X range: [{positions[:, 0].min():.3f}, {positions[:, 0].max():.3f}]")
    print(f"Y range: [{positions[:, 1].min():.3f}, {positions[:, 1].max():.3f}]")
    print(f"Z range: [{positions[:, 2].min():.3f}, {positions[:, 2].max():.3f}]")
   
    center = positions.mean(axis=0)
    print(f"\nScene center: [{center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f}]")
   
    distances = np.linalg.norm(positions - center, axis=1)
    print(f"Average distance from center: {distances.mean():.3f}")
    print(f"Max distance from center: {distances.max():.3f}")
   
    # Camera trajectory length
    if len(positions) > 1:
        trajectory_length = np.sum(np.linalg.norm(np.diff(positions, axis=0), axis=1))
        print(f"\nTotal trajectory length: {trajectory_length:.3f}")
   
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Visualize camera poses from transforms.json')
    parser.add_argument('--input_dir', type=str, required=True,
                        help='Directory containing transforms.json')
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Directory to save visualizations (optional)')
   
    args = parser.parse_args()
   
    # Load transforms
    transforms_path = Path(args.input_dir) / 'transforms.json'
    if not transforms_path.exists():
        print(f"Error: transforms.json not found in {args.input_dir}")
        return
   
    print(f"Loading transforms from: {transforms_path}")
    transforms_data = load_transforms(transforms_path)
   
    # Extract camera poses
    positions, orientations = extract_camera_poses(transforms_data)
   
    # Print statistics
    print_camera_statistics(positions, transforms_data)
   
    # Create visualizations
    print("Creating 3D visualization...")
    fig1 = visualize_camera_poses_3d(positions, orientations)
   
    print("Creating side view visualizations...")
    fig2 = visualize_camera_poses_side_views(positions, orientations)
   
    # Save figures if output directory specified
    if args.output_dir:
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
       
        fig1.savefig(output_path / 'camera_poses_3d.png', dpi=300, bbox_inches='tight')
        fig2.savefig(output_path / 'camera_poses_side_views.png', dpi=300, bbox_inches='tight')
        print(f"\nVisualizations saved to: {output_path}")
   
    plt.show()

if __name__ == '__main__':
    main()