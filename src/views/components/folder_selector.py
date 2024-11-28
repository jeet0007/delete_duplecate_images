"""
Folder selection component.
"""
import customtkinter as ctk
from typing import Optional, Callable

class FolderSelector(ctk.CTkFrame):
    """Component for folder selection with browse button."""
    
    def __init__(self, master, on_browse: Optional[Callable[[], None]] = None):
        super().__init__(master)
        self.on_browse = on_browse
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components."""
        self.folder_label = ctk.CTkLabel(self, text="Select Folder:")
        self.folder_label.pack(side="left", padx=5)
        
        self.folder_path = ctk.CTkEntry(self, width=400)
        self.folder_path.pack(side="left", padx=5)
        
        self.browse_button = ctk.CTkButton(
            self,
            text="Browse",
            command=self._handle_browse
        )
        self.browse_button.pack(side="left", padx=5)
    
    def _handle_browse(self):
        """Handle browse button click."""
        if self.on_browse:
            self.on_browse()
    
    def get_path(self) -> str:
        """Get the current folder path."""
        return self.folder_path.get()
    
    def set_path(self, path: str):
        """Set the folder path."""
        self.folder_path.delete(0, "end")
        self.folder_path.insert(0, path)
