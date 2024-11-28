"""
Main entry point for the duplicate image finder application.
"""
import sys
import traceback
import logging
import argparse
from pathlib import Path
from .controllers.gui_controller import DuplicateFinderController
from .models.image_finder import ImageFinder

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    try:
        parser = argparse.ArgumentParser(description='Find and manage duplicate images.')
        parser.add_argument('--gui', action='store_true', help='Start the GUI application')
        parser.add_argument('--folder', type=str, help='Folder to scan for duplicates')
        args = parser.parse_args()

        if args.gui:
            # Start GUI application
            logger.info("Initializing controller...")
            app = DuplicateFinderController()
            logger.info("Starting main loop...")
            app.run()
        elif args.folder:
            # CLI mode
            logger.info("Initializing image finder...")
            finder = ImageFinder()
            folder_path = Path(args.folder)
            
            if not folder_path.exists():
                logger.error(f"Error: Folder '{args.folder}' does not exist")
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
                if group and group.hash_value:  # Add null check
                    print(f"\nDuplicate Group (Hash: {group.hash_value[:8]}):")
                    for path in group.paths:
                        print(f"  {path}")
        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
