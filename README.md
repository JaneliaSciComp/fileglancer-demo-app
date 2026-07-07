# Fileglancer Demo App

A simple demo app for testing [Fileglancer](https://github.com/JaneliaSciComp/fileglancer) job submission. It sleeps for a configurable duration and prints a message repeatedly. It also includes a conda-based entry point that renders the Mandelbrot set with NumPy.

## Prerequisites

- [Pixi](https://pixi.sh)
- [Miniforge](https://github.com/conda-forge/miniforge) (for the Mandelbrot demo)

## Usage

```bash
pixi run demo --message "Hello!" --sleep_seconds 2 --repeat 3 --verbose
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--sleep_seconds` | integer | 5 | Seconds to sleep between messages (0-300) |
| `--message` | string | "Hello from Fileglancer!" | Message to print |
| `--repeat` | integer | 3 | Number of times to repeat (1-100) |
| `--output_dir` | directory | | Directory to write a summary file (optional) |
| `--verbose` | flag | false | Show sleep countdown |
| `--log_level` | enum | INFO | Set the logging verbosity level. Options: DEBUG, INFO, WARNING, ERROR |

## Mandelbrot Demo (Conda)

The `mandelbrot` entry point renders the Mandelbrot set as ASCII art using NumPy. It runs inside a conda environment, which makes it a good end-to-end test of Fileglancer's `conda_env` support: the job log prints the Python executable and NumPy version so you can verify the environment was activated.

### Creating the environment

The environment is defined in `environment.yml`. Create it once on the system where jobs will run:

```bash
conda env create -f environment.yml
```

This creates a named environment called `fileglancer-demo` containing Python 3.12 and NumPy. Fileglancer activates it automatically when running the entry point (`conda_env: fileglancer-demo` in `runnables.yaml`).

### Running locally

```bash
conda run -n fileglancer-demo python mandelbrot.py --width 120 --height 40
```

Try zooming into an interesting region:

```bash
conda run -n fileglancer-demo python mandelbrot.py --center_x -0.7453 --center_y 0.1127 --zoom 200 --iterations 500
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--width` | integer | 120 | Width of the rendering in characters (20-500) |
| `--height` | integer | 40 | Height of the rendering in characters (10-200) |
| `--zoom` | number | 1.0 | Zoom factor into the view center |
| `--center_x` | number | -0.75 | Real coordinate of the view center |
| `--center_y` | number | 0.0 | Imaginary coordinate of the view center |
| `--iterations` | integer | 80 | Maximum iterations per pixel |
| `--output_dir` | directory | | Directory to write the rendering as a text file (optional) |

## Fileglancer Integration

This repo contains a `runnables.yaml` manifest. To use it in Fileglancer, add the GitHub repo URL on the Apps page.
