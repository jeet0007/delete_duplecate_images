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

## Architecture

The application follows the Model-View-Controller (MVC) pattern:
- **Models**: Core business logic for image processing and duplicate detection
- **Views**: Component-based GUI with modular design
- **Controllers**: Coordination between models and views, handling user interactions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/delete_duplicate_images.git
cd delete_duplicate_images
```

2. Install the required dependencies:
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

## How it Works

The tool uses perceptual hashing to identify visually similar images. This means it can detect duplicates even if they have:
- Different file names
- Different resolutions
- Minor modifications
- Different formats

### Components

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

Feel free to open issues or submit pull requests to improve the tool.

## License

MIT License
