# OIIS - Fundamentals of Image and Signal Processing

This directory contains laboratory works for the course "Fundamentals of Image and Signal Processing" (Основы обработки изображений и сигналов).

## Directory Structure

- `1.py` - Implementation of Fast Fourier Transform (FFT) with comparison between manual and NumPy implementations, including spectrum and time-domain signal visualization.

- `2/` - Laboratory work on image filtering using PIL/Pillow:
  - `2.py` - Script applying various filters (blur, contour, sharpen, grayscale, edge enhancement) to images
  - Supporting image files (`1.png`, `2.png`)

- `3/` - Laboratory work on brightness adjustment of images:
  - `3.py` - Script for brightness alignment between two images using OpenCV
  - Reference images (`1.jpg`, `2.jpg`, `3.jpg`, `4.jpg`)

- `4/` - Laboratory work on image segmentation:
  - `4.py` - Script implementing edge-based (Canny) and region-based (Watershed) segmentation methods
  - Source image (`1.png`)

- `5/` - Stereo image processing materials:
  - Left/right stereo image pairs
  - Anaglyph images
  - `5.py` - Processing script (content to be examined)
  - Report in ODT format

- `6/` - Materials possibly related to red-black trees and mapping:
  - `6.py` - Main script
  - Visualization files (`map.jpg`, `rb.png`, `rbt.png`)
  - Template images

## Documentation

- `Отчёт ОИИС 1.docx` - Report for laboratory work 1 (in Russian)
- Additional reports in other directories (`3/`, `4/`, `5/`) in DOCX and ODT formats

## Requirements

Python packages required:
- numpy
- matplotlib
- pillow (PIL)
- opencv-python
- scipy (may be needed for some operations)

## Notes

All scripts were developed for educational purposes and demonstrate fundamental algorithms in image and signal processing.
File paths in scripts are set to absolute paths referencing the original development environment and may require modification for use in other systems.