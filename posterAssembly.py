#!/usr/bin/env python3
"""
Passport Poster Assembly Tool

Creates posters from passport cover images organized by continent.
Each passport can optionally include the country name below it.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Tuple

# Configuration for text labels
DEFAULT_FONT_SIZE = 40
DEFAULT_FONT_FAMILY = "Arial"
TEXT_PADDING = 10
TEXT_BOTTOM_MARGIN = 15  # Extra bottom margin to prevent text cutoff
TEXT_BACKGROUND_COLOR = (255, 255, 255, 255)  # White background
TEXT_COLOR = (0, 0, 0, 255)  # Black text

# Configuration for poster title
DEFAULT_TITLE_FONT_SIZE = 120
DEFAULT_TITLE_FONT_FAMILY = "Helvetica-Bold"
DEFAULT_TITLE_HEIGHT = 200  # Height of the title row in pixels
TITLE_BACKGROUND_COLOR = (255, 255, 255, 255)  # White background
TITLE_TEXT_COLOR = (0, 0, 0, 255)  # Black text

# Configuration for layout spacing
DEFAULT_HORIZONTAL_SPACING = 0  # Horizontal spacing between passport images in pixels
DEFAULT_VERTICAL_SPACING = 0  # Vertical spacing between rows in pixels

# Configuration for poster background
DEFAULT_BACKGROUND_COLOR = (250, 250, 250, 255)  # Very light gray for poster background

# Configuration for poster margins
DEFAULT_LEFT_MARGIN = 5  # Left margin in pixels
DEFAULT_RIGHT_MARGIN = 5  # Right margin in pixels

# Configuration for footer
DEFAULT_FOOTER_FONT_SIZE = 30
DEFAULT_FOOTER_FONT_FAMILY = "Arial"
DEFAULT_FOOTER_HEIGHT = 100  # Height of the footer row in pixels
FOOTER_BACKGROUND_COLOR = (255, 255, 255, 255)  # White background
FOOTER_TEXT_COLOR = (0, 0, 0, 255)  # Black text
FOOTER_LEFT_MARGIN = 40  # Left margin for footer text in pixels

# Paths
ROOT_OF_IMAGES = './ppcovers/'
REGION_FOLDERS = ["africa", "oceania", "asia", "south_america", "north_america", "europe"]


def load_passport_paths():
    """Load all passport image paths organized by region."""
    region_to_full_pp_cover_paths = {}
    for region_name in REGION_FOLDERS:
        region_folder_path = os.path.join(ROOT_OF_IMAGES, region_name)
        if not os.path.exists(region_folder_path):
            print(f"Warning: Region folder '{region_folder_path}' not found")
            continue
        pp_images_in_folder = os.listdir(region_folder_path)
        full_image_paths_for_region = [
            os.path.join(region_folder_path, pp_image_filename)
            for pp_image_filename in pp_images_in_folder
            if pp_image_filename.endswith('.png')
        ]
        region_to_full_pp_cover_paths[region_name] = full_image_paths_for_region
    return region_to_full_pp_cover_paths


def format_country_name(country_name: str) -> str:
    """Convert file-friendly name to display name (e.g., 'United+States' -> 'United States')"""
    return country_name.replace("+", " ")


def get_country_name_from_path(path: str) -> str:
    """Extract country name from file path."""
    country_name = path.split("/")[-1][0:-4]
    return country_name


def add_text_label_to_image(
    image: Image.Image,
    text: str,
    font_size: int = DEFAULT_FONT_SIZE,
    font_family: str = DEFAULT_FONT_FAMILY,
    text_color: Tuple[int, int, int, int] = TEXT_COLOR,
    bg_color: Tuple[int, int, int, int] = TEXT_BACKGROUND_COLOR
) -> Image.Image:
    """
    Add a text label below the passport image.

    Args:
        image: PIL Image object (the passport cover)
        text: String to display (country name)
        font_size: Size of the font in pixels
        font_family: Font family name (must be installed on system)
        text_color: RGBA tuple for text color
        bg_color: RGBA tuple for background color

    Returns:
        New PIL Image with text label below the passport image
    """
    # Reduce font size for long country names (> 22 characters)
    adjusted_font_size = font_size
    if len(text) >= 30:
        adjusted_font_size = int(font_size * 0.65)
    elif len(text) >= 24:
        adjusted_font_size = int(font_size * 0.9)  # Reduce to 75% of original size
    elif len(text) >= 22:
        adjusted_font_size = int(font_size * 0.9)  # Reduce to 75% of original size        
    # Try to load the BOLD version of the specified font
    font = None
    bold_font_variations = [
        f"{font_family}-Bold",  # Try font name with -Bold suffix
        f"{font_family} Bold",  # Try font name with space Bold
        font_family,  # Try as-is (might already be bold)
        f"/System/Library/Fonts/Supplemental/{font_family} Bold.ttf",
        f"/System/Library/Fonts/Supplemental/{font_family}-Bold.ttf",
        f"/System/Library/Fonts/Supplemental/{font_family}.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]

    for font_variant in bold_font_variations:
        try:
            font = ImageFont.truetype(font_variant, adjusted_font_size)
            break  # Success! Stop trying
        except:
            continue

    if font is None:
        # Use default PIL font as last resort
        font = ImageFont.load_default()
        print(f"Warning: Could not load bold font for '{font_family}', using default font")

    # Calculate text size using textbbox
    draw_temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    text_bbox = draw_temp.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Create new image with space for text
    img_width, img_height = image.size
    text_area_height = text_height + TEXT_PADDING + TEXT_BOTTOM_MARGIN
    new_height = img_height + text_area_height

    # Create new image with white background for text area
    new_image = Image.new("RGBA", (img_width, new_height), bg_color)

    # Paste the original passport image at the top (use alpha channel as mask)
    if image.mode == 'RGBA':
        new_image.paste(image, (0, 0), image)
    else:
        new_image.paste(image, (0, 0))

    # Draw the text centered below the image
    draw = ImageDraw.Draw(new_image)
    text_x = (img_width - text_width) // 2
    text_y = img_height + TEXT_PADDING
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return new_image


def create_title_row(
    width: int,
    title: str,
    title_height: int = DEFAULT_TITLE_HEIGHT,
    title_font_size: int = DEFAULT_TITLE_FONT_SIZE,
    title_font_family: str = DEFAULT_TITLE_FONT_FAMILY,
    title_text_color: Tuple[int, int, int, int] = TITLE_TEXT_COLOR,
    title_bg_color: Tuple[int, int, int, int] = TITLE_BACKGROUND_COLOR
) -> Image.Image:
    """
    Create a title row image to place at the top of the poster.

    Args:
        width: Width of the title row (should match poster width)
        title: Title text to display
        title_height: Height of the title row in pixels (default: 200)
        title_font_size: Font size for the title (default: 120)
        title_font_family: Font family for the title (default: "Helvetica-Bold")
        title_text_color: RGBA tuple for title text color (default: black)
        title_bg_color: RGBA tuple for title background color (default: white)

    Returns:
        PIL Image object containing the title row
    """
    # Create the title image
    title_image = Image.new("RGBA", (width, title_height), title_bg_color)

    # Try to load the specified font with multiple fallback strategies
    font = None
    font_variations = [
        title_font_family,  # Try as-is first
        title_font_family.replace(" ", ""),  # Try without spaces (e.g., "Lithos Pro" -> "LithosPro")
        f"{title_font_family.replace(' ', '')}-Regular",  # Add -Regular suffix
        f"/Library/Fonts/{title_font_family.replace(' ', '')}-Regular.otf",  # Library fonts
        f"/Library/Fonts/{title_font_family.replace(' ', '')}.otf",
        f"/System/Library/Fonts/Supplemental/{title_font_family}.ttf",
        f"/System/Library/Fonts/Supplemental/{title_font_family.replace('-Bold', '')}.ttf",
        "/System/Library/Fonts/Helvetica.ttc",  # Final fallback
    ]

    for font_path in font_variations:
        try:
            font = ImageFont.truetype(font_path, title_font_size)
            break  # Success! Stop trying
        except:
            continue

    if font is None:
        # Use default font as last resort
        font = ImageFont.load_default()
        print(f"Warning: Could not load title font '{title_font_family}', using default font")

    # Calculate text size and position
    draw = ImageDraw.Draw(title_image)
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Center the text both horizontally and vertically
    text_x = (width - text_width) // 2
    text_y = (title_height - text_height) // 2

    # Draw the title text
    draw.text((text_x, text_y), title, font=font, fill=title_text_color)

    return title_image


def create_footer_row(
    width: int,
    footer_text: str,
    footer_height: int = DEFAULT_FOOTER_HEIGHT,
    footer_font_size: int = DEFAULT_FOOTER_FONT_SIZE,
    footer_font_family: str = DEFAULT_FOOTER_FONT_FAMILY,
    footer_text_color: Tuple[int, int, int, int] = FOOTER_TEXT_COLOR,
    footer_bg_color: Tuple[int, int, int, int] = FOOTER_BACKGROUND_COLOR,
    footer_left_margin: int = FOOTER_LEFT_MARGIN
) -> Image.Image:
    """
    Create a footer row image to place at the bottom of the poster.

    Args:
        width: Width of the footer row (should match poster width)
        footer_text: Footer text to display (e.g., copyright notice)
        footer_height: Height of the footer row in pixels (default: 100)
        footer_font_size: Font size for the footer (default: 30)
        footer_font_family: Font family for the footer (default: "Arial")
        footer_text_color: RGBA tuple for footer text color (default: black)
        footer_bg_color: RGBA tuple for footer background color (default: white)
        footer_left_margin: Left margin for footer text in pixels (default: 40)
        left_margin: Left margin of the poster in pixels (default: 5)
        right_margin: Right margin of the poster in pixels (default: 5)

    Returns:
        PIL Image object containing the footer row
    """
    # Create the footer image
    footer_image = Image.new("RGBA", (width, footer_height), footer_bg_color)

    # Try to load the specified font with fallback strategies
    font = None
    font_variations = [
        footer_font_family,  # Try as-is first
        f"/System/Library/Fonts/Supplemental/{footer_font_family}.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",  # Final fallback
    ]

    for font_path in font_variations:
        try:
            font = ImageFont.truetype(font_path, footer_font_size)
            break  # Success! Stop trying
        except:
            continue

    if font is None:
        # Use default font as last resort
        font = ImageFont.load_default()
        print(f"Warning: Could not load footer font '{footer_font_family}', using default font")

    # Calculate text size and position
    draw = ImageDraw.Draw(footer_image)
    text_bbox = draw.textbbox((0, 0), footer_text, font=font)
    text_height = text_bbox[3] - text_bbox[1]

    # Position text on the left with vertical centering
    text_x = footer_left_margin
    text_y = (footer_height - text_height) // 2

    # Draw the footer text
    draw.text((text_x, text_y), footer_text, font=font, fill=footer_text_color)

    return footer_image


def merge_horizontally(im1: Image.Image, im2: Image.Image, spacing: int = 0, bg_color: Tuple[int, int, int, int] = None) -> Image.Image:
    """
    Merge two images horizontally with optional spacing between them.

    Args:
        im1: First image (left)
        im2: Second image (right)
        spacing: Horizontal spacing in pixels between the images (default: 0)
        bg_color: RGBA tuple for background color (default: DEFAULT_BACKGROUND_COLOR)

    Returns:
        Merged image with spacing between im1 and im2
    """
    if bg_color is None:
        bg_color = DEFAULT_BACKGROUND_COLOR

    w = im1.size[0] + spacing + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h), bg_color)

    # Use alpha channel as mask to prevent black artifacts
    if im1.mode == 'RGBA':
        im.paste(im1, (0, 0), im1)
    else:
        im.paste(im1, (0, 0))

    if im2.mode == 'RGBA':
        im.paste(im2, (im1.size[0] + spacing, 0), im2)
    else:
        im.paste(im2, (im1.size[0] + spacing, 0))

    return im


def merge_vertically(im1: Image.Image, im2: Image.Image, spacing: int = 0, bg_color: Tuple[int, int, int, int] = None) -> Image.Image:
    """
    Merge two images vertically with optional spacing between them.

    Args:
        im1: First image (top)
        im2: Second image (bottom)
        spacing: Vertical spacing in pixels between the images (default: 0)
        bg_color: RGBA tuple for background color (default: DEFAULT_BACKGROUND_COLOR)

    Returns:
        Merged image with spacing between im1 and im2
    """
    if bg_color is None:
        bg_color = DEFAULT_BACKGROUND_COLOR

    h = im1.size[1] + spacing + im2.size[1]
    w = max(im1.size[0], im2.size[0])
    im = Image.new("RGBA", (w, h), bg_color)

    # Use alpha channel as mask to prevent black artifacts
    if im1.mode == 'RGBA':
        im.paste(im1, (0, 0), im1)
    else:
        im.paste(im1, (0, 0))

    if im2.mode == 'RGBA':
        im.paste(im2, (0, im1.size[1] + spacing), im2)
    else:
        im.paste(im2, (0, im1.size[1] + spacing))

    return im


def get_processed_image_from_path(image_path: str) -> Image.Image:
    """Process passport image: resize and crop borders."""
    pp_image = Image.open(image_path)
    bottom_crop_length = 25
    bar_width = 5

    box = (bar_width, bar_width, 705 - bottom_crop_length, 1000 - bottom_crop_length)
    resized_image = pp_image.resize((705, 1000))
    resized_image = resized_image.crop(box)

    return resized_image


def get_poster(
    images_per_row: int,
    image_paths: List[str],
    add_labels: bool = True,
    font_size: int = DEFAULT_FONT_SIZE,
    font_family: str = DEFAULT_FONT_FAMILY,
    text_color: Tuple[int, int, int, int] = TEXT_COLOR,
    bg_color: Tuple[int, int, int, int] = TEXT_BACKGROUND_COLOR,
    title: str = None,
    title_height: int = DEFAULT_TITLE_HEIGHT,
    title_font_size: int = DEFAULT_TITLE_FONT_SIZE,
    title_font_family: str = DEFAULT_TITLE_FONT_FAMILY,
    title_text_color: Tuple[int, int, int, int] = TITLE_TEXT_COLOR,
    title_bg_color: Tuple[int, int, int, int] = TITLE_BACKGROUND_COLOR,
    horizontal_spacing: int = DEFAULT_HORIZONTAL_SPACING,
    vertical_spacing: int = DEFAULT_VERTICAL_SPACING,
    background_color: Tuple[int, int, int, int] = DEFAULT_BACKGROUND_COLOR,
    footer_text: str = None,
    footer_height: int = DEFAULT_FOOTER_HEIGHT,
    footer_font_size: int = DEFAULT_FOOTER_FONT_SIZE,
    footer_font_family: str = DEFAULT_FOOTER_FONT_FAMILY,
    footer_text_color: Tuple[int, int, int, int] = FOOTER_TEXT_COLOR,
    footer_bg_color: Tuple[int, int, int, int] = FOOTER_BACKGROUND_COLOR,
    footer_left_margin: int = FOOTER_LEFT_MARGIN,
    left_margin: int = DEFAULT_LEFT_MARGIN,
    right_margin: int = DEFAULT_RIGHT_MARGIN
) -> Image.Image:
    """
    Create a poster from passport cover images.

    Args:
        images_per_row: Number of passport images per row
        image_paths: List of file paths to passport images
        add_labels: Whether to add country name labels below each passport (default: True)
        font_size: Font size for country labels (default: 40)
        font_family: Font family for country labels (default: "Arial")
        text_color: RGBA tuple for text color (default: black)
        bg_color: RGBA tuple for text label background color (default: white)
        title: Optional title text to display at the top of the poster (default: None)
        title_height: Height of the title row in pixels (default: 200)
        title_font_size: Font size for the title (default: 120)
        title_font_family: Font family for the title (default: "Helvetica-Bold")
        title_text_color: RGBA tuple for title text color (default: black)
        title_bg_color: RGBA tuple for title background color (default: white)
        horizontal_spacing: Horizontal spacing in pixels between passport images (default: 0)
        vertical_spacing: Vertical spacing in pixels between rows (default: 0)
        background_color: RGBA tuple for overall poster background color (default: very light gray)
        footer_text: Optional footer text to display at the bottom of the poster (e.g., copyright)
        footer_height: Height of the footer row in pixels (default: 100)
        footer_font_size: Font size for the footer (default: 30)
        footer_font_family: Font family for the footer (default: "Arial")
        footer_text_color: RGBA tuple for footer text color (default: black)
        footer_bg_color: RGBA tuple for footer background color (default: white)
        footer_left_margin: Left margin for footer text in pixels (default: 40)
        left_margin: Left margin of the poster in pixels (default: 5)
        right_margin: Right margin of the poster in pixels (default: 5)

    Returns:
        PIL Image object containing the assembled poster
    """
    print(f"Creating poster with {len(image_paths)} passport covers")
    num_rows = len(image_paths) / images_per_row
    print(f"Grid: {images_per_row} columns × {int(num_rows + 0.5)} rows")

    row_images = []
    elements_in_row_so_far = 0
    current_row_image = None

    for image_path in image_paths:
        country_name = get_country_name_from_path(image_path)

        # Get the processed passport image
        processed_image = get_processed_image_from_path(image_path)

        # Add text label if requested
        if add_labels:
            formatted_name = format_country_name(country_name)
            processed_image = add_text_label_to_image(
                processed_image,
                formatted_name,
                font_size=font_size,
                font_family=font_family,
                text_color=text_color,
                bg_color=background_color
            )

        # Build rows horizontally
        if current_row_image is None:
            current_row_image = processed_image
            elements_in_row_so_far = 1
        elif elements_in_row_so_far < images_per_row:
            current_row_image = merge_horizontally(current_row_image, processed_image, horizontal_spacing, background_color)
            elements_in_row_so_far += 1
        else:
            # Start new row
            row_images.append(current_row_image)
            current_row_image = processed_image
            elements_in_row_so_far = 1

    # Add the last row if it exists
    if current_row_image is not None:
        row_images.append(current_row_image)

    # Merge all rows vertically
    poster = None
    print(f"Merging {len(row_images)} rows...")
    for row_image in row_images:
        if poster is None:
            poster = row_image
        else:
            poster = merge_vertically(poster, row_image, vertical_spacing, background_color)

    # Add title row at the top if title is provided
    if title:
        print(f"Adding title: '{title}'")
        title_row = create_title_row(
            width=poster.size[0],
            title=title,
            title_height=title_height,
            title_font_size=title_font_size,
            title_font_family=title_font_family,
            title_text_color=title_text_color,
            title_bg_color=title_bg_color
        )
        # Add title row at the top
        poster = merge_vertically(title_row, poster, bg_color=background_color)

    # Add footer row at the bottom if footer_text is provided
    if footer_text:
        print(f"Adding footer: '{footer_text}'")
        footer_row = create_footer_row(
            width=poster.size[0],
            footer_text=footer_text,
            footer_height=footer_height,
            footer_font_size=footer_font_size,
            footer_font_family=footer_font_family,
            footer_text_color=footer_text_color,
            footer_bg_color=footer_bg_color,
            footer_left_margin=footer_left_margin
        )
        # Add footer row at the bottom
        poster = merge_vertically(poster, footer_row, bg_color=background_color)

    # Add left and right margins as the final step
    if left_margin > 0 or right_margin > 0:
        poster_width, poster_height = poster.size
        new_width = poster_width + left_margin + right_margin

        # Create new image with margins
        final_poster = Image.new("RGBA", (new_width, poster_height), background_color)

        # Paste the poster with left margin offset
        if poster.mode == 'RGBA':
            final_poster.paste(poster, (left_margin, 0), poster)
        else:
            final_poster.paste(poster, (left_margin, 0))

        poster = final_poster

    print(f"Poster created! Size: {poster.size[0]}×{poster.size[1]} pixels")
    return poster


def main():
    """Example usage of the poster assembly tool."""
    print("Passport Poster Assembly Tool")
    print("=" * 50)

    # Load passport paths
    print("\nLoading passport images...")
    region_to_paths = load_passport_paths()

    # Print summary
    total_passports = sum(len(paths) for paths in region_to_paths.values())
    print(f"\nFound {total_passports} passport covers:")
    for region, paths in region_to_paths.items():
        print(f"  {region}: {len(paths)} passports")

    # Example 1: Create Asia poster (7×7 grid for 49 countries) with spacing
    print("\n" + "=" * 50)
    print("Example 1: Asia Poster (7×7 grid) with 20px spacing")
    print("=" * 50)
    if "asia" in region_to_paths:
        asia_poster = get_poster(
            images_per_row=7,
            image_paths=sorted(region_to_paths["asia"]),
            add_labels=True,
            font_size=40,
            font_family="Arial",
            horizontal_spacing=20  # 20 pixels between each passport
        )

        # Save the poster
        output_path = "./produtti/asia_poster_with_labels.jpg"
        os.makedirs("./produtti", exist_ok=True)
        asia_poster.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Saved: {output_path}")

    # Example 2: Create South America poster (5×3 grid)
    print("\n" + "=" * 50)
    print("Example 2: South America Poster (5×3 grid)")
    print("=" * 50)
    if "south_america" in region_to_paths:
        sa_poster = get_poster(
            images_per_row=5,
            image_paths=sorted(region_to_paths["south_america"]),
            add_labels=True,
            font_size=35,
            font_family="Helvetica"
        )

        output_path = "./produtti/south_america_poster_with_labels.jpg"
        sa_poster.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Saved: {output_path}")

    # Example 3: Create World poster (23×10 grid for standard print sizes) with title
    print("\n" + "=" * 50)
    print("Example 3: World Poster (23×10 grid) - 36\"×24\" Landscape")
    print("=" * 50)
    all_paths = []
    for paths in region_to_paths.values():
        all_paths.extend(paths)

    world_poster = get_poster(
        images_per_row=20,
        image_paths=sorted(all_paths, key=lambda x: x.split("/")[-1]),
        add_labels=True,
        font_size=60,
        font_family="Arial",
        horizontal_spacing=20,
        vertical_spacing=8,
        title="Passports of the World",
        title_height=1000,
        title_font_size=1000,
        title_font_family="LithosPro-Regular",
        footer_text="© 2026. All rights reserved.",
        footer_height=60,
        footer_font_size=26,
        footer_font_family="SF-Pro-Display-Bold",
        footer_text_color=(0, 0, 0, 255),
        footer_bg_color=(255, 255, 255, 255),
        footer_left_margin=40,
        left_margin=10,
        right_margin=10
    )

    output_path = "./produtti/world_poster_with_labels.jpg"
    world_poster.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Saved: {output_path}")

    print("\n" + "=" * 50)
    print("Done! Check the ./produtti/ folder for output files.")
    print("=" * 50)


if __name__ == "__main__":
    main()
