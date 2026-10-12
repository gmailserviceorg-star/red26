"""red26: modern terminal styling and color helpers."""
from __future__ import annotations
import os
import re
from typing import Final

__version__: Final[str] = "1.0.0"
_RESET: Final[str] = "\033[0m"
_ANSI_RE: Final[re.Pattern[str]] = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")
_COLORS: Final[dict[str, int]] = {"black":30,"red":31,"green":32,"yellow":33,"blue":34,"magenta":35,"cyan":36,"white":37,"bright_black":90,"bright_red":91,"bright_green":92,"bright_yellow":93,"bright_blue":94,"bright_magenta":95,"bright_cyan":96,"bright_white":97}
_STYLES: Final[dict[str, int]] = {"bold":1,"dim":2,"italic":3,"underline":4}

def _color_disabled() -> bool:
    return "NO_COLOR" in os.environ or os.environ.get("RED26_NO_COLOR", "").lower() in {"1", "true", "yes"}

def colorize(text: object, color: str | None = None, *, background: str | None = None, bold: bool = False, dim: bool = False, italic: bool = False, underline: bool = False, no_color: bool | None = None) -> str:
    """Apply ANSI color and style codes to a value."""
    value = str(text)
    if no_color is None:
        no_color = _color_disabled()
    if no_color:
        return value
    codes: list[str] = []
    if color is not None:
        key = color.lower().replace(" ", "_")
        if key not in _COLORS:
            raise ValueError(f"Unsupported foreground color: {color!r}")
        codes.append(str(_COLORS[key]))
    if background is not None:
        key = background.lower().replace(" ", "_")
        if key not in _COLORS:
            raise ValueError(f"Unsupported background color: {background!r}")
        codes.append(str(_COLORS[key] + 10))
    for enabled, name in ((bold,"bold"),(dim,"dim"),(italic,"italic"),(underline,"underline")):
        if enabled:
            codes.append(str(_STYLES[name]))
    return f"\033[{';'.join(codes)}m{value}{_RESET}" if codes and value else value

def strip_ansi(text: str) -> str:
    """Remove common ANSI CSI and OSC sequences."""
    return _ANSI_RE.sub("", text)

def rgb_to_hex(red: int, green: int, blue: int, *, prefix: bool = True) -> str:
    """Convert integer RGB channels (0–255) to a hex string."""
    channels = (red, green, blue)
    if any(not isinstance(c, int) or isinstance(c, bool) for c in channels):
        raise TypeError("RGB channels must be integers")
    if any(c < 0 or c > 255 for c in channels):
        raise ValueError("RGB channels must be between 0 and 255")
    value = f"{red:02x}{green:02x}{blue:02x}"
    return f"#{value}" if prefix else value

def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """Convert 3- or 6-digit hexadecimal color notation to an RGB tuple."""
    if not isinstance(value, str):
        raise TypeError("Hex color must be a string")
    raw = value.strip().removeprefix("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", raw):
        raw = "".join(c * 2 for c in raw)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", raw):
        raise ValueError(f"Invalid hex color: {value!r}")
    return (int(raw[0:2],16), int(raw[2:4],16), int(raw[4:6],16))

def is_hex_color(value: str) -> bool:
    """Return whether a string is a valid 3- or 6-digit hex color."""
    return isinstance(value, str) and bool(re.fullmatch(r"#?(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value.strip()))

def supports_color(stream: object | None = None) -> bool:
    """Best-effort terminal color support detection."""
    if _color_disabled():
        return False
    if os.environ.get("FORCE_COLOR", "").lower() in {"1", "true", "yes"}:
        return True
    isatty = getattr(stream, "isatty", None)
    if callable(isatty):
        try:
            return bool(isatty())
        except OSError:
            return False
    return False

def red(text: object, **kwargs: object) -> str: return colorize(text, "red", **kwargs)
def green(text: object, **kwargs: object) -> str: return colorize(text, "green", **kwargs)
def blue(text: object, **kwargs: object) -> str: return colorize(text, "blue", **kwargs)
def yellow(text: object, **kwargs: object) -> str: return colorize(text, "yellow", **kwargs)

__all__ = ["__version__","colorize","strip_ansi","rgb_to_hex","hex_to_rgb","is_hex_color","supports_color","red","green","blue","yellow"]
