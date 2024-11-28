"""
Controller for the GUI application.
"""
import threading
from typing import List, Optional
from ..models.image_finder import ImageFinder, ImageGroup
from ..views.gui_view import DuplicateFinderView

class DuplicateFinderController:
    """Controller that coordinates between the ImageFinder model and GUI view."""
    
    def __init__(self):
        self.model = ImageFinder()
        self.view = DuplicateFinderView()
        self.current_duplicates: Optional[List[ImageGroup]] = None
        self.scanning_thread: Optional[threading.Thread] = None
        self.cancel_scan = False
        
        # Set up view callbacks
        self.view.on_folder_select = self._handle_folder_select
        self.view.on_scan_start = self._handle_scan_start
        self.view.on_delete = self._handle_delete
        self.view.on_cancel = self._handle_cancel
        
        # Set up model callbacks
        self.model.set_progress_callback(self.view.update_progress)
        self.model.set_cancel_callback(self._is_scan_cancelled)

    def _is_scan_cancelled(self) -> bool:
        """Check if scan has been cancelled."""
        return self.cancel_scan

    def _handle_folder_select(self):
        """Handle folder selection."""
        folder = self.view.browse_folder()
        if folder:
            self.view.set_folder_path(folder)

    def _handle_scan_start(self):
        """Handle scan button click."""
        folder = self.view.get_folder_path()
        if not folder:
            self.view.show_error("Please select a folder first!")
            return

        self.view.set_scanning_state(True)
        self.current_duplicates = None
        self.cancel_scan = False

        def scan_thread():
            try:
                # Perform scan
                duplicates = self.model.find_duplicates(folder)
                if not self.cancel_scan:
                    self.current_duplicates = duplicates
                    # Update UI in main thread
                    self.view.window.after(0, self._show_scan_results)
                else:
                    # Show cancelled message in main thread
                    self.view.window.after(0, self.view.show_cancelled_message)
            finally:
                # Reset UI state in main thread
                self.view.window.after(0, lambda: self.view.set_scanning_state(False))

        self.view.show_scanning_message()
        self.scanning_thread = threading.Thread(target=scan_thread, daemon=True)
        self.scanning_thread.start()

    def _show_scan_results(self):
        """Show scan results in the view."""
        if not self.current_duplicates:
            self.view.show_no_duplicates_message()
            # Ensure delete button is disabled if no duplicates
            self.view.disable_delete_button()
            self.view.disable_cancel_button()
        else:
            # Display duplicates with any processing errors
            self.view.display_duplicates(self.current_duplicates, self.model.errors)
            
            # Enable delete button
            self.view.enable_delete_button()
            self.view.disable_cancel_button()

    def _handle_delete(self):
        """Handle delete button click."""
        if not self.current_duplicates:
            return
            
        if self.view.confirm_deletion():
            deleted = self.model.delete_duplicates(self.current_duplicates)
            self.view.show_deletion_results(deleted, self.model.errors)
            self.view.disable_delete_button()
            self.view.show_deletion_complete(len(deleted))
            self.current_duplicates = None

    def _handle_cancel(self):
        """Handle cancel button click."""
        self.cancel_scan = True

    def run(self):
        """Start the application."""
        self.view.run()
