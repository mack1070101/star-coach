#!/usr/bin/env python3
"""
STAR Coach - Enhanced CLI tool for practicing STAR interview answers with timed sections.
Uses prompt_toolkit for rich interactive experience with user controls.
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
    from prompt_toolkit.widgets import Label, Button
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
    Also extract a 'pre prompt' section if present.
    Returns:
        (pre_prompt, List of STARSection objects)
    """
    if file_path is None:
        # Return empty sections with default times
        return None, [
            STARSection("Situation", "", 2),
            STARSection("Task", "", 1),
            STARSection("Action", "", 2),
            STARSection("Result", "", 1),
        ]
    
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    content = file_path.read_text()
    sections = []
    pre_prompt = None
    
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
                if section_name == "pre prompt":
                    pre_prompt = '\n'.join(current_content).strip()
                else:
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
        if section_name == "pre prompt":
            pre_prompt = '\n'.join(current_content).strip()
        else:
            sections.append(STARSection(current_section, '\n'.join(current_content), time_minutes))
    
    # If no sections found, create default ones
    if not sections:
        sections = [
            STARSection("Situation", "", default_times["situation"]),
            STARSection("Task", "", default_times["task"]),
            STARSection("Action", "", default_times["action"]),
            STARSection("Result", "", default_times["result"]),
        ]
    
    return pre_prompt, sections


