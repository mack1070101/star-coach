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

**Option 1: pip from GitHub (Recommended)**
```bash
pip install git+https://github.com/mack1070101/story-star.git
```

**Option 2: Homebrew (macOS)**
```bash
brew tap mack1070101/star-coach
brew install star-coach
```

**Option 3: Direct Download**
```bash
# Download the standalone script
curl -O https://raw.githubusercontent.com/mack1070101/story-star/main/star_coach_standalone.py

# Install prompt_toolkit for enhanced interface
pip install prompt_toolkit

# Run it
python star_coach_standalone.py
```

**Option 4: Clone Repository**
```bash
git clone https://github.com/mack1070101/story-star.git
cd story-star
pip install -e .
```

**Option 5: Basic Version (No Dependencies)**
```bash
# Download and run without prompt_toolkit
curl -O https://raw.githubusercontent.com/mack1070101/story-star/main/star_coach_standalone.py
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
- **Interactive Controls**:
  - **↑ Up Arrow**: Restart the current section
  - **↓ Down Arrow**: Quit/skip the current section
  - **← Left Arrow**: Skip back 5 seconds
  - **→ Right Arrow**: Skip forward 5 seconds
  - **Space**: Pause/resume the timer
  - **Q**: Quit the entire application
- **Color-coded sections** and content
- **Responsive layout** that adapts to terminal size
- **Mouse support** for interactive elements
- **Live status display** showing pause state and time remaining

## 📝 File Format

STAR Coach reads `.org` or `.txt` files with the following format:

```
* Pre Prompt
This text will appear at the top of every section. Use it for reminders, tips, or a motivational message!

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

### Pre Prompt Section
- If your file contains a section titled `* Pre Prompt`, its content will be displayed at the top of every STAR section (Situation, Task, Action, Result).
- This is useful for reminders, interview tips, or any message you want to see throughout your session.

### Timing Format
- **With timing**: `* SectionName: 3m` (3 minutes)
- **Without timing**: `* SectionName` (uses defaults)
- **Default times**: Situation (2m), Task (1m), Action (2m), Result (1m)

## 🛠️ Development

### Project Structure

```
story-star/
├── star_coach/              # Python package
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Main CLI application
│   └── example_star.org     # Example STAR practice file
├── star_coach_standalone.py # Standalone script (legacy)
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
├── README.md                # This file
└── homebrew-tap/           # Homebrew distribution files
    └── star-coach.rb       # Homebrew formula
```

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mack1070101/story-star.git
   cd story-star
   ```

2. **Install in development mode:**
   ```bash
   pip install -e .
   ```

3. **Run the CLI:**
   ```bash
   star-coach --help
   ```

4. **Test with example file:**
   ```bash
   star-coach --file star_coach/example_star.org
   ```

5. **Test basic version:**
   ```bash
   star-coach --basic --file star_coach/example_star.org
   ```

6. **Run the standalone script directly:**
   ```bash
   python star_coach_standalone.py --help
   ```

## 📋 Example Session

When you run STAR Coach with the enhanced interface, you'll see:

```
🌟 STAR Coach - Enhanced Interview Practice Tool
Get ready to practice your STAR answers with rich interface and controls!

📁 Loaded content from: example_star.org
📊 Found 4 sections to practice
🎨 Using enhanced interface with prompt_toolkit and user controls

[Full-screen interface with rich formatting, progress bars, and interactive controls]
```

The interface provides:
- **Section content display** with clear formatting
- **Progress bar** showing completion percentage
- **Control instructions** with arrow key mappings
- **Live timer** with minutes:seconds remaining
- **Status indicator** showing if timer is paused or running

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