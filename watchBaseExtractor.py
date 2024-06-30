import requests
import re
from bs4.element import Comment
from bs4 import BeautifulSoup
import time

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# First part of the code
url = "https://watchbase.com/omega/seamaster-diver-300m"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Host": "watchbase.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1",
    "Te": "trailers",
    "Connection": "close"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
texts = soup.findAll(text=True)
visible_texts = filter(tag_visible, texts)
text = '\n'.join(visible_texts)
texts = text.split('\n')
urls = []
for t in texts:
    if t == '' and t == '': continue
    elif t[0].isnumeric(): urls.append(t)
print(urls)
time.sleep(10)
main_json=[]
# Second part of the code
for url in urls:
    try:
        modified = url.replace('.', '-')
        full_url = "https://watchbase.com/omega/seamaster-diver-300m/" + modified
        # Fetching watch information
        response = requests.get(full_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        text = '\n'.join(visible_texts)

        # Extracting individual fields
        brand_match = re.search(r'Brand:\s*(.*)', text)
        brand = brand_match.group(1).strip() if brand_match else "Not Found"

        family_match = re.search(r'Family:\s*(.*)', text)
        family = family_match.group(1).strip() if family_match else "Not Found"

        reference_match = re.search(r'Reference:\s*(.*?)Name:', text, re.DOTALL)
        reference = reference_match.group(1).strip() if reference_match else "Not Found"

        name_match = re.search(r'Name:\s*(.*?)Movement', text, re.DOTALL)
        name = name_match.group(1).strip() if name_match else "Not Found"

        movement_match = re.search(r'Movement:\s*(.*?):', text, re.DOTALL)
        movement = movement_match.group(1).strip() if movement_match else "Not Found"

        produced_match = re.search(r'Produced:\s*(.*)', text)
        produced = produced_match.group(1).strip() if produced_match else "Not Found"

        limited_match = re.search(r'Limited:\s*(.*)', text)
        limited = limited_match.group(1).strip() if limited_match else "Not Found"

        material_match = re.search(r'Material:\s*(.*)', text)
        material = material_match.group(1).strip() if material_match else "Not Found"

        bezel_match = re.search(r'Bezel:\s*(.*)', text)
        bezel = bezel_match.group(1).strip() if bezel_match else "Not Found"

        glass_match = re.search(r'Glass:\s*(.*)', text)
        glass = glass_match.group(1).strip() if glass_match else "Not Found"

        back_match = re.search(r'Back:\s*(.*)', text)
        back = back_match.group(1).strip() if back_match else "Not Found"

        shape_match = re.search(r'Shape:\s*(.*)', text)
        shape = shape_match.group(1).strip() if shape_match else "Not Found"

        diameter_match = re.search(r'Diameter:\s*(.*)', text)
        diameter = diameter_match.group(1).strip() if diameter_match else "Not Found"

        lug_width_match = re.search(r'Lug Width:\s*(.*)', text)
        lug_width = lug_width_match.group(1).strip() if lug_width_match else "Not Found"

        w_r_match = re.search(r'W/R:\s*(.*)', text)
        w_r = w_r_match.group(1).strip() if w_r_match else "Not Found"

        color_match = re.search(r'Color:\s*(.*)', text)
        color = color_match.group(1).strip() if color_match else "Not Found"

        indexes_match = re.search(r'Indexes:\s*(.*)', text)
        indexes = indexes_match.group(1).strip() if indexes_match else "Not Found"

        finish_match = re.search(r'Finish:\s*(.*)', text)
        finish = finish_match.group(1).strip() if finish_match else "Not Found"

        hands_match = re.search(r'Hands:\s*(.*)', text)
        hands = hands_match.group(1).strip() if hands_match else "Not Found"

        # Fetching price information
        price_url = full_url + "/prices"
        price_response = requests.get(price_url, headers=headers)
        data = price_response.json()
        labels = data['labels'] if 'labels' in data else []
        prices = data['datasets'][0]['data'] if 'datasets' in data and data['datasets'] else []

        # Constructing the watch_info dictionary
        watch_info = {
            "Brand": brand,
            "Family": family,
            "Reference": reference,
            "Name": name,
            "Movement": movement,
            "Produced": produced,
            "Limited": limited,
            "Material": material,
            "Bezel": bezel,
            "Glass": glass,
            "Back": back,
            "Shape": shape,
            "Diameter": diameter,
            "Lug Width": lug_width,
            "W/R": w_r,
            "Color": color,
            "Indexes": indexes,
            "Finish": finish,
            "Hands": hands,
            "Labels": labels,
            "Prices": prices
        }
        print(watch_info)
        main_json.append(watch_info)
        #There is rate limiter thats why having a gap makes sense and to avoid rate limiters use proxies servers and add like this
        # request.get(url=url,headers=header,proxies=proxy)
        time.sleep(5)
    except Exception as e:
        print(f"Error processing {url}: {e}")
time.sleep(10)
import csv,json

output_csv_file = "omega_watches_2.csv"

# Extracting headers dynamically from the first JSON object
headers = main_json[0].keys()

# Writing JSON data to CSV
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for watch_data in main_json:
        writer.writerow(watch_data)

print(f"CSV file '{output_csv_file}' has been successfully created.")
