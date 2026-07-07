"""Fileglancer Demo App - render the Mandelbrot set as ASCII art using NumPy.

This entry point runs inside a conda environment (see environment.yml), so it
also serves as a test that Fileglancer's conda_env activation works: it prints
the Python executable and NumPy version before rendering.
"""

import argparse
import os
import sys
from datetime import datetime

import numpy as np

# Darker characters = more iterations before escape (deeper in the set)
CHARSET = " .:-=+*#%@"


def render(width, height, center_x, center_y, zoom, iterations):
    """Compute an ASCII rendering of the Mandelbrot set."""
    # Terminal characters are roughly twice as tall as they are wide, so the
    # imaginary axis spans half the range of the real axis per character.
    x_span = 3.5 / zoom
    y_span = x_span * (height / width) * 2.0

    x = np.linspace(center_x - x_span / 2, center_x + x_span / 2, width)
    y = np.linspace(center_y - y_span / 2, center_y + y_span / 2, height)
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    z = np.zeros_like(c)
    escape = np.full(c.shape, iterations, dtype=int)
    still_bounded = np.ones(c.shape, dtype=bool)

    for i in range(iterations):
        z[still_bounded] = z[still_bounded] ** 2 + c[still_bounded]
        escaped = still_bounded & (np.abs(z) > 2.0)
        escape[escaped] = i
        still_bounded &= ~escaped

    # Map escape iteration counts to characters
    levels = (escape / iterations * (len(CHARSET) - 1)).astype(int)
    return "\n".join("".join(CHARSET[v] for v in row) for row in levels)


def main():
    parser = argparse.ArgumentParser(description="ASCII Mandelbrot renderer")
    parser.add_argument(
        "--width", type=int, default=120,
        help="Width of the rendering in characters",
    )
    parser.add_argument(
        "--height", type=int, default=40,
        help="Height of the rendering in characters",
    )
    parser.add_argument(
        "--zoom", type=float, default=1.0,
        help="Zoom factor (try 50 at the default center for detail)",
    )
    parser.add_argument(
        "--center_x", type=float, default=-0.75,
        help="Real coordinate of the view center",
    )
    parser.add_argument(
        "--center_y", type=float, default=0.0,
        help="Imaginary coordinate of the view center",
    )
    parser.add_argument(
        "--iterations", type=int, default=80,
        help="Maximum iterations per pixel",
    )
    parser.add_argument(
        "--output_dir", type=str, default="",
        help="Directory to write the rendering as a text file (optional)",
    )
    args = parser.parse_args()

    print("=== Fileglancer Mandelbrot Demo ===")
    print(f"Python executable: {sys.executable}")
    print(f"NumPy version: {np.__version__}")
    print(f"View: center=({args.center_x}, {args.center_y}) "
          f"zoom={args.zoom} iterations={args.iterations}")
    print("===================================")
    print()

    art = render(args.width, args.height, args.center_x, args.center_y,
                 args.zoom, args.iterations)
    print(art)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, "mandelbrot.txt")
        print()
        print(f"Writing output to {output_file}")
        with open(output_file, "w") as f:
            f.write(f"Rendered at {datetime.now()} with NumPy {np.__version__}\n")
            f.write(f"center=({args.center_x}, {args.center_y}) "
                    f"zoom={args.zoom} iterations={args.iterations}\n\n")
            f.write(art + "\n")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
