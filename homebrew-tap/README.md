# Homebrew Tap for STAR Coach

This is a Homebrew tap for the STAR Coach CLI tool - an enhanced Python script for practicing STAR interview answers with rich interactive interface.

## Installation

```bash
# Add the tap
brew tap mack1070101/star-coach

# Install STAR Coach (includes prompt_toolkit for enhanced interface)
brew install star-coach
```

## Usage

After installation, you can use:

```bash
# Practice with enhanced interface (default)
star-coach

# Practice with custom file
star-coach --file example.org

# Practice with the included example
star-coach --file example_star.org

# Force basic interface (no prompt_toolkit)
star-coach --basic
```

## What's Included

- **star-coach**: Enhanced Python script with prompt_toolkit for rich interface
- **Beautiful progress bars** and timed sections with smooth animations
- **Full-screen interface** with color-coded sections
- **Keyboard shortcuts** for interactive control
- **Graceful fallback** to basic interface when needed
- **Support for .org and .txt files** with custom timing
- **Real-time countdown** for each STAR section

## Enhanced Features

- ✅ **Rich interactive interface** - Full-screen with prompt_toolkit
- ✅ **Smooth progress bars** - Real-time animations
- ✅ **Keyboard shortcuts** - `q` to quit, `space` for pause/resume
- ✅ **Color-coded sections** - Beautiful formatting
- ✅ **Responsive layout** - Adapts to terminal size
- ✅ **Mouse support** - Interactive elements
- ✅ **Graceful fallback** - Works without prompt_toolkit

## More Information

Visit the main repository: https://github.com/mack1070101/star-coach 