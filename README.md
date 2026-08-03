# multi-agent-monitoring

Questo progetto implementa una simulazione di monitoraggio e di esplorazione marittima cooperativa tramite una flotta di agenti autonomi. Di seguito sono descritte la struttura dei file del software e le scelte implementative future del sistema.

---

## Struttura del Progetto

Il codice è suddiviso in moduli indipendenti, ciascuno dei quali racchiude funzioni fondamentali per il funzionamento della simulazione:

*   **`agent.py`**: Contiene la definizione della classe degli agenti e i metodi per il campionamento delle posizioni, la pianificazione locale e l'esecuzione del movimento.
*   **`environment.py`**: Contiene la classe `Map` e le funzioni necessarie per gestire lo stato della griglia (compreso il decadimento dei valori nel tempo) e il calcolo complessivo della copertura (*coverage value*).
*   **`main.py`**: Rappresenta il workflow principale della simulazione. Gestisce l'avanzamento del tempo e la generazione del file di log contenente i dati grezzi della simulazione.
*   **`plots.py`**: Contiene le funzioni di utilità grafica utilizzate per produrre tabelle riassuntive e grafici dell'andamento temporale della copertura.
*   **`renderer.py`**: Contiene i metodi per generare il video della simulazione (in formato `.mp4`), salvando inoltre singoli fotogrammi significativi (*key frames*).
*   **`analyze.py`**: Gestisce il flusso di post-processing. Legge i dati di log esportati dal simulatore per generare in modo centralizzato grafici, tabelle e file video.
*   **`bresenham_utilis.py`**: Contiene l'implementazione dell'algoritmo classico di Bresenham e le relative funzioni applicate al sistema:
    *   *is_path_free*: Impedisce ai robot di compiere uno spostamento rettilineo che attraversi o scavalchi la terraferma.
    *   *get_visible_cells*: Impedisce al sensore di rilevare celle posizionate al di là di barriere terrestri, simulando ombre visive realistiche.
*   **`costants.py`**: Raccoglie tutte le costanti di configurazione, i parametri dell'ambiente e le specifiche fisiche dei robot.

---

## Sviluppi Futuri e Scelte Implementative

### 1. Partenza casuale degli agenti
*   **Stato attuale**: Viene  estratta una posizione  casuale all'interno di un'area sferica definita dalla costante `AGENT_START_RADIUS`, l'estrazione è eseguita col codice `random.choice()`, che non segue una distribuzione normale, ma una distribuzione uniforme.
*   **Sviluppo futuro**: Implementazione di un sistema che estragga le posizioni iniziali degli agenti secondo una distribuzione normale. Questa soluzione implica due alternative:
    1.   Generare seguendo una distribuzione normale le coordinate x e y, e successivamente verificare che la posizione generata cada all'interno del raggio definito da `AGENT_START_RADIUS`, e che non sia già stata scelta.
    2.   Utilizzare il metodo citato in precedenza passando come parametro la distribuzione normale, questo implica la definizione della distribuzione normale da utilizzare.
### 2. Gestione dei Pareggi di Copertura
*   **Stato attuale**: Non è prevista nessuna gestione in caso di valori di copertura identici tra più celle candidate, durante la scelta della prossima destinazione dell'agente.
*   **Nota**: In caso di pareggio di copertura, l'agente sceglie la prima cella candidata in ordine di scansione della griglia. L'agente si muove solamente se
trova una cella che restituisce un valore di copertura maggiore di quello della cella corrente.
* **Sviluppo futuro**: Implementazione di un sistema che gestisca i pareggi di copertura.
### 3. Introduzione grandezza fisica velocità degli agenti
*   **Stato attuale**: Gli agenti adesso si muovono di una casella ogni turno di simulazione, ogni turno di simulazione corrisponde a 5 secondi nella realtà, coincidendo con il movimento
* degli agenti rispetto ai pixel che campionano 10 x 10 metri della superificie reale. Gli agenti sono una macchina a stati e agiscono indipendentemente ricalcolando la prossima  tappa 
* ogni qual volta raggiungono la destinazione.
