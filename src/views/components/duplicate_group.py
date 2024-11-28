"""
Component for displaying a group of duplicate images.
"""
import customtkinter as ctk
from PIL import Image
from pathlib import Path
from typing import List

class DuplicateGroup(ctk.CTkFrame):
    """Component that displays a group of duplicate images with thumbnails."""
    
    def __init__(self, master, hash_value: str, paths: List[Path]):
        super().__init__(master)
        self.hash_value = hash_value
        self.paths = paths
        self.image_refs = []  # Keep references to prevent garbage collection
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components."""
        # Group header
        self.header = ctk.CTkLabel(
            self,
            text=f"Duplicate Group (Hash: {self.hash_value[:8]})",
            font=("Arial", 12, "bold")
        )
        self.header.pack(anchor="w", padx=10, pady=5)
        
        # Thumbnails frame
        self.thumbs_frame = ctk.CTkFrame(self)
        self.thumbs_frame.pack(fill="x", padx=10, pady=5)
        
        # Display thumbnails
        self._show_thumbnails()
    
    def _show_thumbnails(self):
        """Display thumbnails for each image in the group."""
        for path in self.paths:
            try:
                img_frame = ctk.CTkFrame(self.thumbs_frame)
                img_frame.pack(side="left", padx=5, pady=5)
                
                with Image.open(path) as img:
                    img.thumbnail((150, 150))
                    photo = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=(150, 150)
                    )
                    self.image_refs.append(photo)
                    
                    img_label = ctk.CTkLabel(img_frame, image=photo, text="")
                    img_label.pack(padx=5, pady=5)
                    
                    name_label = ctk.CTkLabel(
                        img_frame,
                        text=path.name,
                        wraplength=150
                    )
                    name_label.pack(padx=5, pady=(0, 5))
            except Exception as e:
                error_label = ctk.CTkLabel(
                    img_frame,
                    text=f"Error loading\n{path.name}:\n{str(e)}",
                    text_color="red"
                )
                error_label.pack(padx=5, pady=5)
