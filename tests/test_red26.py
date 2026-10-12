import pytest
from red26 import blue, colorize, green, hex_to_rgb, is_hex_color, red, rgb_to_hex, strip_ansi, supports_color, yellow

def test_colorize_and_strip():
    value = colorize("hello", "red", bold=True)
    assert value.startswith("\033[31;1m") and value.endswith("\033[0m")
    assert strip_ansi(value) == "hello"

def test_no_color():
    assert colorize("hello", "red", no_color=True) == "hello"
    assert colorize("", "red") == ""

@pytest.mark.parametrize("fn,code", [(red,"31"),(green,"32"),(blue,"34"),(yellow,"33")])
def test_shortcuts(fn, code):
    assert fn("x").startswith(f"\033[{code}m")

def test_hex_conversion():
    assert rgb_to_hex(255,64,64) == "#ff4040"
    assert rgb_to_hex(0,15,255,prefix=False) == "000fff"
    assert hex_to_rgb("#ff4040") == (255,64,64)
    assert hex_to_rgb("abc") == (170,187,204)

def test_invalid_hex_and_rgb():
    with pytest.raises(ValueError): hex_to_rgb("#gggggg")
    with pytest.raises(ValueError): rgb_to_hex(256,0,0)
    with pytest.raises(TypeError): rgb_to_hex(True,0,0)

def test_validation_and_support():
    assert is_hex_color("#abc") and is_hex_color("FF00aa")
    assert not is_hex_color("not-a-color")
    class Plain:
        def isatty(self): return False
    assert supports_color(Plain()) is False
