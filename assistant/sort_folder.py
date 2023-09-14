import os
import shutil
import sys
from pathlib import Path

# Список розширень для кожної категорії
IMAGE_EXTENSIONS = ('JPEG', 'JPG', 'PNG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENT_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR')

# Папки для кожної категорії
CATEGORIES = {
    'images': IMAGE_EXTENSIONS,
    'video': VIDEO_EXTENSIONS,
    'documents': DOCUMENT_EXTENSIONS,
    'audio': AUDIO_EXTENSIONS,
    'archives': ARCHIVE_EXTENSIONS
}

# Список всіх відомих розширень
KNOWN_EXTENSIONS = set(
    ext for exts in CATEGORIES.values() for ext in exts
)

def normalize(name: str) -> str:
    # Функція для нормалізації імені файлу або папки
    name = name.translate(str.maketrans('', '', r'\/:*?"<>|'))  # Видаляємо заборонені символи
    name = name.encode('ascii', 'ignore').decode('utf-8')  # Транслітерація та видалення некоректних символів
    name = '_'.join(name.split())  # Заміна пробілів на підкреслення
    return name

def sort_folder(folder_path: str) -> None:
    folder = Path(folder_path)
    for item in folder.iterdir():
        if item.is_dir() and item.name not in CATEGORIES:
            sort_folder(item)
        else:
            ext = item.suffix[1:].upper()
            category = None

            if ext in KNOWN_EXTENSIONS:
                for cat, exts in CATEGORIES.items():
                    if ext in exts:
                        category = cat
                        break

            if category:
                target_folder = folder / category
                target_folder.mkdir(parents=True, exist_ok=True)
                target_name = normalize(item.name)
                target_path = target_folder / target_name

                # Додавання підкаталогу для архівів
                if category == 'archives':
                    target_name_without_ext = os.path.splitext(target_name)[0]
                    target_path = target_folder / target_name_without_ext
                    target_path.mkdir(parents=True, exist_ok=True)

                item.rename(target_path)
            else:
                # Розширення невідоме, перейменовуємо і переміщуємо до папки "unknown"
                target_name = normalize(item.name)
                unknown_folder = folder / 'unknown'
                unknown_folder.mkdir(parents=True, exist_ok=True)
                target_path = unknown_folder / target_name
                item.rename(target_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        return

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    sort_folder(folder_path)
    print("Sorting completed.")

if __name__ == "__main__":
    main()