"""
Main GUI view implementation using customtkinter.
"""
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from typing import List, Optional, Callable
from .components.folder_selector import FolderSelector
from .components.action_buttons import ActionButtons
from .components.results_display import ResultsDisplay
from ..models.image_finder import ImageGroup

class DuplicateFinderView:
    """Main GUI view for the duplicate image finder application."""

    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Duplicate Image Finder")
        self.window.geometry("1024x768")
        
        # Callbacks to be set by controller
        self.on_folder_select: Optional[Callable[[], None]] = None
        self.on_scan_start: Optional[Callable[[], None]] = None
        self.on_delete: Optional[Callable[[], None]] = None
        self.on_cancel: Optional[Callable[[], None]] = None
        
        self._setup_gui()

    def _setup_gui(self):
        """Setup the GUI components."""
        # Folder selection
        self.folder_selector = FolderSelector(
            self.window,
            on_browse=self._on_browse_click
        )
        self.folder_selector.pack(pady=20, padx=20, fill="x")
        
        # Progress bar
        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            self.window,
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
        
        # Results display
        self.results_display = ResultsDisplay(self.window)
        self.results_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Action buttons
        self.action_buttons = ActionButtons(
            self.window,
            on_scan=self._on_scan_click,
            on_delete=self._on_delete_click,
            on_cancel=self._on_cancel_click
        )
        self.action_buttons.pack(pady=10, padx=20, fill="x")

    def _on_browse_click(self):
        """Handle browse button click."""
        if self.on_folder_select:
            self.on_folder_select()

    def _on_scan_click(self):
        """Handle scan button click."""
        if self.on_scan_start:
            self.on_scan_start()

    def _on_delete_click(self):
        """Handle delete button click."""
        if self.on_delete:
            self.on_delete()

    def _on_cancel_click(self):
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()

    def get_folder_path(self) -> str:
        """Get the current folder path."""
        return self.folder_selector.get_path()

    def set_folder_path(self, path: str):
        """Set the folder path."""
        self.folder_selector.set_path(path)

    def update_progress(self, value: float):
        """Update the progress bar.
        
        :param value: Progress value between 0 and 1
        """
        # Ensure the update happens in the main thread
        self.window.after(0, self._update_progress, value)
    
    def _update_progress(self, value: float):
        """Internal method to update progress bar."""
        self.progress_var.set(value)
        self.window.update_idletasks()

    def show_error(self, message: str):
        """Display an error message."""
        self.results_display.show_error(message)

    def show_scanning_message(self):
        """Show scanning in progress message."""
        self.results_display.show_scanning_message()

    def show_duplicates(self, duplicates: List[ImageGroup], errors: List[str]):
        """Display duplicate image groups and any errors."""
        self.results_display.show_duplicates(duplicates, errors)
        if duplicates:
            self.action_buttons.enable_delete()

    def show_deletion_results(self, deleted: List[Path], errors: List[str]):
        """Display deletion results and any errors."""
        self.results_display.show_deletion_results(deleted, errors)

    def confirm_deletion(self) -> bool:
        """Show deletion confirmation dialog."""
        return messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete all duplicate files?\n"
            "This action cannot be undone!"
        )

    def show_deletion_complete(self, count: int):
        """Show deletion completion message."""
        messagebox.showinfo(
            "Deletion Complete",
            f"Successfully deleted {count} duplicate files.\n"
            "Original copies have been preserved."
        )

    def set_scanning_state(self, scanning: bool):
        """Update UI state during scanning."""
        self.action_buttons.set_scanning_state(scanning)

    def enable_delete_button(self):
        """Enable the delete button."""
        self.action_buttons.enable_delete()

    def disable_delete_button(self):
        """Disable the delete button."""
        self.action_buttons.disable_delete()

    def browse_folder(self) -> Optional[str]:
        """Show folder selection dialog."""
        return ctk.filedialog.askdirectory()

    def show_cancelled_message(self):
        """Show scan cancelled message."""
        messagebox.showinfo("Cancelled", "Scan cancelled by user.")
        
    def display_duplicates(self, duplicates: List[ImageGroup], errors: Optional[List[str]] = None):
        """Display the list of duplicate image groups."""
        self.results_display.show_duplicates(duplicates, errors or [])
        
    def show_no_duplicates_message(self):
        """Show a message when no duplicates are found."""
        messagebox.showinfo("Scan Complete", "No duplicate images found.")

    def disable_cancel_button(self):
        """Disable and hide the cancel button."""
        self.action_buttons.cancel_button.pack_forget()

    def run(self):
        """Start the GUI event loop."""
        self.window.mainloop()
