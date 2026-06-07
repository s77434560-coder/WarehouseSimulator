#!/usr/bin/env python3
"""
Data loader for Warehouse Simulator exports
Converts JSON simulation data to NumPy arrays for ML training
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

def load_simulation_data(file_path):
    """Load JSON data exported from Godot simulation"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract arrays
    frames = np.array([d['frame'] for d in data])
    timestamps = np.array([d['timestamp'] for d in data])
    positions = np.array([d['position'] for d in data])
    rotations = np.array([d['rotation'] for d in data])
    velocities = np.array([d['velocity'] for d in data])
    raycast_hits = np.array([d['raycast_hit'] for d in data])
    is_moving = np.array([d['is_moving'] for d in data])
    
    return {
        'frames': frames,
        'timestamps': timestamps,
        'positions': positions,
        'rotations': rotations,
        'velocities': velocities,
        'raycast_hits': raycast_hits,
        'is_moving': is_moving,
        'raw_data': data
    }

def visualize_trajectory(data):
    """Plot robot trajectory"""
    positions = data['positions']
    
    plt.figure(figsize=(10, 8))
    plt.plot(positions[:, 0], positions[:, 2], 'b-', linewidth=2, label='Path')
    plt.scatter(positions[0, 0], positions[0, 2], c='green', s=100, label='Start', marker='o')
    plt.scatter(positions[-1, 0], positions[-1, 2], c='red', s=100, label='End', marker='s')
    
    # Color by velocity magnitude
    velocities = data['velocities']
    speeds = np.linalg.norm(velocities, axis=1)
    scatter = plt.scatter(positions[:, 0], positions[:, 2], c=speeds, cmap='viridis', 
                          alpha=0.6, s=20, label='Speed')
    plt.colorbar(scatter, label='Speed (m/s)')
    
    plt.xlabel('X Position')
    plt.ylabel('Z Position')
    plt.title('Robot Navigation Trajectory')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.savefig('trajectory_plot.png', dpi=150)
    plt.show()

def analyze_movement(data):
    """Print movement statistics"""
    velocities = data['velocities']
    speeds = np.linalg.norm(velocities, axis=1)
    raycast_hits = data['raycast_hits']
    
    print("\n" + "="*50)
    print("SIMULATION STATISTICS")
    print("="*50)
    print(f"Total frames: {len(data['frames'])}")
    print(f"Total time: {(data['timestamps'][-1] - data['timestamps'][0])/1000:.2f} seconds")
    print(f"Average speed: {np.mean(speeds):.2f} m/s")
    print(f"Max speed: {np.max(speeds):.2f} m/s")
    print(f"Total distance traveled: {np.sum(speeds * 0.0167):.2f} meters")
    print(f"Collision alerts: {np.sum(raycast_hits)}")
    print(f"Moving percentage: {np.mean(data['is_moving'])*100:.1f}%")
    
    # Position bounds
    positions = data['positions']
    print(f"\nX range: [{np.min(positions[:,0]):.2f}, {np.max(positions[:,0]):.2f}]")
    print(f"Z range: [{np.min(positions[:,2]):.2f}, {np.max(positions[:,2]):.2f}]")

def main():
    parser = argparse.ArgumentParser(description='Analyze simulation export data')
    parser.add_argument('--path', type=str, default='exports/', 
                        help='Path to JSON file or folder')
    args = parser.parse_args()
    
    # Find JSON file
    path = Path(args.path)
    if path.is_dir():
        json_files = list(path.glob("*.json"))
        if not json_files:
            print(f"No JSON files found in {path}")
            return
        json_path = json_files[0]
    else:
        json_path = path
    
    print(f"Loading: {json_path}")
    data = load_simulation_data(json_path)
    analyze_movement(data)
    visualize_trajectory(data)

if __name__ == "__main__":
    main()
