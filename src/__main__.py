"""
Main entry point for the duplicate image finder application.
"""
import argparse
from pathlib import Path
from .controllers.gui_controller import DuplicateFinderController
from .models.image_finder import ImageFinder

def main():
    parser = argparse.ArgumentParser(description='Find and manage duplicate images.')
    parser.add_argument('--gui', action='store_true', help='Start the GUI application')
    parser.add_argument('--folder', type=str, help='Folder to scan for duplicates')
    args = parser.parse_args()

    if args.gui:
        # Start GUI application
        app = DuplicateFinderController()
        app.run()
    elif args.folder:
        # CLI mode
        finder = ImageFinder()
        folder_path = Path(args.folder)
        
        if not folder_path.exists():
            print(f"Error: Folder '{args.folder}' does not exist")
            return
        
        print(f"Scanning folder: {folder_path}")
        duplicates = finder.find_duplicates(str(folder_path))
        
        if finder.errors:
            print("\nWarnings:")
            for error in finder.errors:
                print(f"  {error}")
        
        if not duplicates:
            print("\nNo duplicates found!")
            return
        
        print(f"\nFound {len(duplicates)} groups of duplicates:")
        for group in duplicates:
            print(f"\nDuplicate Group (Hash: {group.hash_value[:8]}):")
            for path in group.paths:
                print(f"  {path}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
