#!/usr/bin/env python3
"""
STAR Coach - Standalone version
A CLI tool for practicing STAR interview answers with timed sections.
This version uses only standard library modules for maximum compatibility.
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import List, Optional


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


def print_banner():
    """Print the application banner."""
    print("🌟 STAR Coach - Interview Practice Tool")
    print("Get ready to practice your STAR answers!\n")


def print_section_header(section: STARSection, section_num: int, total_sections: int):
    """Print a section header."""
    print(f"Section {section_num} of {total_sections}")
    print(f"📋 {section.name.upper()}")
    
    if section.content:
        print("─" * 60)
        print(section.content)
        print("─" * 60)
    else:
        print(f"[No content provided for {section.name}]")
    
    print(f"\n⏱️  Time: {section.time_minutes} minute{'s' if section.time_minutes != 1 else ''}")
    print()


def progress_bar(current: int, total: int, width: int = 50) -> str:
    """Create a simple progress bar."""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(100 * current / total)
    return f"[{bar}] {percentage}%"


def display_section(section: STARSection) -> None:
    """
    Display a STAR section with content and progress bar.
    
    Args:
        section: The STAR section to display
    """
    print(f"Practice {section.name}...")
    
    # Create progress bar
    for i in range(section.time_seconds + 1):
        remaining = section.time_seconds - i
        minutes = remaining // 60
        seconds = remaining % 60
        
        # Clear line and show progress
        print(f"\r{progress_bar(i, section.time_seconds)} ⏱️ {minutes:02d}:{seconds:02d} remaining", end="", flush=True)
        
        if i < section.time_seconds:
            time.sleep(1)
    
    print()  # New line after progress
    print(f"✅ {section.name} section complete!")


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
    
    args = parser.parse_args()
    
    try:
        print_banner()
        
        # Parse the file
        sections = parse_star_file(args.file)
        
        if args.file:
            print(f"📁 Loaded content from: {args.file}")
        else:
            print("📝 No file provided - practicing with empty sections")
        
        print(f"📊 Found {len(sections)} sections to practice\n")
        
        # Practice each section
        for i, section in enumerate(sections, 1):
            print_section_header(section, i, len(sections))
            display_section(section)
            
            if i < len(sections):
                print("\nPress Enter to continue to the next section...")
                input()
        
        print("\n🎉 Congratulations! You've completed your STAR practice session!")
        print("Great job practicing your interview skills!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 