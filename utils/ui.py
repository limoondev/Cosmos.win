"""
Cosmos.win - Galaxy-themed terminal UI engine v5.0
Rich-powered paginated menu with encrypted API key manager, license gate,
search, live dashboard stats, favorites, and beautiful ASCII art.
"""

import os
import sys
import time
import random
import importlib
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.prompt import Prompt
from rich.style import Style
from rich.columns import Columns
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn,
)

# ── Neon-Cyber colour palette ────────────────────────────────────────────
COL_BG       = "#0d1117"
COL_STAR     = "bright_white"
COL_NEON     = "#00ffcc"        # Primary neon teal
COL_CYAN     = "bright_cyan"
COL_PINK     = "#ff6ec7"        # Neon pink accent
COL_BLUE     = "#4fc3f7"        # Soft blue
COL_PURPLE   = "#bb86fc"        # Neon purple
COL_GOLD     = "#ffd700"        # Gold highlights
COL_DIM      = "bright_black"
COL_SUCCESS  = "#00e676"
COL_WARN     = "#ffab00"
COL_DANGER   = "#ff1744"
COL_ORANGE   = "#ff9100"
COL_WHITE    = "bright_white"
COL_LIME     = "#b2ff59"
COL_TEAL     = "#00bfa5"
COL_INDIGO   = "#7c4dff"

# ── Large ASCII art logo ────────────────────────────────────────────────
LOGO_ART = r"""
  ██████╗ ██████╗  ██████╗ ███╗   ███╗ ██████╗  ██████╗    ██╗    ██╗██╗███╗   ██╗
 ██╔════╝██╔═══██╗██╔════╝ ████╗ ████║██╔═══██╗██╔════╝    ██║    ██║██║████╗  ██║
 ██║     ██║   ██║╚█████╗  ██╔████╔██║██║   ██║╚█████╗     ██║ █╗ ██║██║██╔██╗ ██║
 ██║     ██║   ██║ ╚═══██╗ ██║╚██╔╝██║██║   ██║ ╚═══██╗    ██║███╗██║██║██║╚██╗██║
 ╚██████╗╚██████╔╝██████╔╝ ██║ ╚═╝ ██║╚██████╔╝██████╔╝    ╚███╔███╔╝██║██║ ╚████║
  ╚═════╝ ╚═════╝ ╚═════╝  ╚═╝     ╚═╝ ╚═════╝ ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
"""

# ── Smaller sub-logo for menu screens ───────────────────────────────────
LOGO_MINI = r"""
 ██████╗  ██████╗  ██████╗ ███╗   ███╗ ██████╗  ██████╗   ██╗    ██╗██╗███╗   ██╗
██╔════╝ ██╔═══██╗██╔════╝ ████╗ ████║██╔═══██╗██╔════╝   ██║    ██║██║████╗  ██║
██║      ██║   ██║╚█████╗  ██╔████╔██║██║   ██║╚█████╗    ██║ █╗ ██║██║██╔██╗ ██║
╚██████╗ ╚██████╔╝██████╔╝ ██║ ╚═╝ ██║╚██████╔╝██████╔╝   ╚███╔███╔╝██║██║ ╚████║
 ╚═════╝  ╚═════╝ ╚═════╝  ╚═╝     ╚═╝ ╚═════╝ ╚═════╝     ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
"""

TAGLINE = "Cosmos.win, Multi-Tools by @limoons"
VERSION = "v6.0.0"

STARS = ["✦"]
NEON_STARS = ["✦"]

