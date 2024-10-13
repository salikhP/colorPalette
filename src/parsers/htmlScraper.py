import requests

url = 'https://colorhunt.co/palettes/random'
response = requests.get(url)
response.raise_for_status()

with open('colorhunt_palettes.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

print('page html fetched successfully')
