"""
Tests for STAR file parsing functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from star_coach.cli import parse_star_file, STARSection


class TestSTARSection:
    """Test STARSection class."""
    
    def test_star_section_creation(self):
        """Test creating a STAR section."""
        section = STARSection("Situation", "Test content", 2)
        assert section.name == "Situation"
        assert section.content == "Test content"
        assert section.time_minutes == 2
        assert section.time_seconds == 120


class TestParseStarFile:
    """Test parse_star_file function."""
    
    def test_parse_no_file(self):
        """Test parsing when no file is provided."""
        sections = parse_star_file(None)
        
        assert len(sections) == 4
        assert sections[0].name == "Situation"
        assert sections[0].time_minutes == 2
        assert sections[1].name == "Task"
        assert sections[1].time_minutes == 1
        assert sections[2].name == "Action"
        assert sections[2].time_minutes == 2
        assert sections[3].name == "Result"
        assert sections[3].time_minutes == 1
    
    def test_parse_file_not_found(self):
        """Test parsing when file doesn't exist."""
        with pytest.raises(Exception):
            parse_star_file(Path("nonexistent.org"))
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_parse_basic_star_file(self, mock_read_text, mock_exists):
        """Test parsing a basic STAR file."""
        mock_exists.return_value = True
        mock_read_text.return_value = """
* Situation

- I was working on a project with tight deadlines

* Task

- I needed to coordinate with multiple teams

* Action

- I created a detailed timeline and held daily standups

* Result

- We delivered the project on time and under budget
"""
        
        sections = parse_star_file(Path("test.org"))
        
        assert len(sections) == 4
        assert sections[0].name == "Situation"
        assert "tight deadlines" in sections[0].content
        assert sections[0].time_minutes == 2  # default
        
        assert sections[1].name == "Task"
        assert "coordinate with multiple teams" in sections[1].content
        assert sections[1].time_minutes == 1  # default
        
        assert sections[2].name == "Action"
        assert "daily standups" in sections[2].content
        assert sections[2].time_minutes == 2  # default
        
        assert sections[3].name == "Result"
        assert "on time and under budget" in sections[3].content
        assert sections[3].time_minutes == 1  # default
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_parse_with_custom_times(self, mock_read_text, mock_exists):
        """Test parsing a STAR file with custom timing."""
        mock_exists.return_value = True
        mock_read_text.return_value = """
* Situation: 3m

- Complex project scenario

* Task: 2m

- Multiple responsibilities

* Action: 4m

- Detailed implementation steps

* Result: 1m

- Measurable outcomes
"""
        
        sections = parse_star_file(Path("test.org"))
        
        assert len(sections) == 4
        assert sections[0].name == "Situation"
        assert sections[0].time_minutes == 3
        
        assert sections[1].name == "Task"
        assert sections[1].time_minutes == 2
        
        assert sections[2].name == "Action"
        assert sections[2].time_minutes == 4
        
        assert sections[3].name == "Result"
        assert sections[3].time_minutes == 1
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_parse_mixed_timing(self, mock_read_text, mock_exists):
        """Test parsing with some sections having custom times and others using defaults."""
        mock_exists.return_value = True
        mock_read_text.return_value = """
* Situation: 5m

- Very complex situation

* Task

- Standard task description

* Action: 3m

- Detailed actions taken

* Result

- Final outcomes
"""
        
        sections = parse_star_file(Path("test.org"))
        
        assert len(sections) == 4
        assert sections[0].name == "Situation"
        assert sections[0].time_minutes == 5  # custom
        
        assert sections[1].name == "Task"
        assert sections[1].time_minutes == 1  # default
        
        assert sections[2].name == "Action"
        assert sections[2].time_minutes == 3  # custom
        
        assert sections[3].name == "Result"
        assert sections[3].time_minutes == 1  # default
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_parse_empty_file(self, mock_read_text, mock_exists):
        """Test parsing an empty file."""
        mock_exists.return_value = True
        mock_read_text.return_value = ""
        
        sections = parse_star_file(Path("empty.org"))
        
        # Should return default sections
        assert len(sections) == 4
        assert sections[0].name == "Situation"
        assert sections[0].time_minutes == 2
        assert sections[0].content == ""
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_parse_case_insensitive(self, mock_read_text, mock_exists):
        """Test that section names are case insensitive."""
        mock_exists.return_value = True
        mock_read_text.return_value = """
* SITUATION: 3m

- Test content

* task: 2m

- More content

* Action

- Action content

* RESULT: 1m

- Result content
"""
        
        sections = parse_star_file(Path("test.org"))
        
        assert len(sections) == 4
        assert sections[0].name == "SITUATION"
        assert sections[0].time_minutes == 3
        
        assert sections[1].name == "task"
        assert sections[1].time_minutes == 2
        
        assert sections[2].name == "Action"
        assert sections[2].time_minutes == 2  # default
        
        assert sections[3].name == "RESULT"
        assert sections[3].time_minutes == 1 