# ── 44 modules in 6 pages + API Key Manager ─────────────────────────────
PAGES = [
    {
        "title": "THREAT DETECTION & REMOVAL",
        "icon": "✦",
        "color": COL_DANGER,
        "accent": COL_ORANGE,
        "items": [
            ("1",  "✦ Luckyware Scanner",       "Scan processes & files for malware signatures + VirusTotal API"),
            ("2",  "✦ Ransomware Remover",   "Detect & neutralize ransomware activity + auto-quarantine"),
            ("3",  "✦ Rootkit Detector",        "Deep scan for hidden rootkits & stealth malware"),
            ("4",  "✦ Crypto Miner Detector","Detect hidden cryptocurrency miners + resource analysis"),
            ("5",  "✦ Keylogger Detector",   "Find keyloggers & input-capture threats + hook analysis"),
            ("6",  "✦ DLL Hijack Scanner",      "Scan for DLL hijacking vulnerabilities + path validation"),
            ("7",  "✦ Malware Sandbox",         "PE analysis, packer detection & multi-sandbox submission"),
            ("8",  "✦ Boot Guard",       "Boot integrity, Secure Boot & bootkit detection"),
        ],
    },
    {
        "title": "NETWORK & CONNECTIVITY",
        "icon": "✦",
        "color": COL_BLUE,
        "accent": COL_CYAN,
        "items": [
            ("9",  "✦ Network Scanner",          "ARP scan, port scan, device fingerprinting + Shodan"),
            ("10", "✦ Packet Sniffer",           "Capture & analyze network packets with protocol decode"),
            ("11", "✦ WiFi Analyzer",            "Scan & audit nearby Wi-Fi networks + signal mapping"),
            ("12", "✦ DNS Blocker",              "Block ads/trackers via DNS + custom blocklists"),
            ("13", "✦ IP Geolocation",    "Geolocate IPs with IPinfo, ip-api & threat enrichment"),
            ("14", "✦ SSL Scanner",              "Audit SSL/TLS certs, ciphers & certificate transparency"),
            ("15", "✦ Honeypot Detector",        "Detect honeypots & decoy services on the network"),
            ("16", "✦ Traceroute Mapper", "Visual traceroute with geo, ASN & anomaly detection"),
            ("17", "✦ Bandwidth Monitor",        "Real-time bandwidth, per-process usage & speed test"),
        ],
    },
    {
        "title": "SYSTEM & PROCESS MANAGEMENT",
        "icon": "✦",
        "color": COL_PURPLE,
        "accent": COL_INDIGO,
        "items": [
            ("18", "✦ Process Manager",          "Live process viewer with kill, inject detect & tree"),
            ("19", "✦ Service Auditor",          "Audit & manage Windows services + auto-start analysis"),
            ("20", "✦ Scheduled Task Auditor",   "Review scheduled tasks for suspicious entries + decode"),
            ("21", "✦ Permissions Auditor",      "Audit file & folder permissions + inheritance check"),
            ("22", "✦ USB Monitor",              "Monitor USB device connections, history & block"),
            ("23", "✦ Disk Forensics",           "Analyze disk activity, recover artifacts & timeline"),
            ("24", "✦ Env Inspector",            "Environment variables, PATH audit & secret leak scan"),
            ("25", "✦ Startup Optimizer",        "Manage startup programs, services & boot time analysis"),
            ("45", "✦ Hash Calculator",          "Calculate MD5, SHA-1, and SHA-256 for local files [OFFLINE]"),
            ("46", "✦ Base64/Hex Encoder",       "Encode & decode text payloads to Base64 or Hex [OFFLINE]"),
        ],
    },
    {
        "title": "HARDENING & PROTECTION",
        "icon": "✦",
        "color": COL_NEON,
        "accent": COL_TEAL,
        "items": [
            ("26", "✦ System Hardening",  "Check & fix common security misconfigs + CIS benchmark"),
            ("27", "✦ Firewall Manager",          "View, toggle & create Windows Firewall rules + export"),
            ("28", "✦ Registry Protector",        "Monitor & protect critical registry keys + snapshots"),
            ("29", "✦ BIOS/UEFI Checker", "Verify BIOS/UEFI security settings + Secure Boot"),
            ("30", "✦ Exploit Patcher",           "Detect & patch known exploit vectors + CVE database"),
            ("31", "✦ File Integrity Mon", "Monitor files for unauthorized changes + hash baseline"),
            ("32", "✦ Attack Surface Analyzer",   "Enumerate ports, shares, RATs & risk score + remediate"),
            ("33", "✦ Privacy Hardener",          "Disable telemetry, tracking & ad personalization"),
        ],
    },
    {
        "title": "CREDENTIALS & PRIVACY",
        "icon": "✦",
        "color": COL_GOLD,
        "accent": COL_ORANGE,
        "items": [
            ("34", "✦ Password Auditor",  "Audit saved browser credentials + HIBP check"),
            ("35", "✦ Browser Privacy Cleaner",   "Clean browser data, cookies, cache & trackers"),
            ("36", "✦ Phishing URL Checker",      "Analyze URLs + deep API scan (urlscan + VT + GSB)"),
            ("37", "✦ Email Breach Checker",      "Check emails against breach databases + analytics"),
            ("38", "✦ WiFi Password Viewer",      "Extract saved WiFi profiles & passwords"),
        ],
    },
    {
        "title": "INTELLIGENCE & REPORTING",
        "icon": "✦",
        "color": COL_SUCCESS,
        "accent": COL_LIME,
        "items": [
            ("39", "✦ Threat Intel Lookup", "Query AbuseIPDB, VirusTotal, OTX, Shodan, SecurityTrails"),
            ("40", "✦ Log Analyzer",                "Parse & analyze Windows event logs + threat correlate"),
            ("41", "✦ Vulnerability Scanner",       "Scan system for known vulnerabilities + CVE lookup"),
            ("42", "✦ System Report Generator",     "Export comprehensive security assessment (TXT/JSON/HTML)"),
            ("43", "✦ Open Port Monitor",           "Monitor ports, detect changes, Shodan & Censys lookup"),
            ("44", "✦ Dark Web Checker",            "Check data exposure in dark web + breach intel + OSINT"),
        ],
    },
    {
        "title": "BETA - DECOMPILERS & REV ENG",
        "icon": "⚡",
        "color": COL_PINK,
        "accent": COL_PURPLE,
        "items": [
            ("47", "⚡ Enhanced Java Decompiler", "Multi-engine Java decompiler (CFR, Procyon, Fernflower, JD-Core)"),
            ("48", "⚡ Universal Decompiler", "Universal decompiler with external tool integration"),
            ("49", "⚡ Lua Deobfuscator", "Advanced deobfuscation with pattern recognition"),
            ("50", "⚡ Lua Obfuscator", "Maximum protection obfuscation with all features"),
            ("51", "⚡ Lua Decompiler (Unluac)", "Decompile Lua 5.1/5.2 compiled script bytecode [OFFLINE]"),
            ("52", "⚡ Strings Extractor", "Extract human-readable strings from any EXE/DLL/Binary [OFFLINE]"),
        ],
    },
    {
        "title": "MISC - FUN & TOOLS",
        "icon": "🎮",
        "color": COL_LIME,
        "accent": COL_ORANGE,
        "items": [
            ("53", "🎮 ASCII Art Generator", "Generate cool ASCII art from text"),
            ("54", "🎮 Matrix Rain", "Matrix-style falling characters animation"),
            ("55", "🎮 System Prank", "Harmless system pranks and jokes"),
            ("56", "🎮 Fake Error Generator", "Generate realistic fake error messages"),
            ("57", "🎮 Color Picker", "Advanced color picker with hex/rgb conversion"),
            ("58", "🎮 Text Effects", "Apply cool effects to text (rainbow, glow, etc)"),
            ("59", "🎮 Random Jokes", "Display random programming jokes"),
            ("60", "🎮 System Info", "Show detailed system information"),
        ],
    },
]

TOTAL_PAGES = len(PAGES)
MODULE_COUNT = sum(len(p["items"]) for p in PAGES)

ALL_MODULES = {}
for _page in PAGES:
    for _key, _name, _desc in _page["items"]:
        ALL_MODULES[_key] = {"name": _name, "desc": _desc}

