"""
surface_analysis.py

Analysis and output routines for the KMC surface growth simulation:
- saving results to JSON (one file per scenario)
- plotting mean height and roughness vs time
- plotting final surface-height profiles
- comparison plots across scenarios
"""

import json
import numpy as np
import matplotlib.pyplot as plt


def save_scenario_json(filepath, name, description, parameters, time_series, final_state):
    """Writes one scenario's results to a JSON file, following the
    format required by the problem sheet."""
    data = {
        "scenario": {
            "name": name,
            "description": description,
        },
        "parameters": parameters,
        "time_series": time_series,
        "final_state": final_state,
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def plot_mean_height(scenarios, filepath, title):
    """scenarios: list of (label, time_series) tuples."""
    plt.figure(figsize=(7, 5))
    for label, ts in scenarios:
        t = [p["time"] for p in ts]
        h = [p["mean_height"] for p in ts]
        plt.plot(t, h, label=label)
    plt.xlabel("Time  [1/rd]")
    plt.ylabel("Mean surface height  h(t)  [lattice units]")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()


def plot_roughness(scenarios, filepath, title):
    plt.figure(figsize=(7, 5))
    for label, ts in scenarios:
        t = [p["time"] for p in ts]
        w = [p["surface_roughness"] for p in ts]
        plt.plot(t, w, label=label)
    plt.xlabel("Time  [1/rd]")
    plt.ylabel("Surface roughness  W(t)  [lattice units]")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()


def plot_final_profiles(scenarios, filepath, title):
    """scenarios: list of (label, heights) tuples."""
    plt.figure(figsize=(7, 5))
    for label, heights in scenarios:
        x = np.arange(len(heights))
        plt.step(x, heights, where="mid", label=label)
    plt.xlabel("Lattice site  i")
    plt.ylabel("Height  h_i  [lattice units]")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
