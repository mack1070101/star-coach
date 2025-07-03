"""
STAR Coach - Interview timer for managing your STAR answers with timed sections.

A CLI tool that helps you practice and time your STAR (Situation, Task, Action, Result)
interview answers with an interactive, timed interface.
"""

__version__ = "2.1.0"
__author__ = "Mackenzie Bligh"
__email__ = "mackenziebligh@gmail.com"

from .cli import main

__all__ = ["main"] 