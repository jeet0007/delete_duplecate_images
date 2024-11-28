# Duplicate Image Finder and Cleaner

A Python tool to find and remove duplicate images from your folders. It supports both command-line and graphical user interfaces, built with a clean MVC architecture.

## Features

- Find duplicate images using perceptual hashing
- Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, TIFF, HEIC, HEIF)
- Modern GUI with component-based architecture
- Command-line interface for automation
- Preview duplicates before deletion
- Safe deletion with confirmation
- Comprehensive error handling
- Progress tracking with detailed feedback

## System Requirements

### Supported Platforms
- macOS (10.15+)
- Linux (Ubuntu 20.04+)
- Windows 10/11

### Prerequisites
- Python 3.9+
- pip
- Homebrew (macOS)
- libheif
- cairo graphics library

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/delete_duplicate_images.git
cd delete_duplicate_images
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 3. Install System Dependencies

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system libraries
brew install libheif cairo pkg-config
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y libheif-dev libcairo2-dev pkg-config
```

#### Windows
- Download and install [HEIF Image Extensions](https://apps.microsoft.com/detail/9PMMBL1CTSB3) from Microsoft Store
- Install [Cairo Graphics Library](https://www.cairographics.org/download/)

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode
```bash
python -m src --gui
```

### Command Line Mode
```bash
python -m src --folder /path/to/folder
```

### Options
- `--gui`: Launch the graphical user interface
- `--folder`: Specify the folder path to scan (required in CLI mode)

## HEIC/HEIF Support

### What are HEIC/HEIF Files?
HEIC (High Efficiency Image Container) is a modern image format used by Apple devices, offering superior compression compared to JPEG.

### Compatibility
- Fully supported on macOS
- Requires additional libraries on Linux and Windows
- Processed using `pillow-heif` library

### Troubleshooting HEIC Support
- Ensure `libheif` is installed
- Verify `pillow-heif` is correctly installed
- Check system library paths
- Update to the latest version of the application

## Performance and Limitations

- Large folders may take longer to process
- Memory usage scales with number of images
- Recommended: Process folders with less than 10,000 images at a time

## Architecture

The application follows the Model-View-Controller (MVC) pattern:
- **Models**: Core business logic for image processing and duplicate detection
- **Views**: Component-based GUI with modular design
- **Controllers**: Coordination between models and views, handling user interactions

## Components

1. **Image Finder (Model)**
   - Handles image processing and hash computation
   - Manages duplicate detection logic
   - Provides progress tracking
   - Handles errors gracefully

2. **GUI View**
   - Folder selection component
   - Action buttons for scan/delete
   - Results display with thumbnails
   - Progress visualization
   - Error reporting

3. **Controller**
   - Manages user interactions
   - Coordinates between model and view
   - Handles background processing
   - Manages state and updates

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