DISPATCH = {
    "1":  ("modules.luckyware_scanner",       "LuckywareScanner"),
    "2":  ("modules.ransomware_remover",      "RansomwareRemover"),
    "3":  ("modules.rootkit_detector",        "RootkitDetector"),
    "4":  ("modules.crypto_miner_detector",   "CryptoMinerDetector"),
    "5":  ("modules.keylogger_detector",      "KeyloggerDetector"),
    "6":  ("modules.dll_hijack_scanner",      "DLLHijackScanner"),
    "7":  ("modules.malware_sandbox",         "MalwareSandbox"),
    "8":  ("modules.boot_guard",              "BootGuard"),
    "9":  ("modules.network_scanner",         "NetworkScanner"),
    "10": ("modules.packet_sniffer",          "PacketSniffer"),
    "11": ("modules.wifi_analyzer",           "WiFiAnalyzer"),
    "12": ("modules.dns_blocker",             "DNSBlocker"),
    "13": ("modules.ip_geolocation",          "IPGeolocation"),
    "14": ("modules.ssl_scanner",             "SSLScanner"),
    "15": ("modules.honeypot_detector",       "HoneypotDetector"),
    "16": ("modules.traceroute_mapper",       "TracerouteMapper"),
    "17": ("modules.bandwidth_monitor",       "BandwidthMonitor"),
    "18": ("modules.process_manager",         "ProcessManager"),
    "19": ("modules.service_auditor",         "ServiceAuditor"),
    "20": ("modules.scheduled_task_auditor",  "ScheduledTaskAuditor"),
    "21": ("modules.permissions_auditor",     "PermissionsAuditor"),
    "22": ("modules.usb_monitor",             "USBMonitor"),
    "23": ("modules.disk_forensics",          "DiskForensics"),
    "24": ("modules.env_inspector",           "EnvInspector"),
    "25": ("modules.startup_optimizer",       "StartupOptimizer"),
    "26": ("modules.system_hardening",        "SystemHardening"),
    "27": ("modules.firewall_manager",        "FirewallManager"),
    "28": ("modules.registry_protector",      "RegistryProtector"),
    "29": ("modules.bios_uefi_checker",       "BiosUefiChecker"),
    "30": ("modules.exploit_patcher",         "ExploitPatcher"),
    "31": ("modules.file_integrity_monitor",  "FileIntegrityMonitor"),
    "32": ("modules.attack_surface_analyzer", "AttackSurfaceAnalyzer"),
    "33": ("modules.privacy_hardener",        "PrivacyHardener"),
    "34": ("modules.password_auditor",        "PasswordAuditor"),
    "35": ("modules.browser_privacy_cleaner", "BrowserPrivacyCleaner"),
    "36": ("modules.phishing_url_checker",    "PhishingURLChecker"),
    "37": ("modules.email_breach_checker",    "EmailBreachChecker"),
    "38": ("modules.wifi_password_viewer",    "WiFiPasswordViewer"),
    "39": ("modules.threat_intel_lookup",     "ThreatIntelLookup"),
    "40": ("modules.log_analyzer",            "LogAnalyzer"),
    "41": ("modules.vulnerability_scanner",   "VulnerabilityScanner"),
    "42": ("modules.system_report_generator", "SystemReportGenerator"),
    "43": ("modules.open_port_monitor",       "OpenPortMonitor"),
    "44": ("modules.dark_web_checker",        "DarkWebChecker"),
    "45": ("modules.hash_calculator",         "HashCalculator"),
    "46": ("modules.base64_hex_encoder",      "Base64HexEncoder"),
    "47": ("modules.enhanced_java_decompiler", "EnhancedJavaDecompiler"),
    "48": ("modules.universal_decompiler",    "UniversalDecompiler"),
    "49": ("modules.ultimate_lua_deobfuscator", "UltimateLuaDeobfuscator"),
    "50": ("modules.premium_lua_obfuscator", "PremiumLuaObfuscator"),
    "51": ("modules.lua_decompiler",          "LuaDecompiler"),
    "52": ("modules.strings_extractor",       "StringsExtractor"),
    "53": ("modules.ascii_art_generator",    "ASCIIArtGenerator"),
    "54": ("modules.matrix_rain",            "MatrixRain"),
    "55": ("modules.system_prank",           "SystemPrank"),
    "56": ("modules.fake_error_generator",   "FakeErrorGenerator"),
    "57": ("modules.color_picker",           "ColorPicker"),
    "58": ("modules.text_effects",            "TextEffects"),
    "59": ("modules.random_jokes",            "RandomJokes"),
    "60": ("modules.system_info",             "SystemInfo"),
}


# ── Helpers ───────────────────────────────────────────────────────────────

def _tw() -> int:
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 100


def _th() -> int:
    try:
        return os.get_terminal_size().lines
    except Exception:
        return 30


def _cls():
    os.system("cls" if sys.platform == "win32" else "clear")


def _center_pad(text: str, width: int) -> str:
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text


def _box_line(char: str, width: int, color: str) -> str:
    return f"[{color}]{char * width}[/{color}]"


# ══════════════════════════════════════════════════════════════════════════
#  COSMOS UI v5.0
# ══════════════════════════════════════════════════════════════════════════

