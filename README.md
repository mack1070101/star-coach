# 🌟 STAR Coach

A CLI tool that helps job candidates practice giving STAR answers (Situation, Task, Action, Result) for interviews with timed sections and beautiful progress bars.

## ✨ Features

- **Timed Practice Sessions**: Each STAR section has configurable timing
- **Beautiful CLI Interface**: Progress bars and formatted output
- **Flexible Input**: Works with `.org` or `.txt` files
- **Default Fallbacks**: Uses sensible defaults when no file is provided
- **Real-time Progress**: Live progress bars that update every second
- **No Dependencies**: Uses only Python standard library

## 🚀 Quick Start

### Installation

**Option 1: Homebrew (macOS)**
```bash
brew tap mack1070101/star-coach
brew install star-coach
```

**Option 2: Direct Download**
```bash
# Download the standalone script
curl -O https://raw.githubusercontent.com/mack1070101/star-coach/main/star_coach_standalone.py
chmod +x star_coach_standalone.py

# Run it
python star_coach_standalone.py
```

**Option 3: Clone Repository**
```bash
git clone https://github.com/mack1070101/star-coach.git
cd star-coach
python star_coach_standalone.py
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

**Or use the short flag:**
```bash
star-coach -f example_star.org
```

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
├── star_coach_standalone.py  # Main CLI application
├── example_star.org          # Example STAR practice file
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

2. **Run the script:**
   ```bash
   python star_coach_standalone.py --help
   ```

3. **Test with example file:**
   ```bash
   python star_coach_standalone.py --file example_star.org
   ```

## 📋 Example Session

When you run STAR Coach, you'll see output like this:

```
🌟 STAR Coach - Interview Practice Tool
Get ready to practice your STAR answers!

📁 Loaded content from: example_star.org
📊 Found 4 sections to practice

Section 1 of 4

📋 SITUATION
────────────────────────────────────────────────────────────
- I was working as a software engineer at a startup...
────────────────────────────────────────────────────────────

⏱️  Time: 3 minutes

Practice Situation...
[████████████████████████████████████████████████████] 100% ⏱️ 00:00 remaining
✅ Situation section complete!

Press Enter to continue to the next section...
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

- Built with Python standard library for maximum compatibility
- Beautiful CLI output with progress bars and formatting
- Simple and focused design for interview practice

---

**Happy practicing! 🎉** 