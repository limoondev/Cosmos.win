#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║              C O S M O S . W I N  v5.0                ║
║     Cybersecurity Terminal — Galaxy Edition            ║
║     44 Modules  |  11 API Integrations  |  Enhanced UI║
╚═══════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import threading
import ctypes

# Ensure we're on Windows for transparency support
if sys.platform != "win32":
    print("Cosmos.win requires Windows.")
    sys.exit(1)

from utils.window import set_terminal_transparent, set_terminal_title, maximize_terminal
from utils.ui import CosmosUI

def main():
    set_terminal_title("✦ COSMOS.WIN ─ Cybersecurity Terminal ✦")
    maximize_terminal()
    set_terminal_transparent(210)  # 0=invisible, 255=opaque

    app = CosmosUI()
    app.run()

if __name__ == "__main__":
    # Check admin
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        print("\033[93m[!] Relaunching as Administrator for full functionality...\033[0m")
        time.sleep(1)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join([f'"{a}"' for a in sys.argv]), None, 1
        )
        sys.exit(0)

    main()
