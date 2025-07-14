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

## Utilizzo
### profili già esistenti
* acquirente_1
* acquirente_2
* acquirente_3
* venditore_elettronica
* venditore_cancelleria
* venditore_cibo

password identica per tutti i profili: **passwordEcommerce** 

### codici per aggiungere credito
* 4a44dc15364204a80fe80e9039455cc1608281820fe2b24f1e5233ade6af1dd5: valore 10
* f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b: valore 20
* 1a6562590ef19d1045d06c4055742d38288e9e6dcd71ccde5cee80f1d5a774eb: valore 50 
* ad57366865126e55649ecb23ae1d48887544976efea46a48eb5d85a6eeb4d306: valore 100 
* 27badc983df1780b60c2b3fa9d3a19a00e46aac798451f0febdca52920faaddf: valore 200 
* 0604cd3138feed202ef293e062da2f4720f77a05d25ee036a7a01c9cfcdd1f0a: valore 500


 