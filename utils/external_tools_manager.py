"""
External Tools Manager
Manages external decompiler tools, downloads, and installations
"""

import os
import sys
import subprocess
import requests
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, DownloadColumn
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

class ExternalToolsManager:
    def __init__(self, console: Console):
        self.console = console
        self.col_neon = "#00ffcc"
        self.col_success = "#00e676"
        self.col_warn = "#ffab00"
        self.col_danger = "#ff1744"
        self.col_pink = "#ff6ec7"
        self.col_gold = "#ffd700"
        
        # Tools directory
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
        os.makedirs(self.tools_dir, exist_ok=True)
        
        # Tool configurations
        self.tools = {
            'cfr': {
                'name': 'CFR Java Decompiler',
                'url': 'https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar',
                'filename': 'cfr.jar',
                'type': 'jar',
                'description': 'Modern Java decompiler with excellent support',
                'size': '~10MB'
            },
            'procyon': {
                'name': 'Procyon Decompiler',
                'url': 'https://github.com/mstrobel/procyon/releases/download/v0.6.0/procyon-decompiler-0.6.0.jar',
                'filename': 'procyon.jar',
                'type': 'jar',
                'description': 'Advanced Java decompiler with lambda support',
                'size': '~3MB'
            },
            'fernflower': {
                'name': 'Fernflower',
                'url': 'https://github.com/JetBrains/intellij-community/raw/master/plugins/java-decompiler/engine/fernflower.jar',
                'filename': 'fernflower.jar',
                'type': 'jar',
                'description': 'IntelliJ IDEA built-in decompiler',
                'size': '~2MB'
            },
            'jdcore': {
                'name': 'JD-Core',
                'url': 'https://github.com/java-decompiler/jd-core/releases/download/v1.1.3/jd-core-1.1.3.jar',
                'filename': 'jd-core.jar',
                'type': 'jar',
                'description': 'Fast and reliable Java decompiler',
                'size': '~1MB'
            },
            'unluac': {
                'name': 'Unluac',
                'url': 'https://github.com/vi-k/unluac/releases/download/v2021.2/unluac-2021.2.jar',
                'filename': 'unluac.jar',
                'type': 'jar',
                'description': 'Lua 5.1/5.2 bytecode decompiler',
                'size': '~200KB'
            },
            'ghidra': {
                'name': 'Ghidra',
                'url': 'https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.4_build/ghidra_10.4_PUBLIC_20231108.zip',
                'filename': 'ghidra.zip',
                'type': 'zip',
                'description': 'NSA reverse engineering suite',
                'size': '~500MB'
            }
        }
    
    def _download_file(self, url: str, destination: str) -> bool:
        """Download file with progress bar"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with Progress(
                SpinnerColumn(style=f"bold {self.col_neon}"),
                TextColumn("[bold bright_white]{task.description}[/bold bright_white]"),
                BarColumn(bar_width=40, style=f"dim {self.col_blue}", complete_style=f"bold {self.col_neon}"),
                DownloadColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task(f"Downloading {os.path.basename(destination)}...", total=total_size)
                
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
            
            return True
        except Exception as e:
            self.console.print(f"[{self.col_danger}]✗ Download failed: {e}[/{self.col_danger}]")
            return False
    
    def _extract_archive(self, archive_path: str, extract_to: str) -> bool:
        """Extract ZIP or TAR archive"""
        try:
            if archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.endswith(('.tar.gz', '.tgz')):
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_to)
            elif archive_path.endswith('.tar'):
                with tarfile.open(archive_path, 'r') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                return False
            
            return True
        except Exception as e:
            self.console.print(f"[{self.col_danger}]✗ Extraction failed: {e}[/{self.col_danger}]")
            return False
    
    def check_tool_status(self) -> Dict[str, bool]:
        """Check status of all tools"""
        status = {}
        
        for tool_id, tool_config in self.tools.items():
            tool_path = os.path.join(self.tools_dir, tool_config['filename'])
            status[tool_id] = os.path.exists(tool_path)
        
        return status
    
    def display_tool_status(self):
        """Display comprehensive tool status"""
        status = self.check_tool_status()
        
        table = Table(
            title=f"[bold {self.col_pink}]External Tools Status[/bold {self.col_pink}]",
            box=box.ROUNDED,
            show_header=True,
            header_style=f"bold {self.col_gold}"
        )
        
        table.add_column("Tool", style=f"bold {self.col_cyan}", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Size", justify="center")
        table.add_column("Description", style=self.col_dim, justify="left")
        
        for tool_id, tool_config in self.tools.items():
            is_installed = status.get(tool_id, False)
            status_text = f"[{self.col_success}]✓ Installed[/{self.col_success}]" if is_installed else f"[{self.col_danger}]✗ Missing[/{self.col_danger}]"
            
            table.add_row(
                tool_config['name'],
                status_text,
                tool_config['size'],
                tool_config['description']
            )
        
        self.console.print("\\n")
        self.console.print(Align.center(table))
        self.console.print()
    
    def install_tool(self, tool_id: str) -> bool:
        """Install a specific tool"""
        if tool_id not in self.tools:
            self.console.print(f"[{self.col_danger}]✗ Unknown tool: {tool_id}[/{self.col_danger}]")
            return False
        
        tool_config = self.tools[tool_id]
        tool_path = os.path.join(self.tools_dir, tool_config['filename'])
        
        # Check if already installed
        if os.path.exists(tool_path):
            self.console.print(f"[{self.col_warn}]⚠ Tool {tool_config['name']} is already installed[/{self.col_warn}]")
            return True
        
        self.console.print(f"[{self.col_neon}]⚡ Installing {tool_config['name']}...[/{self.col_neon}]")
        
        # Download the tool
        temp_path = os.path.join(self.tools_dir, f"temp_{tool_id}")
        os.makedirs(temp_path, exist_ok=True)
        
        download_path = os.path.join(temp_path, os.path.basename(tool_config['url']))
        
        if not self._download_file(tool_config['url'], download_path):
            shutil.rmtree(temp_path, ignore_errors=True)
            return False
        
        # Handle different file types
        try:
            if tool_config['type'] == 'jar':
                # Move JAR file directly
                shutil.move(download_path, tool_path)
            elif tool_config['type'] == 'zip':
                # Extract ZIP archive
                if self._extract_archive(download_path, temp_path):
                    # Find and move the main executable
                    for root, dirs, files in os.walk(temp_path):
                        for file in files:
                            if file == tool_config['filename']:
                                shutil.move(os.path.join(root, file), tool_path)
                                break
            else:
                self.console.print(f"[{self.col_danger}]✗ Unsupported file type: {tool_config['type']}[/{self.col_danger}]")
                shutil.rmtree(temp_path, ignore_errors=True)
                return False
            
            # Clean up
            shutil.rmtree(temp_path, ignore_errors=True)
            
            self.console.print(f"[{self.col_success}]✓ {tool_config['name']} installed successfully![/{self.col_success}]")
            return True
            
        except Exception as e:
            self.console.print(f"[{self.col_danger}]✗ Installation failed: {e}[/{self.col_danger}]")
            shutil.rmtree(temp_path, ignore_errors=True)
            return False
    
    def install_all_tools(self) -> bool:
        """Install all available tools"""
        self.console.print(f"[{self.col_neon}]⚡ Installing all external tools...[/{self.col_neon}]")
        
        success_count = 0
        total_count = len(self.tools)
        
        for tool_id in self.tools:
            if self.install_tool(tool_id):
                success_count += 1
        
        self.console.print(f"\\n[{self.col_success}]✓ Installed {success_count}/{total_count} tools successfully![/{self.col_success}]")
        return success_count == total_count
    
    def uninstall_tool(self, tool_id: str) -> bool:
        """Uninstall a specific tool"""
        if tool_id not in self.tools:
            self.console.print(f"[{self.col_danger}]✗ Unknown tool: {tool_id}[/{self.col_danger}]")
            return False
        
        tool_config = self.tools[tool_id]
        tool_path = os.path.join(self.tools_dir, tool_config['filename'])
        
        if not os.path.exists(tool_path):
            self.console.print(f"[{self.col_warn}]⚠ Tool {tool_config['name']} is not installed[/{self.col_warn}]")
            return True
        
        try:
            os.remove(tool_path)
            self.console.print(f"[{self.col_success}]✓ {tool_config['name']} uninstalled successfully![/{self.col_success}]")
            return True
        except Exception as e:
            self.console.print(f"[{self.col_danger}]✗ Uninstallation failed: {e}[/{self.col_danger}]")
            return False
    
    def update_tool(self, tool_id: str) -> bool:
        """Update a specific tool"""
        if self.uninstall_tool(tool_id):
            return self.install_tool(tool_id)
        return False
    
    def get_tool_path(self, tool_id: str) -> Optional[str]:
        """Get the path to a tool executable"""
        if tool_id not in self.tools:
            return None
        
        tool_config = self.tools[tool_id]
        tool_path = os.path.join(self.tools_dir, tool_config['filename'])
        
        if os.path.exists(tool_path):
            return tool_path
        
        return None
    
    def run_tool_manager(self):
        """Run the interactive tool manager"""
        from rich.prompt import Prompt, Confirm
        
        while True:
            self.console.print()
            self.console.print(Align.center(Panel(
                f"[bold {self.col_neon}]⚡ EXTERNAL TOOLS MANAGER ⚡[/bold {self.col_neon}]\\n\\n"
                f"[{self.col_dim}]Manage external decompiler tools and dependencies\\n"
                f"Download, install, and update tools automatically[/{self.col_dim}]",
                border_style=self.col_neon,
                box=box.ROUNDED,
                padding=(1, 4)
            )))
            
            # Display tool status
            self.display_tool_status()
            
            # Menu options
            self.console.print(f"[{self.col_neon}]Available options:[/{self.col_neon}]")
            self.console.print(f"  1. Install all tools")
            self.console.print(f"  2. Install specific tool")
            self.console.print(f"  3. Update tool")
            self.console.print(f"  4. Uninstall tool")
            self.console.print(f"  5. Refresh status")
            self.console.print(f"  q. Quit")
            
            choice = Prompt.ask(f"\\n[{self.col_neon}]Select option[/{self.col_neon}]").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                if Confirm.ask(f"[{self.col_warn}]Install all available tools? This may take a while.[/{self.col_warn}]"):
                    self.install_all_tools()
            elif choice == '2':
                self.console.print(f"[{self.col_neon}]Available tools:[/{self.col_neon}]")
                for i, tool_id in enumerate(self.tools.keys(), 1):
                    tool_config = self.tools[tool_id]
                    self.console.print(f"  {i}. {tool_config['name']}")
                
                tool_choice = Prompt.ask(f"[{self.col_neon}]Select tool to install[/{self.col_neon}]")
                try:
                    tool_index = int(tool_choice) - 1
                    tool_ids = list(self.tools.keys())
                    if 0 <= tool_index < len(tool_ids):
                        self.install_tool(tool_ids[tool_index])
                    else:
                        self.console.print(f"[{self.col_danger}]✗ Invalid choice[/{self.col_danger}]")
                except ValueError:
                    self.console.print(f"[{self.col_danger}]✗ Invalid input[/{self.col_danger}]")
            elif choice == '3':
                # Similar implementation for update
                pass
            elif choice == '4':
                # Similar implementation for uninstall
                pass
            elif choice == '5':
                continue
            else:
                self.console.print(f"[{self.col_danger}]✗ Invalid choice[/{self.col_danger}]")
