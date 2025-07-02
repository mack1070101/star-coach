# Homebrew Tap for STAR Coach

This is a Homebrew tap for the STAR Coach CLI tool - a standalone Python script for practicing STAR interview answers.

## Installation

```bash
# Add the tap
brew tap mack1070101/star-coach

# Install STAR Coach
brew install star-coach
```

## Usage

After installation, you can use:

```bash
# Practice with default empty sections
star-coach

# Practice with custom file
star-coach --file example.org

# Practice with the included example
star-coach --file example_star.org
```

## What's Included

- **star-coach**: Standalone Python script with no external dependencies
- **Beautiful progress bars** and timed sections
- **Support for .org and .txt files** with custom timing
- **Real-time countdown** for each STAR section

## Features

- ✅ **No dependencies** - Uses only Python standard library
- ✅ **Timed practice sessions** - Configurable timing per section
- ✅ **File support** - Works with .org and .txt files
- ✅ **Default fallbacks** - Sensible defaults when no file provided
- ✅ **Cross-platform** - Works on any system with Python 3.8+

## More Information

Visit the main repository: https://github.com/mack1070101/star-coach 