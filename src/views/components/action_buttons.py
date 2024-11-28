"""
Action buttons component.
"""
import customtkinter as ctk
from typing import Optional, Callable

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
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components."""
        self.scan_button = ctk.CTkButton(
            self,
            text="Scan for Duplicates",
            command=self._handle_scan
        )
        self.scan_button.pack(side="left", padx=5)
        
        self.cancel_button = ctk.CTkButton(
            self,
            text="Cancel",
            command=self._handle_cancel,
            fg_color="red",
            hover_color="darkred"
        )
        self.cancel_button.pack(side="left", padx=5)
        self.cancel_button.configure(state="disabled")
        self.cancel_button.pack_forget()  # Initially hidden
        
        self.delete_button = ctk.CTkButton(
            self,
            text="Delete Selected",
            command=self._handle_delete
        )
        self.delete_button.pack(side="left", padx=5)
        self.delete_button.configure(state="disabled")
        self.delete_button.pack_forget()  # Initially hidden
    
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
