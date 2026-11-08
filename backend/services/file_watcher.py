from watchdog.observers import Observer
from threading import Lock
from watchdog.events import FileSystemEventHandler
import time
import os
from .state import State

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_paths, list_lock):
        self.file_paths=file_paths
        self.list_lock=list_lock

    def on_created(self, event):
        if not event.is_directory:
            file_path=os.path.abspath(event.src_path)
            with self.list_lock:
                self.file_paths.append(file_path)

def monitor_folder(state:State,folder_path="../data/incoming"):
    file_paths=[]
    list_lock= Lock()
    target_dir=os.path.abspath(folder_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    event_handler= FileEventHandler(file_paths, list_lock)
    observer= Observer()
    observer.schedule(event_handler, target_dir, recursive=False)
    observer.start()
    print(f"Monitoring folder: {target_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    state['file_path_list']=file_paths
    return file_paths

print("Starting folder monitoring...")
file_path_list= monitor_folder()
for file_path in file_path_list:
    print(f"New file detected: {file_path}")
