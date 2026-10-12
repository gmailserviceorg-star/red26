# red26

Modern terminal styling and lightweight color utilities for Python 3.10+.

Independent compatibility-inspired implementation; not affiliated with the original red project.

## Install

```bash
python -m pip install red26
```

## Quick start

```python
from red26 import colorize, strip_ansi, rgb_to_hex, hex_to_rgb

print(colorize('Build something great', 'red', bold=True))
print(rgb_to_hex(255, 64, 64))  # '#ff4040'
print(hex_to_rgb('#ff4040'))    # (255, 64, 64)
print(strip_ansi('\033[31mhello\033[0m'))
```

Features include ANSI foreground/background colors, text styles, ANSI stripping, RGB/hex conversion, hex validation, and no-color support. No runtime dependencies.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m build
```

MIT licensed. See LICENSE and CHANGELOG.md.
