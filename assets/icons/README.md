# Project Icons with Iconify

## Directory Structure
- `svg/`: Scalable Vector Graphics icons (recommended for most uses)
- `png/`: Portable Network Graphics icons (for compatibility)
- `ico/`: Windows icon format

## Icon Sources
- Material Design Icons
- Feather Icons
- Font Awesome

## Usage Guidelines
1. Prefer SVG icons when possible
2. Maintain consistent color scheme
3. Ensure icons are clear and recognizable at different sizes

## Usage in Code
```python
import iconify as ico

# Scan button icon
scan_icon = ico.Icon('mdi:magnify')
scan_button.setIcon(scan_icon)

# Folder selection icon
folder_icon = ico.Icon('mdi:folder-open')
folder_button.setIcon(folder_icon)

# Delete icon
delete_icon = ico.Icon('mdi:delete', color=QtGui.QColor('red'))
delete_button.setIcon(delete_icon)
```

## Icon Libraries
- Material Design Icons (mdi:)
- Font Awesome
- Many more available via `iconify-browser`

## Finding Icons
1. Run `iconify-browser`
2. Search and copy icon identifier
3. Use in your code

## Planned Icons
- App Icon
- Scan Button
- Delete Button
- Folder Select Button
- Cancel Button
- Progress Indicators
