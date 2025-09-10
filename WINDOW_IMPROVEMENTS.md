# RECON-OPS Window Improvements

## 🎯 Better Window Experience on Windows

The RECON-OPS application has been significantly improved for better usability and window management on Windows systems.

## ✅ Key Improvements

### 1. **Responsive Window Sizing**
- Window now adapts to your screen size (75% of screen dimensions)
- Reasonable size limits: minimum 800x600, maximum based on screen size
- Better initial sizing for different screen resolutions

### 2. **Improved Resizability** 
- Lower minimum window size (800x600 instead of 1200x800)
- More reasonable maximum window size
- Better component flexibility when resizing

### 3. **Flexible Layout**
- Text area now expands with window size instead of fixed height
- All components properly scale and adjust to window resizing
- Word wrapping enabled for better text flow
- Larger, more readable font in the queries area

### 4. **Automatic Window Management**
- Auto-maximizes on smaller screens (≤1366x768) for optimal experience
- Smart initial window positioning (centered on screen)
- Window state persistence (remembers your preferred size)

### 5. **Enhanced User Experience**
- Smoother resizing behavior
- Better layout adaptation
- Components remain accessible during resize operations
- All buttons and controls stay visible

## 🔧 Technical Details

### Window Configuration
- **Initial Size**: 75% of screen size (1000-1400px width, 700-1000px height)
- **Minimum Size**: 800x600 pixels
- **Maximum Size**: Full screen dimensions
- **Auto-maximize**: Enabled for screens ≤1366x768

### Layout Improvements
- Responsive text area that grows/shrinks with window
- Fixed header and control sections
- Expandable queries section
- Always-visible action buttons at bottom

### Settings Persistence
- Window size preferences saved to `recon_ops_settings.json`
- Automatic loading of previous window dimensions
- Graceful fallback to defaults if settings file is corrupted

## 🚀 Usage

1. **First Launch**: Application opens with optimal size for your screen
2. **Resize**: Drag window corners/edges - all components adapt smoothly  
3. **Maximize**: Use Windows maximize button or auto-maximize feature
4. **Settings**: Your window size is automatically remembered between sessions

## 🎨 What Changed

### Before:
- Fixed 1400x1000 window (often too large)
- High minimum size (1200x800) - hard to resize smaller
- Fixed text area height - didn't use available space
- Poor resize behavior

### After:
- Adaptive sizing based on your screen
- Reasonable minimum size (800x600)
- Expandable text area that grows with window
- Smooth resizing with proper component scaling
- Auto-maximize on smaller screens
- Window size memory between sessions

## 💡 Tips

- **Small Screen**: Application auto-maximizes for best experience
- **Large Screen**: Starts at 75% size, can be resized as needed
- **Text Area**: Now expands to use available window space
- **Memory**: Your preferred window size is remembered
- **Reset**: Delete `recon_ops_settings.json` to reset to defaults

The application now provides a much better user experience with proper window management that adapts to different screen sizes and user preferences!
