import os
import re
import json

ROOT_DIR = r"c:\Users\hsini\Desktop\website manga projects\Soul Land - Legend of The Gods' Realm"
MANGA_DIR = os.path.join(ROOT_DIR, "manga", "Soul Land")

def extract_chapter_number(folder_name):
    match = re.search(r'Ch\.(\d+(\.\d+)?)', folder_name)
    return float(match.group(1)) if match else 0

def extract_chapter_title(folder_name):
    match = re.match(r'Ch\.\d+\s*-?\s*(.*)', folder_name)
    if match and match.group(1).strip():
        return match.group(1).strip()
    return ""

def get_images(folder_path):
    extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    images = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)):
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions:
                images.append(f)
    def natural_key(s):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
    images.sort(key=natural_key)
    return images

def generate_json():
    folders = [f for f in os.listdir(MANGA_DIR) if os.path.isdir(os.path.join(MANGA_DIR, f)) and re.match(r'Ch\.\d+', f)]
    chapters = []
    for folder in folders:
        num = extract_chapter_number(folder)
        title = extract_chapter_title(folder)
        imgs = get_images(os.path.join(MANGA_DIR, folder))
        chapters.append({
            'num': num,
            'folder': folder,
            'title': title,
            'images': imgs,
            'thumb': imgs[0] if imgs else ''
        })
    chapters.sort(key=lambda x: x['num'])
    
    output_path = os.path.join(ROOT_DIR, "soul-land-app", "src", "lib", "chapters.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=2)
    print(f"Generated {len(chapters)} chapters in {output_path}")

if __name__ == "__main__":
    generate_json()
