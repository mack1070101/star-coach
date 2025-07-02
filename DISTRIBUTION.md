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

## 🔄 Automated Releases

The `.github/workflows/release.yml` file will automatically:

1. **Build the package** when you push a tag
2. **Create a GitHub release** with assets
3. **Upload to PyPI** (if configured)

### To Create a Release:

```bash
# Tag and push
git tag v0.1.0
git push origin v0.1.0
```

## 📋 Distribution Checklist

### Before First Release:

- [ ] **Update version** in `star_coach/__init__.py`
- [ ] **Update version** in `pyproject.toml`
- [ ] **Update version** in Homebrew formula
- [ ] **Test installation** locally
- [ ] **Create GitHub repository**
- [ ] **Push code** to GitHub
- [ ] **Create release** with tag

### For Each Release:

- [ ] **Update version numbers**
- [ ] **Test locally** with `pip install -e .`
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
star-coach-standalone --help
```

### Test Package Installation:

```bash
# Build package
python -m build

# Install from wheel
pip install dist/star_coach-0.1.0-py3-none-any.whl

# Test
star-coach --help
```

## 📊 Distribution Methods Summary

| Method | Command | Pros | Cons |
|--------|---------|------|------|
| **Homebrew** | `brew install mack1070101/star-coach/star-coach` | Easy for macOS users, professional | macOS only |
| **PyPI** | `pip install star-coach` | Cross-platform, standard | Requires Python |
| **Standalone** | Download script | No dependencies, simple | Manual download |
| **GitHub Release** | Download assets | Direct, no package manager | Manual installation |

## 🎯 Recommended Workflow

1. **Start with GitHub releases** (easiest)
2. **Add Homebrew tap** (for macOS users)
3. **Publish to PyPI** (for Python users)
4. **Consider other package managers** (Chocolatey, Snap, etc.)

## 🔧 Troubleshooting

### Common Issues:

**Homebrew installation fails:**
- Check SHA256 in formula
- Ensure release URL is correct
- Verify Python dependency

**PyPI upload fails:**
- Check package name availability
- Verify build artifacts
- Test locally first

**Standalone script issues:**
- Ensure Python 3.8+ is available
- Check file permissions
- Test with different Python versions

## 📞 Support

For distribution issues:
- Check GitHub Issues
- Review Homebrew documentation
- Test with clean environments 