# 🚀 Distribution Guide for STAR Coach

This guide explains how to distribute STAR Coach via Homebrew and other methods.

## 📦 Homebrew Distribution

### Step 1: Create GitHub Repository

1. **Create a new repository** on GitHub (e.g., `mack1070101/star-coach`)
2. **Push your code** to the repository
3. **Create a release** with tag `v0.1.0`

### Step 2: Create Homebrew Tap

1. **Create a new repository** for your Homebrew tap (e.g., `mack1070101/homebrew-star-coach`)
2. **Add the formula** from `homebrew-tap/star-coach.rb`
3. **Update the SHA256** in the formula:

```bash
# Calculate SHA256 for your release
curl -L https://github.com/mack1070101/star-coach/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
```

### Step 3: Update Formula

Replace `PLACEHOLDER_SHA256` in `homebrew-tap/star-coach.rb` with the actual SHA256.

### Step 4: Users Can Install

```bash
# Add the tap
brew tap mack1070101/star-coach

# Install STAR Coach
brew install star-coach
```

## 🔄 Manual Releases

Since we're using the standalone approach, releases are simple:

### To Create a Release:

```bash
# Tag and push
git tag v0.1.0
git push origin v0.1.0
```

### Manual Release Steps:

1. **Go to GitHub repository**
2. **Click "Releases" → "Draft a new release"**
3. **Tag:** `v0.1.0`
4. **Title:** `v0.1.0`
5. **Description:** Add release notes
6. **Attach files:**
   - `star_coach_standalone.py`
   - `example_star.org`
7. **Click "Publish release"**

## 📋 Distribution Checklist

### Before First Release:

- [ ] **Update version** in `star_coach_standalone.py` (if needed)
- [ ] **Test locally** with `python star_coach_standalone.py`
- [ ] **Create GitHub repository**
- [ ] **Push code** to GitHub
- [ ] **Create release** with tag

### For Each Release:

- [ ] **Test locally** with `python star_coach_standalone.py`
- [ ] **Create and push tag**
- [ ] **Update Homebrew formula SHA256**
- [ ] **Test Homebrew installation**

## 🛠️ Local Testing

### Test Homebrew Formula Locally:

```bash
# Test the formula
brew install --build-from-source ./homebrew-tap/star-coach.rb

# Test the installation
star-coach --help
```

### Test Standalone Script:

```bash
# Test basic functionality
python star_coach_standalone.py --help

# Test with example file
python star_coach_standalone.py --file example_star.org

# Test with no file (default sections)
python star_coach_standalone.py
```

## 📊 Distribution Methods Summary

| Method | Command | Pros | Cons |
|--------|---------|------|------|
| **Homebrew** | `brew install mack1070101/star-coach/star-coach` | Easy for macOS users, professional | macOS only |
| **Direct Download** | `curl -O https://raw.githubusercontent.com/mack1070101/star-coach/main/star_coach_standalone.py` | No dependencies, simple | Manual download |
| **GitHub Release** | Download from releases page | Direct, no package manager | Manual installation |
| **Git Clone** | `git clone https://github.com/mack1070101/star-coach.git` | Full source, version control | Requires git |

## 🎯 Recommended Workflow

1. **Start with GitHub releases** (easiest)
2. **Add Homebrew tap** (for macOS users)
3. **Consider other package managers** (Chocolatey, Snap, etc.)

## 🔧 Troubleshooting

### Common Issues:

**Homebrew installation fails:**
- Check SHA256 in formula
- Ensure release URL is correct
- Verify Python dependency

**Standalone script issues:**
- Ensure Python 3.8+ is available
- Check file permissions
- Test with different Python versions

**File not found errors:**
- Verify the script is in the correct location
- Check file permissions (`chmod +x star_coach_standalone.py`)

## 📞 Support

For distribution issues:
- Check GitHub Issues
- Review Homebrew documentation
- Test with clean environments

## 🎉 Benefits of Standalone Approach

✅ **No dependencies** - Uses only Python standard library  
✅ **Simple distribution** - Single file to share  
✅ **Easy installation** - Just download and run  
✅ **Cross-platform** - Works on any system with Python  
✅ **No build process** - No complex packaging required  
✅ **Version control friendly** - Easy to track changes 