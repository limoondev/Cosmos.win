"""
Window transparency and console styling via Windows API.
"""
import ctypes
import ctypes.wintypes
import os
import subprocess

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002
HWND_TOP = 0

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def get_console_hwnd() -> int:
    """Return the HWND of the current console window."""
    return kernel32.GetConsoleWindow()


def set_terminal_transparent(alpha: int = 220):
    """
    Set terminal window transparency.
    alpha: 0 (invisible) -> 255 (fully opaque)
    """
    hwnd = get_console_hwnd()
    if not hwnd:
        return
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)


def set_terminal_title(title: str):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def maximize_terminal():
    """Resize terminal to a comfortable large size without maximizing."""
    hwnd = get_console_hwnd()
    if not hwnd:
        return
    # Get screen dimensions
    screen_w = user32.GetSystemMetrics(0)  # SM_CXSCREEN
    screen_h = user32.GetSystemMetrics(1)  # SM_CYSCREEN
    # Use 85% of screen, centered
    win_w = int(screen_w * 0.85)
    win_h = int(screen_h * 0.85)
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    # SWP_NOZORDER = 0x0004
    user32.SetWindowPos(hwnd, HWND_TOP, x, y, win_w, win_h, 0x0004)


def set_console_font_size(size: int = 18):
    """Attempt to set console font size via registry (takes effect on next launch)."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Console",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "FontSize", 0, winreg.REG_DWORD, (size << 16))
        winreg.CloseKey(key)
    except Exception:
        pass
