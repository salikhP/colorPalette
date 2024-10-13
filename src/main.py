import cv2
import numpy as np
import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from itertools import permutations

def rgb_to_hex(color: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def euclidean_distance(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

def find_dominant_colors(image_path: str, num_colors: int = 4) -> list[str]:
    """
    Finds the dominant colors in an image using K-means clustering.

    :param str image_path: The file path to the image.
    :param int num_colors: The number of dominant colors to find, default is 4.
    :return: A list of dominant colors in hexadecimal string format.
    :rtype: list[str]
    """

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_

    return [rgb_to_hex(color) for color in dominant_colors]

def find_closest_palette(dominant_colors: list[str], palettes: list[list[str]]) -> list[str]:
    """
    Find the closest palette to the dominant colors.

    :param list[str] dominant_colors: List of 4 dominant colors from an image in hex format.
    :param list[list[str]] palettes: 2-dimensional list of palettes, each containing 4 colors in hex format.
    :return: The closest palette as a list of hex color strings.
    :rtype: list[str]
    """

    # hexadecimal -> decimal
    dominant_rgb = [tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) for color in dominant_colors]
    min_distance = float('inf')
    closest_palette = None

    for palette in palettes:
        # hexadecimal -> decimal
        palette_rgb = [tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) for color in palette]

        # 24 unique pairings
        for perm in permutations(palette_rgb):
            # match comparison one-to-one
            total_distance = sum(euclidean_distance(dominant_rgb[i], perm[i]) for i in range(4))

            # choose the palette with the minimum sum of each euclidian distance
            if total_distance < min_distance:
                min_distance = total_distance
                closest_palette = palette

    return closest_palette

def display_palette(palette: list[str], title: str) -> None:
    fig, ax = plt.subplots(figsize=(4, 1))
    fig.subplots_adjust(top=0.7)
    ax.set_title(title, loc='center')
    for i, color in enumerate(palette):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.show()

image_dominant_colors = find_dominant_colors(image_path="images/pancake_input.png")

palette_file_path = "parsers/parsed_palettes/palettes.json"
with open(palette_file_path, "r") as file:
    palettes = json.load(file)

closest_palette = find_closest_palette(image_dominant_colors, palettes)

# print result in hex code
print("Dominant colors in the image:", image_dominant_colors)
print("Closest palette is:", closest_palette)

# display as color blocks
display_palette(image_dominant_colors, "Dominant Colors")
display_palette(closest_palette, "Closest Palette")
