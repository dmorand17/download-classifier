import logging
import os
import shutil
import sys

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

downloads_folder = None
if len(sys.argv) > 1:
    downloads_folder = sys.argv[-1]
else:
    print("Must provide a folder to watch (e.g. '/Users/someuser/Downloads')")
    sys.exit()

logging.basicConfig(filename="classification.log", level=logging.INFO)

# Log to console
logging.getLogger().addHandler(logging.StreamHandler())

folders = {
    "images": [".jpg", ".png", ".svg"],
    "documents": [".pdf", ".docx"],
    "datasets": [".xlsx", ".csv", ".json", ".xml"],
    "other": [],
}


class ClassificationHandler(FileSystemEventHandler):
    def __init__(self, folders, downloads_folder):
        self.folders = folders
        self.downloads_folder = downloads_folder

    def on_created(self, event):
        if event.is_directory:
            return None
        file_path = event.src_path
        file_extension = os.path.splitext(file_path)[1]
        for folder_name, exts in self.folders.items():
            if file_extension in exts:
                folder_path = os.path.join(self.downloads_folder, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                logging.info(f"Moving '{file_path}' -> '{folder_path}'")
                shutil.move(file_path, folder_path)


logging.info(f"Monitoring {downloads_folder}...")

event_handler = ClassificationHandler(folders, downloads_folder)
observer = Observer()
observer.schedule(event_handler, downloads_folder, recursive=True)
observer.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()
