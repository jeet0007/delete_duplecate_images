"""
Component for displaying scan and deletion results.
"""
import customtkinter as ctk
from pathlib import Path
from typing import List
from .duplicate_group import DuplicateGroup
from ...models.image_finder import ImageGroup

class ResultsDisplay(ctk.CTkScrollableFrame):
    """Component that displays scan results and deletion status."""
    
    def __init__(self, master):
        super().__init__(master)
        self.image_refs = []  # Keep references to prevent garbage collection
    
    def clear(self):
        """Clear all results."""
        for widget in self.winfo_children():
            widget.destroy()
        self.image_refs.clear()
    
    def show_error(self, message: str):
        """Display an error message."""
        self.clear()
        error_label = ctk.CTkLabel(
            self,
            text=message,
            text_color="red",
            font=("Arial", 12, "bold")
        )
        error_label.pack(pady=20)
    
    def show_scanning_message(self):
        """Show scanning in progress message."""
        self.clear()
        scanning_label = ctk.CTkLabel(
            self,
            text="Scanning for duplicates...",
            font=("Arial", 12)
        )
        scanning_label.pack(pady=20)
    
    def show_warnings(self, errors: List[str]):
        """Display warning messages."""
        if not errors:
            return
            
        error_label = ctk.CTkLabel(
            self,
            text="Warnings:",
            font=("Arial", 12, "bold")
        )
        error_label.pack(anchor="w", padx=5, pady=5)
        
        for error in errors[:5]:
            warn_label = ctk.CTkLabel(
                self,
                text=f"• {error}",
                text_color="orange"
            )
            warn_label.pack(anchor="w", padx=20)
        
        if len(errors) > 5:
            more_label = ctk.CTkLabel(
                self,
                text=f"... and {len(errors) - 5} more warnings",
                text_color="orange"
            )
            more_label.pack(anchor="w", padx=20, pady=(0, 10))
    
    def show_duplicates(self, duplicates: List[ImageGroup], errors: List[str]):
        """Display duplicate image groups and any errors."""
        self.clear()
        
        # Show any warnings
        self.show_warnings(errors)
        
        if not duplicates:
            no_dupes_label = ctk.CTkLabel(
                self,
                text="No duplicates found!",
                font=("Arial", 14, "bold")
            )
            no_dupes_label.pack(pady=20)
            return
        
        # Show total count
        total_label = ctk.CTkLabel(
            self,
            text=f"Found {len(duplicates)} groups of duplicates:",
            font=("Arial", 14, "bold")
        )
        total_label.pack(anchor="w", padx=5, pady=10)
        
        # Show each duplicate group
        for group in duplicates:
            group_widget = DuplicateGroup(self, group.hash_value, group.paths)
            group_widget.pack(fill="x", padx=5, pady=10)
            # Keep reference to prevent garbage collection
            self.image_refs.extend(group_widget.image_refs)
    
    def show_deletion_results(self, deleted: List[Path], errors: List[str]):
        """Display deletion results and any errors."""
        self.clear()
        
        # Show any warnings
        self.show_warnings(errors)
        
        # Show success message
        success_label = ctk.CTkLabel(
            self,
            text=f"Successfully deleted {len(deleted)} duplicate files:",
            font=("Arial", 12, "bold")
        )
        success_label.pack(anchor="w", padx=5, pady=(10, 5))
        
        # List deleted files
        for path in deleted:
            file_label = ctk.CTkLabel(
                self,
                text=f"• {path.name}"
            )
            file_label.pack(anchor="w", padx=20)
