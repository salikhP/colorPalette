from bs4 import BeautifulSoup
import json

with open("./html/colorhunt_palettes_rendered.html", "r", encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

palette_items = soup.find_all('div', class_='item')

palette_list = []
palette_count = 0

for item in palette_items:
    palette = item.find('div', class_='palette')

    if palette is None:
        continue

    colors = []
    for color_div in palette.find_all('div', class_='place'):
        color_code = color_div.find('span').text.strip()
        if color_code != '':
            colors.append(color_code)

    if len(colors) == 4:
        palette_list.append(colors)
        palette_count += 1

with open("./parsed_palettes/palettes.json", "w", encoding='utf-8') as file:
    json.dump(palette_list, file, indent=4)
print("Palettes are saved to parsed_palettes/palettes.json")