def create_progress_bar_app(section: STARSection, section_num: int, total_sections: int, pre_prompt: str = None):
    """Create a prompt_toolkit application with progress bar and user controls."""
    
    # Create key bindings
    kb = KeyBindings()
    
    # Progress tracking with control variables
    progress = [0]  # Use list to allow modification in nested functions
    paused = [False]
    quit_section = [False]
    restart_section = [False]
    restart_timer = [False]  # New: restart the entire timer
    quit_app = [False]
    
    def update_progress():
        if not paused[0] and progress[0] < section.time_seconds:
            progress[0] += 1
            return True
        return False
    
    @kb.add('q')
    @kb.add('Q')
    def quit_app_handler(event):
        """Quit the entire application."""
        quit_app[0] = True
        event.app.exit()
    
    @kb.add('r')
    @kb.add('R')
    def restart_timer_handler(event):
        """Restart the entire timer."""
        restart_timer[0] = True
        event.app.exit()
    
    @kb.add('up')
    @kb.add('k')  # Vim: k for up
    def restart_section_handler(event):
        """Restart the current section."""
        restart_section[0] = True
        event.app.exit()
    
    @kb.add('down')
    @kb.add('j')  # Vim: j for down
    def quit_section_handler(event):
        """Quit the current section."""
        quit_section[0] = True
        event.app.exit()
    
    @kb.add('left')
    @kb.add('h')  # Vim: h for left
    def skip_back_handler(event):
        """Skip back 5 seconds."""
        progress[0] = max(0, progress[0] - 5)
        event.app.invalidate()
    
    @kb.add('right')
    @kb.add('l')  # Vim: l for right
    def skip_forward_handler(event):
        """Skip forward 5 seconds."""
        progress[0] = min(section.time_seconds, progress[0] + 5)
        event.app.invalidate()
    
    @kb.add('space')
    def pause_resume_handler(event):
        """Pause/resume the timer."""
        paused[0] = not paused[0]
        event.app.invalidate()
    
    # Create progress bar
    def get_progress_text():
        percentage = int((progress[0] / section.time_seconds) * 100)
        filled = int(50 * progress[0] / section.time_seconds)
        bar = "█" * filled + "░" * (50 - filled)
        return f"[{bar}] {percentage}%"
    
    # Create time display
    def get_time_text():
        # Calculate elapsed and remaining time
        elapsed_minutes = progress[0] // 60
        elapsed_seconds = progress[0] % 60
        remaining_minutes = (section.time_seconds - progress[0]) // 60
        remaining_seconds = (section.time_seconds - progress[0]) % 60
        
        # Show "paused" instead of "elapsed" when paused
        time_label = "Paused" if paused[0] else "Elapsed"
        
        return f"{time_label}: {elapsed_minutes:02d}:{elapsed_seconds:02d} | Remaining: {remaining_minutes:02d}:{remaining_seconds:02d}"
    
    progress_display = FormattedTextControl(HTML(f"<ansigreen>{get_progress_text()}</ansigreen>"))
    time_display = FormattedTextControl(HTML(f"<ansigreen>{get_time_text()}</ansigreen>"))
    
    # Always show section title and time
    section_title_html = f"<ansiblue>📋 {section.name.upper()}</ansiblue>\n<ansigreen>⏱️  Time: {section.time_minutes} minute{'s' if section.time_minutes != 1 else ''}</ansigreen>"
    
    pre_prompt_html = f"<ansimagenta>{pre_prompt}</ansimagenta>\n\n" if pre_prompt else ""
    if section.content:
        content_lines = section.content.splitlines()
        content_html = f"{pre_prompt_html}{section_title_html}\n<ansiyellow>Content:</ansiyellow>\n{section.content}"
        content_height = D.exact((pre_prompt.count('\n') if pre_prompt else 0) + 3 + 1 + len(content_lines))
    else:
        content_html = f"{pre_prompt_html}{section_title_html}"
        content_height = D.exact((pre_prompt.count('\n') if pre_prompt else 0) + 3 + 1)
    content_display = FormattedTextControl(HTML(content_html))
    
    # Create controls display
    def get_controls_text():
        return f"""
<ansiyellow>Controls:</ansiyellow>
<ansigreen>↑/k</ansigreen> Restart Section  <ansigreen>↓/j</ansigreen> Quit Section
<ansigreen>←/h</ansigreen> Skip Back 5s     <ansigreen>→/l</ansigreen> Skip Forward 5s
<ansigreen>Space</ansigreen> Pause/Resume  <ansigreen>R</ansigreen> Restart Timer  <ansired>Q</ansired> Quit App
        """
    
    controls_display = FormattedTextControl(HTML(get_controls_text()))
    
    # Layout: progress bar with time display below it
    root_container = FloatContainer(
        content=HSplit([
            Window(content=content_display, height=content_height),
            Window(content=progress_display, height=1),
            Window(content=time_display, height=2),
            Window(content=controls_display, height=D(min=6, weight=1)),
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
        while progress[0] < section.time_seconds and not quit_section[0] and not restart_section[0] and not restart_timer[0] and not quit_app[0]:
            time.sleep(1)
            if not paused[0]:
                update_progress()
            # Update progress bar, time display, and controls
            progress_display.text = HTML(f"<ansigreen>{get_progress_text()}</ansigreen>")
            time_display.text = HTML(f"<ansigreen>{get_time_text()}</ansigreen>")
            controls_display.text = HTML(get_controls_text())
            app.invalidate()
        # Only call app.exit() if the app is still running
        if app.is_running:
            app.exit()
    
    import threading
    timer_thread = threading.Thread(target=run_timer)
    timer_thread.daemon = True
    timer_thread.start()
    
    return app, quit_section, restart_section, restart_timer, quit_app


def display_section_enhanced(section: STARSection, section_num: int, total_sections: int, pre_prompt: str = None) -> tuple[bool, bool, bool, bool]:
    """
    Display a STAR section with enhanced prompt_toolkit interface.
    Args:
        section: The STAR section to display
        section_num: Current section number
        total_sections: Total number of sections
        pre_prompt: Optional pre-prompt text to display at the top
    Returns:
        tuple: (quit_section, restart_section, restart_timer, quit_app)
    """
    if not PROMPT_TOOLKIT_AVAILABLE:
        display_section_basic(section, section_num, total_sections)
        return False, False, False, False
    try:
        app, quit_section, restart_section, restart_timer, quit_app = create_progress_bar_app(section, section_num, total_sections, pre_prompt=pre_prompt)
        try:
            app.run()
        except Exception as e:
            if e.__class__.__name__ == "NotEnoughSpaceError":
                pass
            else:
                raise
        was_quit = quit_section[0]
        was_restart = restart_section[0]
        was_restart_timer = restart_timer[0]
        was_app_quit = quit_app[0]
        if was_app_quit:
            print(f"\n👋 Application quit by user!")
            return False, False, False, True
        elif was_restart_timer:
            print(f"\n🔄 Timer restarted by user!")
            return False, False, True, False
        elif was_quit:
            print(f"\n⏭️  {section.name} section skipped!")
            return was_quit, was_restart, False, was_app_quit
        elif was_restart:
            print(f"\n🔄 {section.name} section restarted!")
            return display_section_enhanced(section, section_num, total_sections, pre_prompt=pre_prompt)
        else:
            print(f"\n✅ {section.name} section complete!")
            return was_quit, was_restart, False, was_app_quit
    except Exception as e:
        print(f"Error with enhanced display: {e}")
        display_section_basic(section, section_num, total_sections)
        return False, False, False, False


def display_section_basic(section: STARSection, section_num: int, total_sections: int) -> tuple[bool, bool, bool]:
    """
    Basic display fallback when prompt_toolkit is not available.
    
    Args:
        section: The STAR section to display
        section_num: Current section number
        total_sections: Total number of sections
        
    Returns:
        tuple: (quit_section, restart_section, quit_app)
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
    print("Controls: Press Ctrl+C to quit")
    
    # Create progress bar with time below
    for i in range(section.time_seconds + 1):
        remaining = section.time_seconds - i
        minutes = remaining // 60
        seconds = remaining % 60
        elapsed = i
        elapsed_minutes = elapsed // 60
        elapsed_seconds = elapsed % 60
        
        # Clear lines and show progress bar on first line, time on second line
        print(f"\r{progress_bar_basic(i, section.time_seconds)}", end="", flush=True)
        print(f"\nElapsed: {elapsed_minutes:02d}:{elapsed_seconds:02d} | Remaining: {minutes:02d}:{seconds:02d}", end="", flush=True)
        
        if i < section.time_seconds:
            time.sleep(1)
    
    print()  # New line after progress
    print(f"✅ {section.name} section complete!")
    return False, False, False


def progress_bar_basic(current: int, total: int, width: int = 50) -> str:
    """Create a simple progress bar for fallback."""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(100 * current / total)
    return f"[{bar}] {percentage}%"


def print_banner():
    print("🌟 STAR Coach - Interview Timer")
    print("Get ready to manage your STAR answers with a focused, timed interface!\n")


def press_any_key():
    """Wait for user to press any key."""
    try:
        import msvcrt  # Windows
        print("Press any key to continue...", end="", flush=True)
        msvcrt.getch()
        print()  # New line after key press
    except ImportError:
        try:
            import tty
            import termios
            import sys
            # Unix/Linux/macOS
            print("Press any key to continue...", end="", flush=True)
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            print()  # New line after key press
        except (ImportError, termios.error):
            # Fallback to input() if termios not available
            input("Press any key to continue...")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="STAR Coach - Interview timer for managing your STAR answers with timed sections."
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
    parser.add_argument(
        "--repeat", "-r",
        action="store_true",
        help="Repeat STAR sections in a loop until you quit"
    )
    
    args = parser.parse_args()
    
    # Force basic mode if requested
    if args.basic:
        global PROMPT_TOOLKIT_AVAILABLE
        PROMPT_TOOLKIT_AVAILABLE = False
    
    try:
        # Parse the file
        pre_prompt, sections = parse_star_file(args.file)
        
        if args.file:
            file_msg = f"📁 Loaded content from: {args.file}"
        else:
            file_msg = "📝 No file provided - using default STAR sections"
        
        section_count_msg = f"📊 {len(sections)} sections to time your answers"
        
        if PROMPT_TOOLKIT_AVAILABLE:
            interface_msg = "🎨 Using enhanced interface with prompt_toolkit and answer management controls"
        else:
            interface_msg = "📱 Using basic interface"
        
        # Timer for each section, with repeat mode
        def timer_once():
            for i, section in enumerate(sections, 1):
                print_banner()
                print(file_msg)
                print(section_count_msg)
                print(interface_msg)
                if pre_prompt:
                    print(pre_prompt + "\n")
                quit_section, restart_section, restart_timer, quit_app = display_section_enhanced(section, i, len(sections), pre_prompt=pre_prompt)
                
                # If app was quit, exit the loop
                if quit_app:
                    return True
                
                # If timer was restarted, restart the entire timer
                if restart_timer:
                    return "restart"  # Signal to restart entire timer
                
                # If section was quit, skip to next
                if quit_section:
                    continue
                
                # If section was restarted, don't advance to next section
                if restart_section:
                    i -= 1  # Stay on current section
                    continue
                
                if i < len(sections):
                    if PROMPT_TOOLKIT_AVAILABLE:
                        press_any_key()
                    else:
                        press_any_key()
            return False
        
        if args.repeat:
            while True:
                result = timer_once()
                if result == True:  # App was quit
                    break
                elif result == "restart":  # Timer was restarted
                    continue  # Continue loop to restart from beginning
                elif result == False:  # Timer completed normally
                    continue
            print("\n👋 Exited repeat mode. Interview timer stopped.")
        else:
            # Non-repeat mode: handle restart timer
            while True:
                result = timer_once()
                if result == True:  # App was quit
                    break
                elif result == "restart":  # Timer was restarted
                    continue  # Continue loop to restart from beginning
                elif result == False:  # Timer completed normally
                    break
            print("\n⏰ All sections complete! Interview timer finished.")
            print("You managed your STAR answers with precision!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 