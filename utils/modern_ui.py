"""
Modern UI Enhancement System
Ultra-modern interface components with animations and effects
"""

import os
import time
import random
import math
from typing import List, Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.tree import Tree
from rich.rule import Rule
from rich.markdown import Markdown

class ModernUI:
    def __init__(self, console: Console):
        self.console = console
        self.animation_frame = 0
        
        # Enhanced color palette
        self.colors = {
            'primary': '#00ffcc',      # Neon cyan
            'secondary': '#ff6ec7',    # Neon pink
            'accent': '#bb86fc',       # Purple
            'success': '#00e676',      # Green
            'warning': '#ffab00',      # Amber
            'danger': '#ff1744',       # Red
            'info': '#4fc3f7',         # Blue
            'gold': '#ffd700',         # Gold
            'dim': 'bright_black',     # Dim gray
            'bright': 'bright_white'   # Bright white
        }
        
        # Animation patterns
        self.patterns = ['⚡', '✦', '◆', '●', '■', '▲', '⬟', '⬢']
        self.loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def create_animated_header(self, title: str, subtitle: str = "") -> Panel:
        """Create animated header with dynamic effects"""
        # Animated pattern
        pattern = self.patterns[self.animation_frame % len(self.patterns)]
        
        header_content = f"""[bold {self.colors['primary']}] {pattern} {title} {pattern} [/bold {self.colors['primary']}]
        
{self.colors['dim']}{subtitle}[/{self.colors['dim']}]"""
        
        return Panel(
            Align.center(Text.from_markup(header_content)),
            border_style=self.colors['primary'],
            box=box.DOUBLE,
            padding=(1, 3)
        )
    
    def create_modern_menu(self, title: str, items: List[Tuple[str, str, str]], 
                          current_page: int = 0, total_pages: int = 1) -> Panel:
        """Create modern menu with enhanced styling"""
        content = []
        
        # Menu title with animation
        pattern = self.patterns[self.animation_frame % len(self.patterns)]
        content.append(f"[bold {self.colors['primary']}] {pattern} {title} {pattern} [/bold {self.colors['primary']}]\n")
        
        # Menu items
        for key, name, description in items:
            # Alternating colors for better readability
            item_color = self.colors['info'] if int(key) % 2 == 0 else self.colors['accent']
            content.append(f"[{item_color}]{key}.[/bold {item_color}] [bold]{name}[/bold]")
            content.append(f"   {self.colors['dim']}{description}[/{self.colors['dim']}]")
            content.append("")
        
        # Page indicator
        if total_pages > 1:
            page_info = f"[{self.colors['gold']}]Page {current_page + 1}/{total_pages}[/{self.colors['gold']}]"
            content.append(f"\n{Align.center(Text.from_markup(page_info))}")
        
        return Panel(
            "\n".join(content),
            border_style=self.colors['primary'],
            box=box.ROUNDED,
            padding=(1, 3)
        )
    
    def create_status_dashboard(self, stats: Dict[str, any]) -> Panel:
        """Create modern status dashboard with metrics"""
        # Create metrics table
        table = Table(
            title=f"[bold {self.colors['secondary']}]System Status[/bold {self.colors['secondary']}]",
            box=box.ROUNDED,
            show_header=True,
            header_style=f"bold {self.colors['gold']}"
        )
        
        table.add_column("Metric", style=f"bold {self.colors['info']}", justify="left")
        table.add_column("Value", style=f"bold {self.colors['primary']}", justify="right")
        table.add_column("Status", justify="center")
        
        # Add stats with status indicators
        for key, value in stats.items():
            # Determine status
            if isinstance(value, (int, float)):
                if value > 0:
                    status = f"[{self.colors['success']}]●[/]"
                else:
                    status = f"[{self.colors['dim']}]○[/]"
            else:
                status = f"[{self.colors['info']}]◐[/]"
            
            # Format value
            if isinstance(value, (int, float)):
                if value > 1000000:
                    formatted_value = f"{value/1000000:.1f}M"
                elif value > 1000:
                    formatted_value = f"{value/1000:.1f}K"
                else:
                    formatted_value = str(value)
            else:
                formatted_value = str(value)[:20] + ("..." if len(str(value)) > 20 else "")
            
            table.add_row(
                key.replace('_', ' ').title(),
                formatted_value,
                status
            )
        
        return table
    
    def create_progress_section(self, tasks: List[Tuple[str, int, int]]) -> Panel:
        """Create modern progress section with multiple progress bars"""
        content = []
        
        for task_name, current, total in tasks:
            percentage = (current / total) * 100 if total > 0 else 0
            
            # Progress bar
            bar_length = 30
            filled = int((bar_length * percentage) / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            # Color based on percentage
            if percentage >= 80:
                bar_color = self.colors['success']
            elif percentage >= 50:
                bar_color = self.colors['warning']
            else:
                bar_color = self.colors['danger']
            
            content.append(f"[{self.colors['info']}] {task_name} [/{self.colors['info']}]")
            content.append(f"[{bar_color}]{bar}[/{bar_color}] {percentage:.1f}%")
            content.append("")
        
        return Panel(
            "\n".join(content),
            title=f"[bold {self.colors['primary']}]Progress[/bold {self.colors['primary']}]",
            border_style=self.colors['primary'],
            box=box.ROUNDED,
            padding=(1, 2)
        )
    
    def create_feature_grid(self, features: List[Tuple[str, str, str]]) -> Panel:
        """Create modern feature grid with icons"""
        # Create columns for feature display
        columns = []
        
        for icon, title, description in features:
            feature_text = f"""[bold {self.colors['primary']}]{icon}[/bold {self.colors['primary']}]
[bold {self.colors['info']}]{title}[/bold {self.colors['info']}]
{self.colors['dim']}{description}[/{self.colors['dim']}]"""
            
            feature_panel = Panel(
                Text.from_markup(feature_text),
                border_style=self.colors['accent'],
                box=box.ROUNDED,
                padding=(1, 2)
            )
            columns.append(feature_panel)
        
        # Arrange in columns (3 per row)
        rows = []
        for i in range(0, len(columns), 3):
            row = Columns(columns[i:i+3], equal=True, expand=True)
            rows.append(row)
        
        content = "\n".join([str(row) for row in rows])
        
        return Panel(
            Text.from_markup(content),
            title=f"[bold {self.colors['secondary']}]Features[/bold {self.colors['secondary']}]",
            border_style=self.colors['secondary'],
            box=box.ROUNDED,
            padding=(1, 2)
        )
    
    def create_animated_loading(self, message: str) -> str:
        """Create animated loading message"""
        char = self.loading_chars[self.animation_frame % len(self.loading_chars)]
        return f"[{self.colors['primary']}]{char}[/{self.colors['primary']}] {message}"
    
    def create_notification(self, message: str, notification_type: str = "info") -> Panel:
        """Create modern notification with appropriate styling"""
        type_config = {
            'success': {'color': self.colors['success'], 'icon': '✓', 'style': 'bold'},
            'warning': {'color': self.colors['warning'], 'icon': '⚠', 'style': 'bold'},
            'error': {'color': self.colors['danger'], 'icon': '✗', 'style': 'bold'},
            'info': {'color': self.colors['info'], 'icon': 'ℹ', 'style': 'bold'}
        }
        
        config = type_config.get(notification_type, type_config['info'])
        
        content = f"[{config['color']}]{config['icon']} {message}[/{config['color']}]"
        
        return Panel(
            Align.center(Text.from_markup(content)),
            border_style=config['color'],
            box=box.ROUNDED,
            padding=(0, 2)
        )
    
    def create_command_palette(self, commands: List[Tuple[str, str, str]]) -> Panel:
        """Create modern command palette"""
        content = []
        
        for key, command, description in commands:
            content.append(f"[{self.colors['primary']}] {key} [/]")
            content.append(f"[bold]{command}[/bold]")
            content.append(f"{self.colors['dim']}{description}[/{self.colors['dim']}]")
            content.append("")
        
        return Panel(
            "\n".join(content),
            title=f"[bold {self.colors['gold']}]Command Palette[/bold {self.colors['gold']}]",
            border_style=self.colors['gold'],
            box=box.ROUNDED,
            padding=(1, 2)
        )
    
    def create_tool_comparison(self, tools: List[Dict]) -> Panel:
        """Create modern tool comparison table"""
        table = Table(
            title=f"[bold {self.colors['secondary']}]Tool Comparison[/bold {self.colors['secondary']}]",
            box=box.ROUNDED,
            show_header=True,
            header_style=f"bold {self.colors['gold']}"
        )
        
        table.add_column("Tool", style=f"bold {self.colors['info']}", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Performance", justify="center")
        table.add_column("Features", justify="left")
        
        for tool in tools:
            # Status indicator
            status = tool.get('status', 'unknown')
            if status == 'available':
                status_display = f"[{self.colors['success']}]● Ready[/]"
            elif status == 'missing':
                status_display = f"[{self.colors['danger']}]✗ Missing[/]"
            else:
                status_display = f"[{self.colors['warning']}]◐ Unknown[/]"
            
            # Performance indicator
            performance = tool.get('performance', 0)
            if performance >= 80:
                perf_display = f"[{self.colors['success']}]⚡ Fast[/]"
            elif performance >= 50:
                perf_display = f"[{self.colors['warning']}]⚡ Medium[/]"
            else:
                perf_display = f"[{self.colors['danger']}]⚡ Slow[/]"
            
            # Features
            features = tool.get('features', [])[:3]
            features_display = ", ".join(features)
            
            table.add_row(
                tool.get('name', 'Unknown'),
                status_display,
                perf_display,
                features_display
            )
        
        return table
    
    def update_animation(self):
        """Update animation frame"""
        self.animation_frame = (self.animation_frame + 1) % 100
    
    def create_welcome_screen(self, app_name: str, version: str, description: str) -> Panel:
        """Create modern welcome screen"""
        ascii_art = """
    ╔═════════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ⚡ COSMOS.WIN - PREMIUM CYBERSECURITY SUITE ⚡          ║
    ║                                                           ║
    ╚═════════════════════════════════════════════════════════════
        """
        
        content = f"""[bold {self.colors['primary']}]{ascii_art}[/bold {self.colors['primary']}]

[bold {self.colors['gold']}]Version: {version}[/bold {self.colors['gold']}]

{self.colors['dim']}{description}[/{self.colors['dim']}]"""
        
        return Panel(
            Align.center(Text.from_markup(content)),
            border_style=self.colors['primary'],
            box=box.DOUBLE,
            padding=(1, 2)
        )
    
    def create_error_screen(self, error_message: str, error_details: str = "") -> Panel:
        """Create modern error screen"""
        content = f"""[bold {self.colors['danger']}]✗ ERROR[/bold {self.colors['danger']}]

{self.colors['bright']}{error_message}[/{self.colors['bright']}]"""
        
        if error_details:
            content += f"\n\n{self.colors['dim']}{error_details}[/{self.colors['dim']}]"
        
        return Panel(
            Align.center(Text.from_markup(content)),
            border_style=self.colors['danger'],
            box=box.ROUNDED,
            padding=(1, 3)
        )
