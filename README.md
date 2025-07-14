# E-commerce
Progetto e-commerce per acquistare prodotti su una piattaforma online. 


## Utenti
Gli utenti vengono divisi in "Acquirenti" e "Venditori" su cui vengono applicati permessi per limitare le operazioni che possono effettuare.
Il ruolo viene deciso in fase di registrazione.

### Utenti non autenticati
Gli utenti non autenticati possono effettuare solamente operazioni di ricerca.

### Acquirenti
- **Ordini**: possono effettuare acquisti e verranno memorizzati dentro agi ordini.
Per gli ordini effettuati è possibile lasciare una valutazione che attribuirà un voto ed un commento visualizzati nella pagina dell'articolo.
- **Carrello**: gli articoli possono essere aggiunti in un carrello, possono essere tolti in automatico quando avviene un acquisto oppure tramite bottone nella pagina della visualizzazione.
- **Profilo**: vengono visualizzati i dati dell'Acquirente, modificabili.
- **Portafoglio**: nella pagina profilo è possibile accedere alla pagina di ricarica credito, in cui inserendo il codice di una carta è possibile ricaricare il credito del portafoglio (il codice per semplicità è il codice hash256 dei valori delle banconote da 10-500)

### Venditori
- **Articoli**: visualizzare gli articoli aggiunti dal venditore, aggiungere articoli e relative immagini e modificarle. Vi è un bottone per eliminare un articolo ma non viene eliminato dal db ma messo a True un flag di visibilità per garantire la rintracciabilità del venditore di ogni articolo venduto.
- **Carrello**: gli articoli possono essere aggiunti in un carrello, possono essere tolti in automatico quando avviene un acquisto oppure tramite bottone nella pagina della visualizzazione.
- **Profilo**: vengono visualizzati i dati dell'Acquirente, modificabili.