import os
import requests
from bs4 import BeautifulSoup
import random
import time
import sys

def slowprint(text, delay=1./400):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def download_image(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def rename_images(folder):
    for filename in os.listdir(folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            new_name = f"{random.randint(1000000, 9999999)}.jpg"
            os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
            print(f"Renamed {filename} to {new_name}")

def parse_pages(pages_input):
    pages = set()  
    for part in pages_input.split():
        if '-' in part:  
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))  
        else:
            pages.add(int(part))  
    return sorted(pages)  

def get_images(tag, character, pages, folder_name):
    base_url = "https://yande.re/post"
    folder = create_folder(folder_name)

    for page in pages:
        params = {'page': page}
        if tag or character:
            params['tags'] = (tag + ' ' + character).strip()

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            images = soup.find_all('a', class_='directlink largeimg')
            for img in images:
                download_image(img['href'], folder)
        else:
            print(f"Failed to retrieve page {page}.")
    
    rename_images(folder)
    print(" ")
    slowprint("All images have been downloaded.")

def main():
    try:
        os.system("clear")
        print("\033[1;36m")
        os.system("figlet yande.re fetch")
        slowprint("\033[1;36m ==============================================")
        slowprint(" ")
        tag = input("Enter tags (e.g. swimsuits, ass, etc.): ").strip()
        character = input("Enter characters (e.g. hatsune_miku, kagamine_rin, etc.): ").strip()

        pages_input = input("Enter pages (e.g. 1 3 5 or 1-5 | default is 1 page): ").strip()
        if not pages_input:
            pages = [1]  
        else:
            pages = parse_pages(pages_input)

        folder_name = input("Enter folder name (or press Enter for default 'images'): ").strip()
        if not folder_name:
            folder_name = "images"

        folder_name = os.path.join(os.getcwd(), folder_name)

        print(f"\nScraping images with tags '{tag}' and characters '{character}' from yande.re...\n")
        get_images(tag, character, pages, folder_name)

        print("Download completed successfully!")

    except KeyboardInterrupt:
        slowprint(" ")
        slowprint(" ")
        slowprint("\033[1;36m ==============================================")
        os.system("figlet exiting")
        slowprint("\033[1;36m ==============================================")
        slowprint(" ")
        sys.exit()
if __name__ == "__main__":
    main()

