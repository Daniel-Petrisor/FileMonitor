from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import os
import time
from datetime import datetime



file_path = 'D:/Github/FileMonitor/Current.txt'

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        now = datetime.now()                                    # Ottieni l'ora corrente
        now_str = now.strftime("%d/%m/%Y, %H:%M:%S")            # Formatta l'ora come stringa
        print("File modificato: ",now_str, event.src_path)      # Stampiamo il percorso del file che è stato modificato

        # Controlliamo se il percorso modificato è un file
        if os.path.isfile(event.src_path):
            try:
                # Apriamo il file in modalità lettura
                with open(event.src_path, 'r') as file:        # Leggiamo e stampiamo il contenuto del file
                    print(file.read())

            except Exception as e:
                print(f"Si è verificato un errore durante la lettura del file: {e}")





if __name__ == "__main__":
    event_handler = MyHandler()

    # Creiamo un'istanza dell'Observer di watchdog
    # observer = Observer() # Metodo standard per monitorare i file system del sistema locale
    observer = PollingObserver() # Metodo per monitorare i file su una rete locale
    observer.schedule(event_handler, path=file_path, recursive=False)

    # Se desideri monitorare anche la creazione di nuovi file, oppure un'intera directory, dovrai impostare recursive=True
    # observer.schedule(event_handler, path='path_to_your_directory', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
