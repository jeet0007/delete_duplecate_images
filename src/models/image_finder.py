"""
Image finder model that handles the core business logic for finding and managing duplicate images.
"""
from pathlib import Path
from PIL import Image
from collections import defaultdict
import hashlib
from typing import List, Dict, Tuple, Callable, Optional, Union, Iterator
from dataclasses import dataclass
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

@dataclass
class ImageGroup:
    """Group of duplicate images."""
    hash_value: str
    paths: List[Path]

class ImageFinder:
    """Find and manage duplicate images."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.heif'}
    BATCH_SIZE = 100  # Process images in batches of 100
    
    def __init__(self):
        self.image_hashes: Dict[str, List[Path]] = defaultdict(list)
        self.errors: List[str] = []
        self._progress_callback: Optional[Callable[[float], None]] = None
        self._cancel_callback: Optional[Callable[[], bool]] = None
        self._current_progress: int = 0
        self._total_files: int = 0

    def set_progress_callback(self, callback: Optional[Callable[[float], None]]) -> None:
        """Set callback for progress updates."""
        self._progress_callback = callback

    def set_cancel_callback(self, callback: Optional[Callable[[], bool]]) -> None:
        """Set callback to check if operation should be cancelled."""
        self._cancel_callback = callback

    def _update_progress(self, value: int) -> None:
        """Update progress and notify through callback if set."""
        self._current_progress = value
        if self._progress_callback:
            self._progress_callback(value)

    def is_supported_image(self, file_path: Path) -> bool:
        """Check if the file is a supported image format."""
        if file_path.name.startswith('._'):  # Skip macOS metadata files
            return False
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS

    def compute_image_hash(self, image_path: Path) -> Optional[str]:
        """Compute perceptual hash for an image."""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Resize to thumbnail for faster comparison
                img.thumbnail((100, 100))
                # Get image data as bytes
                img_data = img.tobytes()
                # Compute MD5 hash
                return hashlib.md5(img_data).hexdigest()
        except Exception as e:
            self.errors.append(f"Error processing {image_path.name}: {str(e)}")
            return None

    def _batch_files(self, files: List[Path]) -> Iterator[List[Path]]:
        """Split files into batches for processing."""
        for i in range(0, len(files), self.BATCH_SIZE):
            yield files[i:i + self.BATCH_SIZE]

    def find_duplicates(self, folder: Union[str, Path]) -> List[ImageGroup]:
        """Find duplicate images in the given folder."""
        folder = Path(folder)
        if not folder.exists():
            raise ValueError(f"Folder {folder} does not exist")

        # Reset state
        self.image_hashes.clear()
        self.errors.clear()

        # Get all image files
        image_files = self._get_image_files(folder)
        total_files = len(image_files)
        if total_files == 0:
            return []

        files_processed = 0
        # Process files in batches
        for batch in self._batch_files(image_files):
            # Check for cancellation at the start of each batch
            if self._cancel_callback and self._cancel_callback():
                return []
            
            # Process each file in the batch
            for file in batch:
                try:
                    hash_val = self._calculate_image_hash(file)
                    self.image_hashes[hash_val].append(file)
                except Exception as e:
                    self.errors.append(f"Error processing {file}: {e}")
                
                files_processed += 1
                # Update progress
                if self._progress_callback:
                    progress = min(1.0, files_processed / total_files)
                    self._progress_callback(progress)

        # Filter for groups with duplicates
        duplicate_groups = [
            ImageGroup(hash_value=hash_val, paths=paths)
            for hash_val, paths in self.image_hashes.items()
            if len(paths) > 1
        ]

        return duplicate_groups

    def _get_image_files(self, folder: Path) -> List[Path]:
        return [f for f in folder.rglob('*') if self.is_supported_image(f)]

    def _calculate_image_hash(self, file: Path) -> str:
        return self.compute_image_hash(file)

    def delete_duplicates(self, duplicates: List[ImageGroup], keep_original: bool = True) -> List[Path]:
        """
        Delete duplicate images.
        
        :param duplicates: List of ImageGroup containing duplicate images
        :param keep_original: If True, keep the first image in each group
        :return: List of deleted image paths
        """
        deleted_paths: List[Path] = []
        
        for group in duplicates:
            # If keep_original is True, keep the first image in the group
            images_to_delete = group.paths[1:] if keep_original else group.paths
            
            for image_path in images_to_delete:
                try:
                    # Check for cancellation
                    if self._cancel_callback and self._cancel_callback():
                        break
                    
                    # Delete the file
                    image_path.unlink()
                    deleted_paths.append(image_path)
                except Exception as e:
                    self.errors.append(f"Error deleting {image_path}: {e}")
        
        return deleted_paths
