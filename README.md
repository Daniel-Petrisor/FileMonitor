# FileMonitor
## Monitorare le modifiche a un file di testo in una rete aziendale.


Utilizzare la libreria watchdog per monitorare più file o anche intere directory
Watchdog fornisce un PollingObserver che controlla attivamente i file per le modifiche invece di fare affidamento sugli eventi del file system.
Questo può essere più affidabile per i file di rete, ma potrebbe anche essere più lento o utilizzare più risorse del sistema rispetto al metodo standard.
Se vuoi monitorare più file, puoi semplicemente chiamare il metodo schedule più volte, una volta per ogni file che vuoi monitorare.
Se vuoi monitorare un’intera directory e tutti i suoi sottodirectory, 
puoi passare il percorso della directory al metodo schedule e impostare il parametro recursive su True.




Questo script stampa un messaggio ogni volta che il file specificato viene modificato.

1. Installare la libreria watchdog
    `pip install watchdog`

1.  Sostituire 'percorso_del_tuo_file' con il percorso del file che desideri monitorare.

