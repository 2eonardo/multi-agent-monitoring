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

### 1. Posizione di Partenza degli Agenti (Spawn)
*   **Stato attuale**: Gli agenti iniziano la simulazione da un unico punto fisso definito all'interno di `costants.py`.
*   **Sviluppo futuro**: Possibile implementazione  di un sistema di partenze casuali degli agenti da celle di mare non sovrapposte.
### 2. Gestione dei Pareggi di Copertura
*   **Stato attuale**: Non è prevista nessuna gestione in caso di valori di copertura identici tra più celle candidate, durante la scelta della prossima destinazione dell'agente.
*   **Nota**: In caso di pareggio di copertura, l'agente sceglie la prima cella candidata in ordine di scansione della griglia. L'agente si muove solamente se
trova una cella che restituisce un valore di copertura maggiore di quello della cella corrente.
* **Sviluppo futuro**: Implementazione di un sistema che gestisca i pareggi di copertura.
### 3. Flusso di Coordinamento della Simulazione
*   **Simulazione Simultanea (Attuale)**: Il ciclo corrente prevede che ogni robot calcoli la propria destinazione in base allo stato iniziale del turno. Successivamente, tutti i movimenti vengono applicati contemporaneamente.
Così facendo, nessun agente è a conoscenza delle decisioni degli altri nello stesso istante.
*   **Simulazione Sequenziale (Precedente)**: Inizialmente i robot pianificavano ed eseguivano la propria mossa uno dopo l'altro nello stesso turno. In questo scenario, gli agenti che agivano per ultimi possedevano già l'informazione aggiornata sulla mossa dei compagni.

