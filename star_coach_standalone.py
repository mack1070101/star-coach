#!/usr/bin/env python3
"""
STAR Coach - Enhanced CLI tool for practicing STAR interview answers with timed sections.
Uses prompt_toolkit for rich interactive experience.
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import List, Optional

try:
    from prompt_toolkit import Application
    from prompt_toolkit.layout import Layout, HSplit, Window, ScrollablePane
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.containers import FloatContainer, Float
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.formatted_text import HTML, FormattedText
    from prompt_toolkit.widgets import ProgressBar, Label, Button
    from prompt_toolkit.styles import Style
    from prompt_toolkit.layout.dimension import D
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False
    print("Warning: prompt_toolkit not available. Falling back to basic interface.")
    print("Install with: pip install prompt_toolkit")


class STARSection:
    """Represents a single STAR section with content and timing."""
    
    def __init__(self, name: str, content: str, time_minutes: int):
        self.name = name
        self.content = content.strip()
        self.time_minutes = time_minutes
        self.time_seconds = time_minutes * 60


def parse_star_file(file_path: Optional[Path]) -> List[STARSection]:
    """
    Parse a .org or .txt file and extract STAR sections with timing.
    
    Args:
        file_path: Path to the input file, or None for empty practice
        
    Returns:
        List of STARSection objects
    """
    if file_path is None:
        # Return empty sections with default times
        return [
            STARSection("Situation", "", 2),
            STARSection("Task", "", 1),
            STARSection("Action", "", 2),
            STARSection("Result", "", 1),
        ]
    
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    content = file_path.read_text()
    sections = []
    
    # Default times for each section
    default_times = {
        "situation": 2,
        "task": 1,
        "action": 2,
        "result": 1,
    }
    
    # Split content by STAR section headers
    # Pattern matches: * SectionName: time or * SectionName
    section_pattern = r'\*\s*([^:]+)(?::\s*(\d+)m)?'
    
    lines = content.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        match = re.match(section_pattern, line, re.IGNORECASE)
        if match:
            # Save previous section if exists
            if current_section:
                section_name = current_section.lower().strip()
                time_minutes = default_times.get(section_name, 2)
                sections.append(STARSection(current_section, '\n'.join(current_content), time_minutes))
            
            # Start new section
            current_section = match.group(1).strip()
            time_str = match.group(2)
            if time_str:
                # Update default time for this section
                section_name = current_section.lower().strip()
                default_times[section_name] = int(time_str)
            current_content = []
        elif current_section and line.strip():
            current_content.append(line)
    
    # Add the last section
    if current_section:
        section_name = current_section.lower().strip()
        time_minutes = default_times.get(section_name, 2)
        sections.append(STARSection(current_section, '\n'.join(current_content), time_minutes))
    
    # If no sections found, create default ones
    if not sections:
        sections = [
            STARSection("Situation", "", default_times["situation"]),
            STARSection("Task", "", default_times["task"]),
            STARSection("Action", "", default_times["action"]),
            STARSection("Result", "", default_times["result"]),
        ]
    
    return sections


def create_progress_bar_app(section: STARSection, section_num: int, total_sections: int):
    """Create a prompt_toolkit application with progress bar."""
    
    # Create key bindings
    kb = KeyBindings()
    
    # Progress tracking
    progress = [0]  # Use list to allow modification in nested functions
    
    def update_progress():
        if progress[0] < section.time_seconds:
            progress[0] += 1
            return True
        return False
    
    @kb.add('q')
    def quit_app(event):
        """Quit the application."""
        event.app.exit()
    
    @kb.add('space')
    def pause_resume(event):
        """Pause/resume the timer."""
        # This could be enhanced with pause functionality
        pass
    
    # Create progress bar
    progress_bar = ProgressBar()
    
    # Create content display
    content_text = section.content if section.content else f"[No content provided for {section.name}]"
    content_display = FormattedTextControl(
        HTML(f"""
<ansiblue>📋 {section.name.upper()}</ansiblue>

<ansiyellow>Content:</ansiyellow>
{content_text}

