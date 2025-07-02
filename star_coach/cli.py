"""
STAR Coach CLI - Practice STAR interview answers with timed sections.
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()
console = Console()


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
        raise typer.BadParameter(f"File not found: {file_path}")
    
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


def display_section(section: STARSection) -> None:
    """
    Display a STAR section with content and progress bar.
    
    Args:
        section: The STAR section to display
    """
    console.print(f"\n[bold blue]📋 {section.name.upper()}[/bold blue]")
    
    if section.content:
        # Display content in a panel
        content_text = Text(section.content, style="white")
        panel = Panel(content_text, title=f"{section.name} Content", border_style="blue")
        console.print(panel)
    else:
        console.print(f"[italic]No content provided for {section.name}[/italic]")
    
    console.print(f"\n[bold green]⏱️  Time: {section.time_minutes} minute{'s' if section.time_minutes != 1 else ''}[/bold green]")
    
    # Create progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Practice {section.name}...", 
            total=section.time_seconds
        )
        
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)
    
    console.print(f"[bold green]✅ {section.name} section complete![/bold green]")


@app.command()
def main(
    file: Optional[Path] = typer.Option(
        None, 
        "--file", "-f", 
        help="Path to .org or .txt file with STAR content"
    )
):
    """
    STAR Coach - Practice your STAR interview answers with timed sections.
    
    Reads a file with STAR format and guides you through timed practice sessions.
    """
    try:
        console.print("[bold yellow]🌟 STAR Coach - Interview Practice Tool[/bold yellow]")
        console.print("[italic]Get ready to practice your STAR answers![/italic]\n")
        
        # Parse the file
        sections = parse_star_file(file)
        
        if file:
            console.print(f"[green]📁 Loaded content from: {file}[/green]")
        else:
            console.print("[yellow]📝 No file provided - practicing with empty sections[/yellow]")
        
        console.print(f"[blue]📊 Found {len(sections)} sections to practice[/blue]\n")
        
        # Practice each section
        for i, section in enumerate(sections, 1):
            console.print(f"[bold]Section {i} of {len(sections)}[/bold]")
            display_section(section)
            
            if i < len(sections):
                console.print("\n[bold]Press Enter to continue to the next section...[/bold]")
                input()
        
        console.print("\n[bold green]🎉 Congratulations! You've completed your STAR practice session![/bold green]")
        console.print("[italic]Great job practicing your interview skills![/italic]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app() 