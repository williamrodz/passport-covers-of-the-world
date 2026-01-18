#!/usr/bin/env python3
"""
List all available fonts on the system that can be used with PIL/Pillow
"""

from PIL import ImageFont
import os
from pathlib import Path

def find_font_files():
    """Find all font files in common macOS font directories"""
    font_dirs = [
        "/System/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
        "/Library/Fonts",
        str(Path.home() / "Library" / "Fonts")
    ]

    font_extensions = ('.ttf', '.otf', '.ttc', '.dfont')
    fonts = {}

    for font_dir in font_dirs:
        if not os.path.exists(font_dir):
            continue

        for file in os.listdir(font_dir):
            if file.lower().endswith(font_extensions):
                font_name = file.rsplit('.', 1)[0]
                font_path = os.path.join(font_dir, file)
                fonts[font_name] = font_path

    return fonts

def test_font(font_name_or_path, size=100):
    """Test if a font can be loaded by PIL"""
    try:
        ImageFont.truetype(font_name_or_path, size)
        return True
    except:
        return False

def main():
    print("=" * 80)
    print("AVAILABLE FONTS ON YOUR SYSTEM")
    print("=" * 80)

    fonts = find_font_files()

    # Group by category
    system_fonts = []
    supplemental_fonts = []
    library_fonts = []
    user_fonts = []

    for name, path in sorted(fonts.items()):
        if "/System/Library/Fonts/Supplemental" in path:
            supplemental_fonts.append((name, path))
        elif "/System/Library/Fonts" in path:
            system_fonts.append((name, path))
        elif "/Library/Fonts" in path:
            library_fonts.append((name, path))
        else:
            user_fonts.append((name, path))

    print(f"\n📁 SYSTEM FONTS ({len(system_fonts)} fonts)")
    print("-" * 80)
    for name, path in system_fonts[:10]:  # Show first 10
        print(f"  {name}")
    if len(system_fonts) > 10:
        print(f"  ... and {len(system_fonts) - 10} more")

    print(f"\n📁 SUPPLEMENTAL FONTS ({len(supplemental_fonts)} fonts)")
    print("-" * 80)
    common_fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Courier', 'Georgia', 'Verdana']
    for name, path in supplemental_fonts:
        if any(cf.replace(' ', '') in name.replace(' ', '') for cf in common_fonts):
            print(f"  {name}")

    print(f"\n📁 LIBRARY FONTS - Installed Applications ({len(library_fonts)} fonts)")
    print("-" * 80)
    for name, path in library_fonts:
        print(f"  {name}")

    if user_fonts:
        print(f"\n📁 USER FONTS ({len(user_fonts)} fonts)")
        print("-" * 80)
        for name, path in user_fonts:
            print(f"  {name}")

    # Check for specific fonts
    print("\n" + "=" * 80)
    print("TESTING SPECIFIC FONTS")
    print("=" * 80)

    test_fonts = [
        ("Lithos Pro Regular", "/Library/Fonts/LithosPro-Regular.otf"),
        ("Lithos Pro Black", "/Library/Fonts/LithosPro-Black.otf"),
        ("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"),
        ("Helvetica", "/System/Library/Fonts/Helvetica.ttc"),
        ("Helvetica-Bold", "/System/Library/Fonts/Helvetica.ttc"),
    ]

    for name, path in test_fonts:
        if os.path.exists(path):
            can_load = test_font(path)
            status = "✓ WORKS" if can_load else "✗ CANNOT LOAD"
            print(f"  {status}: {name}")
            print(f"           Path: {path}")
        else:
            print(f"  ✗ NOT FOUND: {name}")

    print("\n" + "=" * 80)
    print("HOW TO USE FONTS IN YOUR CODE")
    print("=" * 80)
    print("""
For posterAssembly.py, you can use fonts in several ways:

1. Font name only (will try multiple paths):
   title_font_family="Helvetica-Bold"

2. Full path to font file:
   title_font_family="/Library/Fonts/LithosPro-Regular.otf"

3. For Lithos Pro, use either:
   title_font_family="LithosPro-Regular"
   OR
   title_font_family="/Library/Fonts/LithosPro-Regular.otf"
    """)

    print("\nTip: The code tries multiple fallback paths, so shorter names often work!")

if __name__ == "__main__":
    main()
