from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'Il file {event.src_path} è stato modificato')

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    # Se desideri monitorare anche la creazione di nuovi file, dovrai impostare recursive=True
    observer.schedule(event_handler, path='percorso_del_tuo_file', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