<ansigreen>⏱️  Time: {section.time_minutes} minute{'s' if section.time_minutes != 1 else ''}</ansigreen>
        """)
    )
    
    # Create status display
    status_display = FormattedTextControl(
        HTML(f"<ansicyan>Section {section_num} of {total_sections}</ansicyan>")
    )
    
    # Create instructions
    instructions = FormattedTextControl(
        HTML("<ansiyellow>Press 'q' to quit, 'space' to pause/resume</ansiyellow>")
    )
    
    # Layout
    root_container = FloatContainer(
        content=HSplit([
            Window(content=status_display, height=1),
            Window(height=1),  # Spacer
            Window(content=content_display, height=D(min=10)),
            Window(height=1),  # Spacer
            Window(content=progress_bar, height=3),
            Window(height=1),  # Spacer
            Window(content=instructions, height=1),
        ]),
        floats=[
            Float(
                content=Window(
                    content=FormattedTextControl(
                        HTML(f"<ansired>Practice {section.name}...</ansired>")
                    ),
                    height=1
                ),
                top=0,
                right=0,
            )
        ]
    )
    
    layout = Layout(root_container)
    
    # Style
    style = Style.from_dict({
        'progress-bar': 'bg:#ansiblue #ansiwhite',
        'progress-bar.used': 'bg:#ansigreen',
    })
    
    # Create application
    app = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=True,
        mouse_support=True,
    )
    
    # Start timer
    def run_timer():
        while progress[0] < section.time_seconds:
            time.sleep(1)
            update_progress()
            # Update progress bar
            progress_bar.percentage = (progress[0] / section.time_seconds) * 100
            app.invalidate()
        app.exit()
    
    import threading
    timer_thread = threading.Thread(target=run_timer)
    timer_thread.daemon = True
    timer_thread.start()
    
    return app


def display_section_enhanced(section: STARSection, section_num: int, total_sections: int) -> None:
    """
    Display a STAR section with enhanced prompt_toolkit interface.
    
    Args:
        section: The STAR section to display
        section_num: Current section number
        total_sections: Total number of sections
    """
    if not PROMPT_TOOLKIT_AVAILABLE:
        # Fallback to basic display
        display_section_basic(section, section_num, total_sections)
        return
    
    try:
        app = create_progress_bar_app(section, section_num, total_sections)
        app.run()
        
        # Show completion message
        print(f"\n✅ {section.name} section complete!")
        
    except Exception as e:
        print(f"Error with enhanced display: {e}")
        # Fallback to basic display
        display_section_basic(section, section_num, total_sections)


def display_section_basic(section: STARSection, section_num: int, total_sections: int) -> None:
    """
    Basic display fallback when prompt_toolkit is not available.
    
    Args:
        section: The STAR section to display
        section_num: Current section number
        total_sections: Total number of sections
    """
    print(f"\nSection {section_num} of {total_sections}")
    print(f"📋 {section.name.upper()}")
    
    if section.content:
        print("─" * 60)
        print(section.content)
        print("─" * 60)
    else:
        print(f"[No content provided for {section.name}]")
    
    print(f"\n⏱️  Time: {section.time_minutes} minute{'s' if section.time_minutes != 1 else ''}")
    print()
    
    print(f"Practice {section.name}...")
    
    # Create progress bar
    for i in range(section.time_seconds + 1):
        remaining = section.time_seconds - i
        minutes = remaining // 60
        seconds = remaining % 60
        
        # Clear line and show progress
        print(f"\r{progress_bar_basic(i, section.time_seconds)} ⏱️ {minutes:02d}:{seconds:02d} remaining", end="", flush=True)
        
        if i < section.time_seconds:
            time.sleep(1)
    
    print()  # New line after progress
    print(f"✅ {section.name} section complete!")


def progress_bar_basic(current: int, total: int, width: int = 50) -> str:
    """Create a simple progress bar for fallback."""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(100 * current / total)
    return f"[{bar}] {percentage}%"


def print_banner():
    """Print the application banner."""
    if PROMPT_TOOLKIT_AVAILABLE:
        print("🌟 STAR Coach - Enhanced Interview Practice Tool")
        print("Get ready to practice your STAR answers with rich interface!\n")
    else:
        print("🌟 STAR Coach - Interview Practice Tool")
        print("Get ready to practice your STAR answers!\n")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="STAR Coach - Practice your STAR interview answers with timed sections."
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Path to .org or .txt file with STAR content"
    )
    parser.add_argument(
        "--basic", "-b",
        action="store_true",
        help="Use basic interface (disable prompt_toolkit)"
    )
    
    args = parser.parse_args()
    
    # Force basic mode if requested
    if args.basic:
        global PROMPT_TOOLKIT_AVAILABLE
        PROMPT_TOOLKIT_AVAILABLE = False
    
    try:
        print_banner()
        
        # Parse the file
        sections = parse_star_file(args.file)
        
        if args.file:
            print(f"📁 Loaded content from: {args.file}")
        else:
            print("📝 No file provided - practicing with empty sections")
        
        print(f"📊 Found {len(sections)} sections to practice")
        
        if PROMPT_TOOLKIT_AVAILABLE:
            print("🎨 Using enhanced interface with prompt_toolkit")
        else:
            print("📱 Using basic interface")
        
        print()
        
        # Practice each section
        for i, section in enumerate(sections, 1):
            display_section_enhanced(section, i, len(sections))
            
            if i < len(sections):
                if PROMPT_TOOLKIT_AVAILABLE:
                    input("\nPress Enter to continue to the next section...")
                else:
                    print("\nPress Enter to continue to the next section...")
                    input()
        
        print("\n🎉 Congratulations! You've completed your STAR practice session!")
        print("Great job practicing your interview skills!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 