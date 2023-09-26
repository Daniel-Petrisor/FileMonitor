# Import delle librerie necessarie
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import os
import time
from datetime import datetime
import csv
import json
from rich import print # Opzionale


# Definizione dei percorsi dei file e dei file JSON di output
file_path_1 = 'D:/Github/FileMonitor/Current.txt'
out_json_prod1 = "D:/Github/FileMonitor/data_prod.json"

# Classe che estende FileSystemEventHandler per gestire gli eventi del file system
class MyHandler(FileSystemEventHandler):

    def process_file(self, event):
        # Apertura del file in modalità lettura
        with open(event.src_path, 'r') as f:
            # Lettura del contenuto del file come CSV
            reader = csv.reader(f)
            result_dict = {
                "logger": {
                    "path": event.src_path,
                    "datetime": datetime.fromtimestamp(os.path.getmtime(event.src_path)).strftime('%d/%m/%Y %H:%M:%S'),
                    "sensors": []
                }
            }

            for row in reader:
                sensor_data = {
                    "name": row[1],
                    "value": float(row[2] + '.' + row[3]),
                }
                result_dict["logger"]["sensors"].append(sensor_data)

            print(result_dict)

            # Determina il file JSON di output basato sul percorso del file sorgente
            out_json = None
            if event.src_path == file_path_1:
                out_json = out_json_prod1
            # elif event.src_path == file_path_prod2:
            #     out_json = out_json_prod2
            # elif event.src_path == file_path_prod3:
            #     out_json = out_json_prod3

            # Scrittura dei dati processati nel file JSON
            with open(out_json, 'a') as json_file:
                json.dump(result_dict, json_file)
                json_file.write(',\n')



     # Metodo chiamato quando un file viene modificato
    def on_modified(self, event):
        # Ottieni l'ora corrente
        now = datetime.now()
        # Formatta l'ora come stringa
        now_str = now.strftime("%d/%m/%Y, %H:%M:%S")
        # Stampa il percorso del file modificato e l'ora corrente
        print("File modificato: ", now_str, event.src_path)

        # Controlla se il percorso modificato è un file
        if os.path.isfile(event.src_path):
            try:
                # Processa il file modificato
                self.process_file(event)
            except Exception as e:
                print(f"[red]Si è verificato un errore durante la lettura del file:[/red] {e}")




# Punto di ingresso principale del programma
if __name__ == "__main__":
    # Crea un'istanza del gestore degli eventi
    event_handler = MyHandler()

    # Creiamo un'istanza dell'Observer di watchdog
    # observer = Observer() # Metodo standard per monitorare i file system del sistema locale
    observer = PollingObserver() # Metodo per monitorare i file su una rete locale

    # Programma l'Observer per monitorare i percorsi specificati con il gestore degli eventi
    observer.schedule(event_handler, path=file_path_1, recursive=False)

    # Se desideri monitorare anche la creazione di nuovi file, oppure un'intera directory, dovrai impostare recursive=True
    # observer.schedule(event_handler, path='path_to_your_directory', recursive=True)

    # Avvia l'Observer
    observer.start()

    try:
        while True:
            print("[italic red]In attesa della modifica del file[/italic red]")
            # Metti in pausa il ciclo per 5 secondi ad ogni iterazione per evitare sovraccarichi della CPU
            time.sleep(5)
    except KeyboardInterrupt:
        # Se l'utente interrompe il programma con Ctrl+C, ferma l'Observer
        observer.stop()

    # Aspetta che l'Observer termini prima di uscire dal programma    
    observer.join()
