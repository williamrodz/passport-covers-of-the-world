# Passport Poster Assembly

Create beautiful posters from passport cover images organized by continent.

## Features

- Generates posters with passport covers from 199 countries
- Adds country name labels below each passport
- Customizable font size and font family
- Supports custom text and background colors
- Organizes passports by continent (Africa, Asia, Europe, North America, South America, Oceania)

## Setup

### Option 1: Using uv (recommended)

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install pillow

# Or install with jupyter support
uv pip install pillow jupyter notebook
```

### Option 2: Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Script

The script includes example code that creates three posters:

```bash
# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the script
python posterAssembly.py
```

This will create:
- `produtti/asia_poster_with_labels.jpg` - 7×7 grid (49 countries)
- `produtti/south_america_poster_with_labels.jpg` - 5×3 grid (13 countries)
- `produtti/world_poster_with_labels.jpg` - 20×10 grid (199 countries)

### Using the Functions

```python
from posterAssembly import load_passport_paths, get_poster

# Load passport images
region_to_paths = load_passport_paths()

# Create a poster with default settings
poster = get_poster(
    images_per_row=7,
    image_paths=sorted(region_to_paths["asia"]),
    add_labels=True,
    font_size=40,
    font_family="Arial"
)

# Save the poster
poster.convert("RGB").save("my_poster.jpg", "JPEG", quality=95)
```

### Customization Options

```python
# Custom font size and family
poster = get_poster(
    images_per_row=10,
    image_paths=all_paths,
    add_labels=True,
    font_size=50,              # Larger text
    font_family="Helvetica"    # Different font
)

# Custom colors (RGBA tuples)
poster = get_poster(
    images_per_row=8,
    image_paths=paths,
    text_color=(50, 50, 50, 255),    # Dark gray text
    bg_color=(240, 240, 240, 255)    # Light gray background
)

# Without labels
poster = get_poster(
    images_per_row=8,
    image_paths=paths,
    add_labels=False
)
```

## Available Fonts (macOS)

Common system fonts:
- Arial
- Helvetica
- Times New Roman
- Courier
- Georgia
- Verdana

## Jupyter Notebook

The original `posterAssembly.ipynb` notebook is also available for interactive exploration and customization.

To use it:

```bash
# Install jupyter if not already installed
uv pip install jupyter notebook

# Start jupyter
jupyter notebook posterAssembly.ipynb
```

## Suggested Poster Dimensions

### World Posters (199 countries)
- **20×10 grid**: 40"×44" (nearly square)
- **23×9 grid**: 46"×30" (wide landscape)
- **18×11 grid**: 36"×48" (portrait)

### Continent Posters
- **Africa** (53): 8×7 grid → 24"×30"
- **Asia** (49): 7×7 grid → 24"×24" (perfect square!)
- **Europe** (47): 8×6 grid → 24"×24"
- **North America** (23): 6×4 grid → 18"×18"
- **South America** (13): 5×3 grid → 18"×14"
- **Oceania** (14): 4×4 grid → 16"×16"

## File Structure

```
.
├── posterAssembly.py       # Python script
├── posterAssembly.ipynb    # Jupyter notebook
├── ppcovers/               # Passport cover images by continent
│   ├── africa/
│   ├── asia/
│   ├── europe/
│   ├── north_america/
│   ├── south_america/
│   └── oceania/
└── produtti/               # Output folder for generated posters
```

## Fonts to Use
Standard System Fonts (Always Available)

  - Arial
  - Arial-Black
  - Arial-Bold
  - Georgia
  - Georgia-Bold
  - Times New Roman
  - Times New Roman Bold
  - Verdana
  - Verdana-Bold
  - Courier New
  - Courier New Bold

  Decorative/Display Fonts (Great for Poster Titles)

  - LithosPro-Regular ← You're using this
  - LithosPro-Black (heavier version)
  - TrajanPro-Bold (classic serif, great for titles)
  - TrajanPro-Regular
  - CooperBlackStd (bold, vintage look)
  - CharlemagneStd-Bold (elegant small caps)
  - BrushScriptStd (script/handwritten)
  - RosewoodStd-Regular (decorative western style)
  - StencilStd (stencil style)
  - BlackoakStd (bold display font)

  Adobe Pro Fonts (Professional)

  - MyriadPro-Bold (clean, modern)
  - MyriadPro-Semibold
  - MinionPro-Bold (elegant serif)
  - MinionPro-Semibold
  - ChaparralPro-Bold
  - NuevaStd-Bold

  SF Fonts (Apple System Fonts - Modern)

  - SF-Pro-Display-Bold
  - SF-Pro-Display-Black
  - SF-Pro-Display-Heavy

  You can use any of these directly in your code:
  title_font_family="LithosPro-Regular"  # What you're currently using
  title_font_family="TrajanPro-Bold"     # Classic alternative
  title_font_family="MyriadPro-Bold"     # Modern clean look



## License

This project is for educational and personal use.
