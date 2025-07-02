# 🌟 STAR Coach

A CLI tool that helps job candidates practice giving STAR answers (Situation, Task, Action, Result) for interviews with timed sections and beautiful progress bars.

## ✨ Features

- **Timed Practice Sessions**: Each STAR section has configurable timing
- **Enhanced CLI Interface**: Rich interactive interface with prompt_toolkit
- **Flexible Input**: Works with `.org` or `.txt` files
- **Default Fallbacks**: Uses sensible defaults when no file is provided
- **Real-time Progress**: Live progress bars that update every second
- **Graceful Fallback**: Works with or without prompt_toolkit
- **Interactive Controls**: Keyboard shortcuts for pause/resume/quit

## 🚀 Quick Start

### Installation

**Option 1: Homebrew (macOS) - Enhanced Version**
```bash
brew tap mack1070101/star-coach
brew install star-coach
```

**Option 2: Direct Download - Enhanced Version**
```bash
# Download the standalone script
curl -O https://raw.githubusercontent.com/mack1070101/star-coach/main/star_coach_standalone.py

# Install prompt_toolkit for enhanced interface
pip install prompt_toolkit

# Run it
python star_coach_standalone.py
```

**Option 3: Clone Repository - Enhanced Version**
```bash
git clone https://github.com/mack1070101/star-coach.git
cd star-coach
pip install prompt_toolkit
python star_coach_standalone.py
```

**Option 4: Basic Version (No Dependencies)**
```bash
# Download and run without prompt_toolkit
curl -O https://raw.githubusercontent.com/mack1070101/star-coach/main/star_coach_standalone.py
python star_coach_standalone.py --basic
```

### Basic Usage

**Practice with default empty sections:**
```bash
star-coach
```

**Practice with a custom STAR file:**
```bash
star-coach --file example_star.org
```

**Force basic interface (no prompt_toolkit):**
```bash
star-coach --basic
```

## 🎨 Enhanced Interface Features

When `prompt_toolkit` is available, you get:

- **Full-screen interface** with rich formatting
- **Real-time progress bars** with smooth animations
- **Keyboard shortcuts**:
  - `q` - Quit the current section
  - `space` - Pause/resume (planned feature)
- **Color-coded sections** and content
- **Responsive layout** that adapts to terminal size
- **Mouse support** for interactive elements

## 📝 File Format

STAR Coach reads `.org` or `.txt` files with the following format:

```org
* Situation: 3m

- I was working on a project with tight deadlines
- The team was struggling with coordination

* Task: 2m

- I needed to coordinate with multiple teams
- Create a timeline and ensure delivery

* Action: 4m

- I created a detailed timeline and held daily standups
- Implemented tracking tools and communication channels

* Result: 1m

- We delivered the project on time and under budget
- Team efficiency improved by 40%
```

### Timing Format

- **With timing**: `* SectionName: 3m` (3 minutes)
- **Without timing**: `* SectionName` (uses defaults)
- **Default times**: Situation (2m), Task (1m), Action (2m), Result (1m)

## 🛠️ Development

### Project Structure

```
star-coach/
├── star_coach_standalone.py  # Main CLI application (enhanced)
├── example_star.org          # Example STAR practice file
├── requirements.txt          # Dependencies for enhanced version
├── README.md                 # This file
└── homebrew-tap/            # Homebrew distribution files
    └── star-coach.rb        # Homebrew formula
```

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mack1070101/star-coach.git
   cd star-coach
   ```

2. **Install dependencies for enhanced version:**
   ```bash
   pip install prompt_toolkit
   ```

3. **Run the script:**
   ```bash
   python star_coach_standalone.py --help
   ```

4. **Test with example file:**
   ```bash
   python star_coach_standalone.py --file example_star.org
   ```

5. **Test basic version:**
   ```bash
   python star_coach_standalone.py --basic --file example_star.org
   ```

## 📋 Example Session

When you run STAR Coach with the enhanced interface, you'll see:

```
🌟 STAR Coach - Enhanced Interview Practice Tool
Get ready to practice your STAR answers with rich interface!

📁 Loaded content from: example_star.org
📊 Found 4 sections to practice
🎨 Using enhanced interface with prompt_toolkit

[Full-screen interface with rich formatting, progress bars, and controls]
```

## 🎯 Use Cases

- **Interview Preparation**: Practice your STAR answers with realistic timing
- **Public Speaking**: Get comfortable with timed presentations
- **Team Training**: Help team members practice structured communication
- **Self-Assessment**: Time yourself to improve your storytelling skills

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Enhanced with [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) for rich CLI experience
- Graceful fallback to basic interface when dependencies aren't available
- Beautiful progress bars and interactive controls
- Simple and focused design for interview practice

---

**Happy practicing! 🎉** 