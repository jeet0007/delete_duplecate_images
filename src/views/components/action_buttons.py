"""
Action buttons component.
"""
import os
import io
import customtkinter as ctk
from typing import Optional, Callable
from PIL import Image
from cairosvg import svg2png

class ActionButtons(ctk.CTkFrame):
    """Component for scan and delete buttons."""
    
    def __init__(
            self,
            master,
            on_scan: Optional[Callable[[], None]] = None,
            on_delete: Optional[Callable[[], None]] = None,
            on_cancel: Optional[Callable[[], None]] = None
        ):
        super().__init__(master)
        self.on_scan = on_scan
        self.on_delete = on_delete
        self.on_cancel = on_cancel
        
        # Load icons
        self.icons = self._load_icons()
        self._setup_ui()
        
    def _load_icons(self):
        """Load all icons."""
        icons = {}
        icon_path = os.path.join('assets', 'icons', 'svg')
        
        # Define icon sizes (in pixels)
        icon_size = (24, 24)
        
        # Load icons if they exist
        icon_files = {
            'scan': 'scan-icon.svg',
            'folder': 'folder_open_icon.svg',
            'delete': 'delete_icon.svg',
            'cancel': 'cancel_icon.svg',
            'success': 'success.svg',
            'duplicate': 'duplicate_icon.svg'
        }
        
        for name, filename in icon_files.items():
            path = os.path.join(icon_path, filename)
            if os.path.exists(path):
                try:
                    # Convert SVG to PNG in memory
                    png_data = svg2png(url=path, output_width=icon_size[0], output_height=icon_size[1])
                    # Create PIL Image from PNG data
                    img = Image.open(io.BytesIO(png_data))
                    # Create CustomTkinter image
                    icons[name] = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=icon_size
                    )
                except Exception as e:
                    print(f"Failed to load icon {filename}: {e}")
                    continue
        
        return icons
    
    def _setup_ui(self):
        """Setup the UI components."""
        # Scan button with icon
        self.scan_button = ctk.CTkButton(
            self,
            text="Scan for Duplicates",
            command=self._handle_scan,
            image=self.icons.get('scan')
        )
        self.scan_button.pack(side="left", padx=5)
        
        # Cancel button with icon
        self.cancel_button = ctk.CTkButton(
            self,
            text="Cancel",
            command=self._handle_cancel,
            fg_color="red",
            hover_color="darkred",
            image=self.icons.get('cancel')
        )
        self.cancel_button.pack(side="left", padx=5)
        self.cancel_button.configure(state="disabled")
        self.cancel_button.pack_forget()
        
        # Delete button with icon
        self.delete_button = ctk.CTkButton(
            self,
            text="Delete Selected",
            command=self._handle_delete,
            image=self.icons.get('delete')
        )
        self.delete_button.pack(side="left", padx=5)
        self.delete_button.configure(state="disabled")
        self.delete_button.pack_forget()
    
    def _handle_scan(self):
        """Handle scan button click."""
        if self.on_scan:
            self.on_scan()
    
    def _handle_delete(self):
        """Handle delete button click."""
        if self.on_delete:
            self.on_delete()
    
    def _handle_cancel(self):
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()
            
    def set_scanning_state(self, is_scanning: bool):
        """Update button states based on scanning state."""
        if is_scanning:
            # During scanning: hide delete, show cancel
            self.scan_button.pack_forget()
            self.delete_button.pack_forget()
            self.cancel_button.pack(side="left", padx=5)
            self.cancel_button.configure(state="normal")
        else:
            # After scanning: hide cancel, show scan and potentially delete
            self.cancel_button.pack_forget()
            self.scan_button.pack(side="left", padx=5)
            
    def enable_delete(self):
        """Enable the delete button."""
        self.delete_button.pack(side="left", padx=5)
        self.delete_button.configure(state="normal")
    
    def disable_delete(self):
        """Disable delete button."""
        self.delete_button.pack_forget()