class CosmosUI:
    def __init__(self):
        self.console = Console(highlight=False)
        self.current_page = 0
        self._session_start = datetime.now()
        self._launch_history: list[str] = []
        self._favorites: set[str] = set()

    def _setup_console_font(self):
        """Try to set a modern monospaced font if possible."""
        import ctypes
        
        # Check if running in Windows Terminal (WT_SESSION environment variable)
        in_wt = "WT_SESSION" in os.environ
        if in_wt:
            # We don't try to change font via ctypes if in WT, as WT handles its own profiles.
            return True
            
        # If standard conhost.exe, try to set a better font via ctypes
        try:
            LF_FACESIZE = 32
            STD_OUTPUT_HANDLE = -11

            class COORD(ctypes.Structure):
                _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

            class CONSOLE_FONT_INFOEX(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_ulong),
                            ("nFont", ctypes.c_ulong),
                            ("dwFontSize", COORD),
                            ("FontFamily", ctypes.c_uint),
                            ("FontWeight", ctypes.c_uint),
                            ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

            font = CONSOLE_FONT_INFOEX()
            font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
            
            # Fetch current to populate structure correctly
            h_out = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            ctypes.windll.kernel32.GetCurrentConsoleFontEx(h_out, ctypes.c_long(False), ctypes.byref(font))
            
            # Try setting Fira Code or Cascadia Code (monospaced)
            font.FaceName = "SF Mono"
            font.FontWeight = 700  # Bold
            font.dwFontSize.Y = 16
            
            ctypes.windll.kernel32.SetCurrentConsoleFontEx(h_out, ctypes.c_long(False), ctypes.byref(font))
            
            # Check if it accepted our first choice (SF Mono)
            ctypes.windll.kernel32.GetCurrentConsoleFontEx(h_out, ctypes.c_long(False), ctypes.byref(font))
            if font.FaceName != "SF Mono":
                # Fallback to Cascadia Code
                font.FaceName = "Cascadia Code"
                ctypes.windll.kernel32.SetCurrentConsoleFontEx(h_out, ctypes.c_long(False), ctypes.byref(font))
                
        except Exception:
            pass
            
        return False

    # ───────────────────────���──────────────────────────────────────────────
    #  BOOT ANIMATION (enhanced)
    # ──────────────────────────────────────────────────────────────────────
    def _boot_animation(self):
        _cls()
        c = self.console
        cols = _tw()

        # Phase 1: Starfield fade in with ✦
        star_colors = [COL_CYAN, COL_NEON, COL_BLUE, COL_PINK, COL_PURPLE]
        for frame in range(12):
            _cls()
            density = 0.002 * (frame + 1)
            lines = []
            for _ in range(6):
                row = ""
                for _ in range(min(cols, 120)):
                    if random.random() < density:
                        col = random.choice(star_colors)
                        row += f"[{col}]✦[/{col}]"
                    else:
                        row += " "
                lines.append(row)
            c.print("\n".join(lines))
            time.sleep(0.04)

        _cls()
        
        # Phase 2: Logo Reveal
        self._print_starfield(1)
        logo_lines = LOGO_ART.strip("\n").split("\n")
        
        for line in logo_lines:
            c.print(f"[bold {COL_NEON}]{line}[/bold {COL_NEON}]", justify="center")
            time.sleep(0.04)
            
        c.print()
        c.print(Align.center(f"[bold {COL_STAR}]✦[/bold {COL_STAR}]  [bold {COL_GOLD}]{TAGLINE}[/bold {COL_GOLD}]  [bold {COL_STAR}]✦[/bold {COL_STAR}]"))
        c.print(Align.center(
            f"[{COL_DIM}]{VERSION}[/{COL_DIM}]  "
            f"[{COL_NEON}]✦[/{COL_NEON}]  "
            f"[{COL_DIM}]{MODULE_COUNT} Security Modules[/{COL_DIM}]  "
            f"[{COL_NEON}]✦[/{COL_NEON}]  "
            f"[{COL_DIM}]Offline + API Integrations[/{COL_DIM}]"
        ))
        c.print()
        c.print()

        # Phase 3: Stylish Progress Bar
        steps = [
            ("Initializing Cosmos kernel...", COL_CYAN),
            ("Loading offline security modules...", COL_BLUE),
            ("Mounting cryptographic engines...", COL_PINK),
            ("Securing local environment...", COL_PURPLE),
            ("Connecting to API hubs...", COL_NEON),
            ("Calibrating UI rendering...", COL_GOLD),
            ("System ready for deployment.", COL_SUCCESS),
        ]
        
        with Progress(
            TextColumn("  [bold {task.fields[col]}]✦ {task.description:<35}[/bold {task.fields[col]}]"),
            BarColumn(bar_width=40, style=f"dim {COL_BLUE}", complete_style=f"bold {COL_NEON}"),
            TextColumn("[bold bright_white]{task.percentage:>3.0f}%[/bold bright_white]"),
            console=c,
        ) as prog:
            task = prog.add_task(steps[0][0], total=100, col=steps[0][1])
            
            for i in range(1, 101):
                idx = min((i * len(steps)) // 100, len(steps) - 1)
                desc, col = steps[idx]
                prog.update(task, description=desc, col=col, completed=i)
                time.sleep(0.02)

        c.print()
        time.sleep(0.4)

    def _welcome_screen(self):
        """Display welcome message instead of license screen"""
        c = self.console
        _cls()
        
        welcome_panel = Panel(
            f"[bold {COL_NEON}]✦ WELCOME TO COSMOS.WIN ✦[/bold {COL_NEON}]\n\n"
            f"[{COL_DIM}]Premium Cybersecurity Suite\n"
            f"{MODULE_COUNT} Security Modules Ready\n"
            f"Advanced Reverse Engineering Tools\n"
            f"Modern UI with External Tool Integration[/{COL_DIM}]\n\n"
            f"[bold {COL_SUCCESS}]All modules unlocked and ready to use![/bold {COL_SUCCESS}]",
            border_style=COL_NEON,
            box=box.ROUNDED,
            padding=(2, 4),
            width=min(_tw() - 4, 80)
        )
        
        c.print(Align.center(welcome_panel))
        c.print()
        c.input(f"  [{COL_DIM}]Press Enter to continue...[/{COL_DIM}]")

    # ──────────────────────────────────────────────────────────────────────
    #  MAIN ENTRY
    # ──────────────────────────────────────────────────────────────────────
    def run(self):
        is_wt = self._setup_console_font()
        self._boot_animation()

        if not is_wt:
            self.console.print()
            self.console.print(Align.center(Panel(
                f"[{COL_WARN}]\u26a0  RECOMMENDATION[/{COL_WARN}]\n\n"
                f"[{COL_DIM}]For the best experience, including support for modern fonts\n"
                f"and ligatures, please run Cosmos.win inside [bold bright_white]Windows Terminal[/bold bright_white].[/{COL_DIM}]",
                border_style=COL_WARN,
                box=box.ROUNDED,
                padding=(1, 4),
                width=min(_tw() - 4, 72)
            )))
            self.console.print()
            time.sleep(2)

        # Display welcome message
        self._welcome_screen()
        
        self.current_page = 0

        while True:
            choice = self._main_menu()
            if choice is None:
                continue
            upper = choice.upper()
            if upper == "Q":
                self._bye()
                break
            elif upper == "K":
                from utils.api_keys import APIKeyManager
                APIKeyManager(self.console).run()
            elif upper == "D":
                self._dashboard()
            elif upper == "F":
                self._show_favorites()
            elif upper == "H":
                self._show_history()
            elif upper == "R":
                self._quick_scan_menu()
            else:
                # Check if adding to favorites
                if choice.startswith("f") and choice[1:].isdigit():
                    mod_key = choice[1:]
                    if mod_key in ALL_MODULES:
                        if mod_key in self._favorites:
                            self._favorites.discard(mod_key)
                            self.console.print(f"  [{COL_WARN}]Removed from favorites[/{COL_WARN}]")
                        else:
                            self._favorites.add(mod_key)
                            self.console.print(f"  [{COL_SUCCESS}]Added to favorites[/{COL_SUCCESS}]")
                        time.sleep(0.4)
                        continue
                self._dispatch(choice)

    # ──────────────────────────────────────────────────────────────────────
    #  DISPATCH (enhanced with history tracking)
    # ──────────────────────────────────────────────────────────────────────
    def _dispatch(self, choice: str):
        c = self.console
        if choice not in DISPATCH:
            c.print(f"  [{COL_DANGER}]Unknown module: {choice}[/{COL_DANGER}]")
            time.sleep(0.4)
            return

        module_path, class_name = DISPATCH[choice]
        mod_info = ALL_MODULES.get(choice, {})
        mod_name = mod_info.get("name", class_name)

        # Track history
        self._launch_history.append(choice)
        if len(self._launch_history) > 20:
            self._launch_history = self._launch_history[-20:]

        # Loading splash with category color
        _cls()
        c.print()

        # Find which page this module belongs to for themed loading
        page_color = COL_NEON
        for pg in PAGES:
            for k, _, _ in pg["items"]:
                if k == choice:
                    page_color = pg["color"]
                    break

        c.print(Align.center(
            Panel(
                Align.center(Text.from_markup(
                    f"[bold {page_color}]\u23f3  Loading {mod_name}[/bold {page_color}]\n\n"
                    f"[{COL_DIM}]Initializing module subsystems...[/{COL_DIM}]"
                )),
                border_style=page_color,
                box=box.ROUNDED,
                padding=(1, 4),
                width=min(_tw() - 4, 60),
            )
        ))
        time.sleep(0.2)

        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            _cls()
            cls(c).run()
        except Exception as e:
            c.print(f"\n  [{COL_DANGER}]\u274c  Error: {e}[/{COL_DANGER}]")
            c.input(f"\n  [{COL_DIM}]Press Enter to return...[/{COL_DIM}]")

    # ──────────────────────────────────────────────────────────────────────
    #  PAGINATED MAIN MENU (completely redesigned)
    # ──────────────────────────────────────────────────────────────────────
    def _main_menu(self) -> str | None:
        _cls()
        c = self.console
        page = PAGES[self.current_page]
        cols = _tw()
        box_w = min(cols - 4, 100)

        # ── Starfield ──
        self._print_starfield(1)

        # ── Compact gradient logo ──
        self._print_logo_mini()

        # ── Status dashboard ribbon ──
        now = datetime.now().strftime("%H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")
        from utils.api_keys import list_configured_services
        api_count = len(list_configured_services())
        uptime = str(datetime.now() - self._session_start).split(".")[0]

        # Build ribbon with rich formatting
        api_badge = f"[bold {COL_NEON}]{api_count}[/bold {COL_NEON}]" if api_count > 0 else f"[{COL_DIM}]0[/{COL_DIM}]"
        fav_count = len(self._favorites)
        hist_count = len(self._launch_history)

        ribbon_items = [
            f"[bold {COL_GOLD}]\u2b50 Lifetime Developer[/bold {COL_GOLD}]",
            f"[bold {COL_CYAN}]\U0001f4e6 {MODULE_COUNT} Modules[/bold {COL_CYAN}]",
            f"\U0001f511 APIs: {api_badge}",
            f"[{COL_SUCCESS}]\u25cf[/{COL_SUCCESS}] [{COL_DIM}]Online[/{COL_DIM}]",
            f"[{COL_DIM}]\U0001f553 {now}[/{COL_DIM}]",
        ]
        separator = f"  [{COL_DIM}]\u2502[/{COL_DIM}]  "
        ribbon = f"  [{COL_DIM}]\u2502[/{COL_DIM}]  " + separator.join(ribbon_items) + f"  [{COL_DIM}]\u2502[/{COL_DIM}]"
        c.print(Align.center(ribbon))
        c.print()

        # ── Page tabs (horizontal, interactive look) ──
        tabs = ""
        for i in range(TOTAL_PAGES):
            pg = PAGES[i]
            num = i + 1
            if i == self.current_page:
                tabs += f" [bold {pg['color']} on grey15] {pg['icon']} {num}:{pg['title'][:12]} [/bold {pg['color']} on grey15] "
            else:
                tabs += f" [{COL_DIM}]{pg['icon']} {num}[/{COL_DIM}] "
        c.print(Align.center(tabs))

        # ── Category divider with gradient ──
        pcolor = page.get("color", COL_CYAN)
        accent = page.get("accent", pcolor)
        c.print()
        c.print(Align.center(
            f"[{COL_DIM}]\u2500\u2500\u2500[/{COL_DIM}]  "
            f"[bold {pcolor}]{page['icon']}  {page['title']}[/bold {pcolor}]  "
            f"[{COL_DIM}]\u2500\u2500\u2500[/{COL_DIM}]  "
            f"[{COL_DIM}]({len(page['items'])} modules)[/{COL_DIM}]"
        ))
        c.print()

        # ── Module cards (enhanced two-column layout for wide terminals) ──
        items = page["items"]
        card_width = min(box_w - 4, 92)

        for idx, (key, name, desc) in enumerate(items):
            is_fav = key in self._favorites
            fav_mark = f" [{COL_GOLD}]\u2605[/{COL_GOLD}]" if is_fav else ""

            # Number badge
            num_str = f"[bold {COL_GOLD}]{key:>2}[/bold {COL_GOLD}]"
            sep = f"[{COL_DIM}]\u2502[/{COL_DIM}]"

            # Alternate row shading
            if idx % 2 == 0:
                desc_col = COL_STAR
                name_col = COL_CYAN
            else:
                desc_col = COL_DIM
                name_col = accent

            # Build clean module row
            line = (
                f"    {num_str}  {sep}  [bold {name_col}]{name}[/bold {name_col}]{fav_mark}"
            )
            padding = " " * max(1, 36 - len(name))
            line += f"{padding}{sep}  [{desc_col}]{desc}[/{desc_col}]"

            c.print(line)

            if idx < len(items) - 1:
                divider_w = min(box_w - 8, 88)
                c.print(f"    [{COL_DIM}]{'.' * divider_w}[/{COL_DIM}]")

        c.print()

        # ── Navigation bar (enhanced with more options) ──
        c.print(Rule(style=COL_DIM))

        prev_s = f"[bold {COL_CYAN}]\u25c0 P[/bold {COL_CYAN}]" if self.current_page > 0 else f"[{COL_DIM}]\u25c0 P[/{COL_DIM}]"
        next_s = f"[bold {COL_CYAN}]N \u25b6[/bold {COL_CYAN}]" if self.current_page < TOTAL_PAGES - 1 else f"[{COL_DIM}]N \u25b6[/{COL_DIM}]"
        page_s = f"[bold {COL_STAR}]{self.current_page + 1}[/bold {COL_STAR}][{COL_DIM}]/{TOTAL_PAGES}[/{COL_DIM}]"

        nav_line = (
            f"  {prev_s}  [{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"Page {page_s}  [{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"{next_s}  [{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_NEON}]S[/{COL_NEON}] [{COL_DIM}]Search[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_GOLD}]1-{MODULE_COUNT}[/{COL_GOLD}] [{COL_DIM}]Launch[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_PINK}]K[/{COL_PINK}] [{COL_DIM}]API Keys[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_BLUE}]D[/{COL_BLUE}] [{COL_DIM}]Dashboard[/{COL_DIM}]"
        )
        c.print(Align.center(nav_line))

        # Second nav row with extras
        nav_line2 = (
            f"  [{COL_GOLD}]F[/{COL_GOLD}] [{COL_DIM}]Favorites[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_PURPLE}]H[/{COL_PURPLE}] [{COL_DIM}]History[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_ORANGE}]R[/{COL_ORANGE}] [{COL_DIM}]Quick Scan[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_DIM}]f<#> Fav/Unfav[/{COL_DIM}]  "
            f"[{COL_DIM}]\u2502[/{COL_DIM}]  "
            f"[{COL_DANGER}]Q[/{COL_DANGER}] [{COL_DIM}]Quit[/{COL_DIM}]"
        )
        c.print(Align.center(nav_line2))
        c.print()

        # ── Prompt ──
        choice = Prompt.ask(
            f"  [bold {COL_NEON}]cosmos[/bold {COL_NEON}]"
            f"[{COL_DIM}]::[/{COL_DIM}]"
            f"[bold {COL_PINK}]win[/bold {COL_PINK}] "
            f"[{COL_GOLD}]\u25b8[/{COL_GOLD}]",
            default="N",
        ).strip()

        upper = choice.upper()
        if upper == "N":
            self.current_page = (self.current_page + 1) % TOTAL_PAGES
            return None
        elif upper == "P":
            self.current_page = (self.current_page - 1) % TOTAL_PAGES
            return None
        elif upper == "S":
            return self._search_module()
        # Direct page jump: 1-6 for pages when prefixed with 'g'
        elif upper.startswith("G") and upper[1:].isdigit():
            pg_num = int(upper[1:]) - 1
            if 0 <= pg_num < TOTAL_PAGES:
                self.current_page = pg_num
            return None

        return choice

    # ──────────────────────────────────────────────────────────────────────
    #  SEARCH (enhanced with fuzzy matching)
    # ──────────────────────────────────────────────────────────────────────
    def _search_module(self) -> str | None:
        c = self.console
        c.print()
        query = Prompt.ask(f"  [{COL_NEON}]\U0001f50d  Search modules[/{COL_NEON}]").strip().lower()
        if not query:
            return None

        matches = []
        for key, info in ALL_MODULES.items():
            name_lower = info["name"].lower()
            desc_lower = info["desc"].lower()
            # Score-based matching
            score = 0
            if query == name_lower:
                score = 100
            elif query in name_lower:
                score = 80
            elif query in desc_lower:
                score = 60
            else:
                # Fuzzy: check if all query chars appear in order
                qi = 0
                for ch in name_lower + " " + desc_lower:
                    if qi < len(query) and ch == query[qi]:
                        qi += 1
                if qi == len(query):
                    score = 30

            if score > 0:
                matches.append((key, info["name"], info["desc"], score))

        # Sort by score descending
        matches.sort(key=lambda x: x[3], reverse=True)

        if not matches:
            c.print(f"  [{COL_WARN}]No modules matching '{query}'[/{COL_WARN}]")
            time.sleep(0.6)
            return None

        if len(matches) == 1:
            c.print(f"  [{COL_SUCCESS}]Found: {matches[0][1]}[/{COL_SUCCESS}]")
            time.sleep(0.3)
            return matches[0][0]

        c.print()
        c.print(f"  [bold {COL_CYAN}]Results for '{query}':[/bold {COL_CYAN}]")
        c.print()

        # Show results in a nice table
        result_table = Table(box=box.ROUNDED, border_style=COL_CYAN, show_header=True,
                            header_style=f"bold {COL_CYAN}", expand=False)
        result_table.add_column("#", style=f"bold {COL_GOLD}", width=5, justify="center")
        result_table.add_column("MODULE", style=f"bold {COL_STAR}", width=30)
        result_table.add_column("DESCRIPTION", style=COL_DIM, width=45)
        result_table.add_column("MATCH", style=f"bold {COL_NEON}", width=8, justify="center")

        for key, name, desc, score in matches[:10]:
            match_label = "exact" if score >= 80 else "good" if score >= 60 else "fuzzy"
            match_col = COL_SUCCESS if score >= 80 else COL_WARN if score >= 60 else COL_DIM
            result_table.add_row(
                key, name, desc[:45],
                f"[{match_col}]{match_label}[/{match_col}]"
            )

        c.print(Align.center(result_table))
        c.print()

        pick = Prompt.ask(
            f"  [{COL_CYAN}]Module # to launch (or Enter to cancel)[/{COL_CYAN}]", default=""
        ).strip()

        if pick and pick in DISPATCH:
            return pick
        return None

    # ──────────────────────────────────────────────────────────────────────
    #  DASHBOARD (new feature)
    # ──────────────────────────────────────────────────────────────────────
    def _dashboard(self):
        _cls()
        c = self.console
        cols = _tw()
        w = min(cols - 4, 90)

        self._print_starfield(1)
        c.print(Align.center(
            f"[bold {COL_NEON}]\u2550\u2550\u2550  SYSTEM DASHBOARD  \u2550\u2550\u2550[/bold {COL_NEON}]"
        ))
        c.print()

        now = datetime.now()
        uptime = str(now - self._session_start).split(".")[0]
        from utils.api_keys import list_configured_services, SUPPORTED_SERVICES

        configured = list_configured_services()
        total_services = len(SUPPORTED_SERVICES)

        # ── System Info ──
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024**3)
            ram_total = ram.total / (1024**3)
            disk = psutil.disk_usage('C:\\')
            disk_used = disk.used / (1024**3)
            disk_total = disk.total / (1024**3)
            has_psutil = True
        except Exception:
            has_psutil = False

        # ── Session Info Panel ──
        session_content = (
            f"  [{COL_CYAN}]Session Start:[/{COL_CYAN}]   {self._session_start.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  [{COL_CYAN}]Uptime:[/{COL_CYAN}]          {uptime}\n"
            f"  [{COL_CYAN}]Current Time:[/{COL_CYAN}]     {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  [{COL_CYAN}]Modules Loaded:[/{COL_CYAN}]   [bold {COL_NEON}]{MODULE_COUNT}[/bold {COL_NEON}]\n"
            f"  [{COL_CYAN}]API Keys:[/{COL_CYAN}]         [bold {COL_GOLD}]{len(configured)}/{total_services}[/bold {COL_GOLD}] configured\n"
            f"  [{COL_CYAN}]Modules Launched:[/{COL_CYAN}]  {len(self._launch_history)}\n"
            f"  [{COL_CYAN}]Favorites:[/{COL_CYAN}]        {len(self._favorites)}"
        )
        c.print(Panel(
            session_content,
            title=f"[bold {COL_CYAN}]Session Info[/bold {COL_CYAN}]",
            border_style=COL_CYAN,
            box=box.ROUNDED,
            width=w,
        ))
        c.print()

        # ── System Resources Panel ──
        if has_psutil:
            cpu_bar_len = 30
            cpu_filled = int(cpu_percent / 100 * cpu_bar_len)
            cpu_bar = f"[{COL_NEON}]{'█' * cpu_filled}[/{COL_NEON}][{COL_DIM}]{'░' * (cpu_bar_len - cpu_filled)}[/{COL_DIM}]"
            ram_pct = ram.percent
            ram_filled = int(ram_pct / 100 * cpu_bar_len)
            ram_bar = f"[{COL_CYAN}]{'█' * ram_filled}[/{COL_CYAN}][{COL_DIM}]{'░' * (cpu_bar_len - ram_filled)}[/{COL_DIM}]"
            disk_pct = disk.percent
            disk_filled = int(disk_pct / 100 * cpu_bar_len)
            disk_bar = f"[{COL_GOLD}]{'█' * disk_filled}[/{COL_GOLD}][{COL_DIM}]{'░' * (cpu_bar_len - disk_filled)}[/{COL_DIM}]"

            sys_content = (
                f"  [{COL_CYAN}]CPU:[/{COL_CYAN}]   {cpu_bar}  [bold {COL_STAR}]{cpu_percent:.0f}%[/bold {COL_STAR}]\n"
                f"  [{COL_CYAN}]RAM:[/{COL_CYAN}]   {ram_bar}  [bold {COL_STAR}]{ram_used:.1f}/{ram_total:.1f} GB[/bold {COL_STAR}]  ({ram_pct:.0f}%)\n"
                f"  [{COL_CYAN}]Disk:[/{COL_CYAN}]  {disk_bar}  [bold {COL_STAR}]{disk_used:.0f}/{disk_total:.0f} GB[/bold {COL_STAR}]  ({disk_pct:.0f}%)"
            )
            c.print(Panel(
                sys_content,
                title=f"[bold {COL_NEON}]System Resources[/bold {COL_NEON}]",
                border_style=COL_NEON,
                box=box.ROUNDED,
                width=w,
            ))
            c.print()

        # ── API Status Panel ──
        api_table = Table(box=box.SIMPLE, border_style=COL_DIM, show_header=True,
                         header_style=f"bold {COL_CYAN}", expand=False, padding=(0, 1))
        api_table.add_column("SERVICE", style=f"bold {COL_STAR}", width=22)
        api_table.add_column("STATUS", justify="center", width=14)
        api_table.add_column("URL", style=COL_DIM, width=40)

        for sid, info in SUPPORTED_SERVICES.items():
            if sid in configured:
                status = f"[bold {COL_SUCCESS}]ACTIVE[/bold {COL_SUCCESS}]"
            else:
                status = f"[{COL_DIM}]NOT SET[/{COL_DIM}]"
            api_table.add_row(info["name"], status, info["url"][:40])

        c.print(Panel(
            api_table,
            title=f"[bold {COL_GOLD}]API Integration Status[/bold {COL_GOLD}]",
            border_style=COL_GOLD,
            box=box.ROUNDED,
            width=w,
        ))
        c.print()

        # ── Module Categories Overview ──
        cat_table = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {COL_CYAN}",
                         expand=False, padding=(0, 1))
        cat_table.add_column("CATEGORY", style=f"bold {COL_STAR}", width=32)
        cat_table.add_column("MODULES", justify="center", width=10)
        cat_table.add_column("COLOR", justify="center", width=12)

        for pg in PAGES:
            col = pg["color"]
            cat_table.add_row(
                f"[{col}]{pg['icon']} {pg['title']}[/{col}]",
                f"[bold {COL_STAR}]{len(pg['items'])}[/bold {COL_STAR}]",
                f"[{col}]\u2588\u2588\u2588[/{col}]"
            )

        c.print(Panel(
            cat_table,
            title=f"[bold {COL_PURPLE}]Module Categories[/bold {COL_PURPLE}]",
            border_style=COL_PURPLE,
            box=box.ROUNDED,
            width=w,
        ))

        # ── Most Used Modules ──
        if self._launch_history:
            c.print()
            from collections import Counter
            freq = Counter(self._launch_history)
            top_mods = freq.most_common(5)

            usage_table = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {COL_CYAN}",
                               expand=False, padding=(0, 1))
            usage_table.add_column("MODULE", style=f"bold {COL_STAR}", width=32)
            usage_table.add_column("LAUNCHES", justify="center", width=10)

            for mod_key, count in top_mods:
                name = ALL_MODULES.get(mod_key, {}).get("name", mod_key)
                bar = f"[{COL_NEON}]{'=' * min(count * 2, 20)}[/{COL_NEON}]"
                usage_table.add_row(name, f"[bold {COL_GOLD}]{count}[/bold {COL_GOLD}] {bar}")

            c.print(Panel(
                usage_table,
                title=f"[bold {COL_ORANGE}]Most Used Modules[/bold {COL_ORANGE}]",
                border_style=COL_ORANGE,
                box=box.ROUNDED,
                width=w,
            ))

        c.print()
        c.input(f"  [{COL_DIM}]Press Enter to return to menu...[/{COL_DIM}]")

    # ──────────────────────────────────────────────────────────────────────
    #  FAVORITES (new feature)
    # ──────────────────────────────────────────────────────────────────────
    def _show_favorites(self):
        c = self.console
        if not self._favorites:
            c.print(f"\n  [{COL_DIM}]No favorites yet. Use 'f<number>' to add (e.g., f1 for module 1).[/{COL_DIM}]")
            time.sleep(1)
            return

        c.print()
        c.print(f"  [bold {COL_GOLD}]\u2605  FAVORITES[/bold {COL_GOLD}]")
        c.print()

        fav_table = Table(box=box.ROUNDED, border_style=COL_GOLD, show_header=True,
                         header_style=f"bold {COL_CYAN}", expand=False)
        fav_table.add_column("#", style=f"bold {COL_GOLD}", width=5, justify="center")
        fav_table.add_column("MODULE", style=f"bold {COL_STAR}", width=30)
        fav_table.add_column("DESCRIPTION", style=COL_DIM, width=45)

        for key in sorted(self._favorites, key=int):
            info = ALL_MODULES.get(key, {})
            fav_table.add_row(key, info.get("name", "?"), info.get("desc", "?")[:45])

        c.print(Align.center(fav_table))
        c.print()

        pick = Prompt.ask(
            f"  [{COL_CYAN}]Module # to launch (or Enter to cancel)[/{COL_CYAN}]", default=""
        ).strip()
        if pick and pick in DISPATCH:
            self._dispatch(pick)

    # ──────────────────────────────────────────────────────────────────────
    #  HISTORY (new feature)
    # ──────────────────────────────────────────────────────────────────────
    def _show_history(self):
        c = self.console
        if not self._launch_history:
            c.print(f"\n  [{COL_DIM}]No launch history yet.[/{COL_DIM}]")
            time.sleep(0.6)
            return

        c.print()
        c.print(f"  [bold {COL_PURPLE}]\U0001f4dc  LAUNCH HISTORY[/bold {COL_PURPLE}]  [{COL_DIM}](last 20)[/{COL_DIM}]")
        c.print()

        for i, key in enumerate(reversed(self._launch_history[-15:]), 1):
            info = ALL_MODULES.get(key, {})
            c.print(f"    [{COL_DIM}]{i:>2}.[/{COL_DIM}]  [{COL_GOLD}]{key:>2}[/{COL_GOLD}]  [{COL_DIM}]\u2502[/{COL_DIM}]  [{COL_STAR}]{info.get('name', '?')}[/{COL_STAR}]")

        c.print()
        pick = Prompt.ask(
            f"  [{COL_CYAN}]Module # to relaunch (or Enter to cancel)[/{COL_CYAN}]", default=""
        ).strip()
        if pick and pick in DISPATCH:
            self._dispatch(pick)

    # ──────────────────────────────────────────────────────────────────────
    #  QUICK SCAN MENU (new feature)
    # ──────────────────────────────────────────────────────────────────────
    def _quick_scan_menu(self):
        c = self.console
        c.print()
        c.print(f"  [bold {COL_ORANGE}]\u26a1  QUICK SCAN[/bold {COL_ORANGE}]  [{COL_DIM}]Launch common scans quickly[/{COL_DIM}]")
        c.print()

        quick_items = [
            ("1", "Full Malware Scan",      "1",  "Luckyware Scanner"),
            ("2", "Network Discovery",      "9",  "Network Scanner"),
            ("3", "Vulnerability Check",    "41", "Vulnerability Scanner"),
            ("4", "Port Monitor",           "43", "Open Port Monitor"),
            ("5", "Threat Intel Lookup",    "39", "Threat Intel Lookup"),
            ("6", "Email Breach Check",     "37", "Email Breach Checker"),
            ("7", "System Report",          "42", "System Report Generator"),
        ]

        for qk, label, mod_key, mod_name in quick_items:
            c.print(f"    [{COL_GOLD}]{qk}[/{COL_GOLD}]  [{COL_DIM}]\u2502[/{COL_DIM}]  [{COL_ORANGE}]{label}[/{COL_ORANGE}]  [{COL_DIM}]-> {mod_name}[/{COL_DIM}]")

        c.print(f"    [{COL_DIM}]0[/{COL_DIM}]  [{COL_DIM}]\u2502[/{COL_DIM}]  [{COL_DIM}]Cancel[/{COL_DIM}]")
        c.print()

        pick = Prompt.ask(f"  [{COL_ORANGE}]quick[/{COL_ORANGE}][{COL_DIM}]>[/{COL_DIM}]", default="0").strip()

        for qk, label, mod_key, mod_name in quick_items:
            if pick == qk:
                self._dispatch(mod_key)
                return

    # ──────────────────────────────────────────────────────────────────────
    #  HELPERS (enhanced)
    # ──────────────────────────────────────────────────────────────────────
    def _print_logo_small(self):
        """Print the full logo with gradient and tagline."""
        c = self.console
        logo_lines = LOGO_ART.strip("\n").split("\n")
        gradient = [COL_CYAN, COL_NEON, COL_BLUE, COL_CYAN, COL_NEON, COL_GOLD, COL_PINK]
        for i, line in enumerate(logo_lines):
            col = gradient[i % len(gradient)]
            c.print(f"[bold {col}]{line}[/bold {col}]", justify="center")
        c.print(Align.center(
            f"[bold {COL_GOLD}]{TAGLINE}[/bold {COL_GOLD}]  [{COL_DIM}]{VERSION}[/{COL_DIM}]"
        ))
        c.print()

    def _print_logo_mini(self):
        """Print a slightly more compact logo for menu screens."""
        c = self.console
        logo_lines = LOGO_MINI.strip("\n").split("\n")
        gradient = [COL_CYAN, COL_NEON, COL_BLUE, COL_PINK, COL_GOLD]
        for i, line in enumerate(logo_lines):
            col = gradient[i % len(gradient)]
            c.print(f"[bold {col}]{line}[/bold {col}]", justify="center")
        c.print(Align.center(
            f"[bold {COL_GOLD}]{TAGLINE}[/bold {COL_GOLD}]  "
            f"[{COL_DIM}]{VERSION}[/{COL_DIM}]  "
            f"[{COL_NEON}]\u2726[/{COL_NEON}]  "
            f"[{COL_DIM}]{MODULE_COUNT} Modules[/{COL_DIM}]"
        ))
        c.print()

    def _print_starfield(self, rows: int = 1):
        cols = min(_tw(), 120)
        c = self.console
        star_colors = [COL_CYAN, COL_NEON, COL_BLUE, COL_STAR, COL_PINK, COL_PURPLE]
        for _ in range(rows):
            row = ""
            for _ in range(cols):
                if random.random() < 0.03:
                    ch = random.choice(NEON_STARS)
                    col = random.choice(star_colors)
                    row += f"[{col}]{ch}[/{col}]"
                else:
                    row += " "
            c.print(row)

    def _bye(self):
        _cls()
        c = self.console
        self._print_starfield(2)
        self._print_logo_small()
        c.print()
        w = min(_tw() - 4, 62)

        uptime = str(datetime.now() - self._session_start).split(".")[0]

        c.print(Align.center(Panel(
            Align.center(Text.from_markup(
                f"[bold {COL_NEON}]\u2726  Thank you for using Cosmos.win  \u2726[/bold {COL_NEON}]\n\n"
                f"[{COL_CYAN}]Session Duration:[/{COL_CYAN}] {uptime}\n"
                f"[{COL_CYAN}]Modules Used:[/{COL_CYAN}] {len(set(self._launch_history))}\n"
                f"[{COL_CYAN}]Total Launches:[/{COL_CYAN}] {len(self._launch_history)}\n\n"
                f"[{COL_DIM}]Stay safe in the galaxy. \U0001f30c[/{COL_DIM}]\n"
                f"[{COL_DIM}]Session ended at {datetime.now().strftime('%H:%M:%S')}[/{COL_DIM}]"
            )),
            border_style=COL_NEON,
            box=box.DOUBLE,
            padding=(1, 4),
            width=w,
        )))
        c.print()
        time.sleep(1.2)
