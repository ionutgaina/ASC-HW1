Ionuț Găină 334CD

# Tema 1 - Le Stats Sportif

## Introducere

Ca idee generală cum funcționează serverul este în felul următor:

- Am modularizat serverul în 3 clase principale: `ThreadPool`, `DataIngestor`, `TaskService` și `Routes`.

- `ThreadPool` este clasa care se ocupă de alocarea și gestionarea thread-urilor. Aceasta are un număr fix de thread-uri și un buffer de task-uri. Când un task este adăugat în buffer, thread-urile care sunt deja pornite îl vor prelua și îl vor executa (dacă nu s-a dat request de shutdown).

- `DataIngestor` este clasa care se ocupă de citirea datelor din csv și de stocarea întrebărilor speciale pentru best5 și worst5.

- `TaskService` este clasa unde se află metodele care se ocupă de procesarea datelor și de generarea răspunsurilor.


## Implementare

### ThreadPool

- `ThreadPool` la inițializare pornește un număr de thread-uri și un buffer de task-uri. Thread-urile sunt pornite și așteaptă să preia task-uri din coadă. Dacă coada este goală, thread-urile așteaptă până când un task este adăugat.

- Avem implementată și o listă de task-uri, pentru a putea ține evidența ce task-uri au trecut prin server.

- În `ThreadPool` ne ocupăm și de shutdown-ul serverului. Când se dă comanda de shutdown, thread-urile sunt oprite și se așteaptă ca toate task-urile să fie terminate.

- Pentru a adăuga un task în coadă, folosim `add_task` care adaugă task-ul în coadă, dacă nu s-a dat comanda de shutdown.

- Penntru a da comanda de shutdown, folosim `shutdown` care setează flag-ul de shutdown și așteaptă ca toate task-urile să fie terminate.

#### TaskRunner

- `TaskRunner` este clasa care se ocupă de rularea task-urilor. Aceasta primește un task și îl execută folosind metoda `execute` din task, rezultatul fiind stocat într-un fișier.

#### Task

- `Task` este clasa din care se derivă toate task-urile. Aceasta are metoda `execute` care este executată în TaskRunner, am folosit această abordare pentru a putea extinde funcționalitatea serverului cu ușurință, în plus să pot avea o altă clasă care se va ocupa de logica task-urilor.

### DataIngestor

- Citirea datelor din csv, ce se face în constructorul clasei `DataIngestor` este făcută folosind `pandas` pentru a citi datele din csv și a le stoca într-un dataframe. Am folosit această abordare pentru a putea accesa datele mai ușor și să pot face operații pe ele mai rapid.


### TaskService

- `TaskService` este clasa care se ocupă de procesarea datelor și de generarea răspunsurilor. Aceasta are metode pentru fiecare tip de task.

- Am folosit această clasă pentru a putea extinde funcționalitatea serverului cu ușurință și pentru a păstra codul mai organizat.

- Pentru fiecare task am implementat o metodă care primește datele necesare și returnează un răspuns.

### Routes

- `Routes` este clasa care se ocupă de rutarea request-urilor. Aceasta primește un request și îl procesează, apoi returnează un răspuns. Aici se crează un Task cu argumente uncția care trebuie executată și datele necesare din request, apoi se adaugă în coada de task-uri a ThreadPool-ului.


### Logging

- Pentru logging am creat câte un log pentru fiecare request, la începutul request-ului și la sfârșitul lui. Acest lucru l-am făcut pentru a putea urmări mai ușor ce se întâmplă în server și pentru a putea identifica mai ușor eventuale probleme.

- În metodele procesării task-urilor am folosit logging pentru a putea urmări mai ușor ce se întâmplă în server. Am folosit doar la începutul metodei, întrucât consider că este suficient să văd rezultatul final la sfârșitul request-ului și să nu umplu log-ul cu informații duplicate.

### Testare

- Testele unitare sunt făcute pentru fiecare task `TaskService`-ului. Acestea verifică dacă rezultatul întors de metodele de procesare a task-urilor este corect.

- Pentru testare puteți folosi comanda `python -m unittest test_services.py` în directorul `unittests`.

## Feedback

- Tema mi s-a părut foarte faină întrucât am putut să lucrez cu multe concepte noi, cum ar fi logging, unittesting și cel mai important să înțeleg cum funcționează un server.

- Am avut câteva probleme la început cu logging-ul, fiind ceva nou pentru mine și în enunțul temei nu erau specificate prea multe detalii despre cam ce ar trebui să conțină log-ul, de aceea sper că am înțeles corect ce trebuia să fac.

- Ca sugestie pentru viitoarele teme, aș sugera să se adauge mai multe detalii, fiind concepte noi pentru mulți dintre noi și chiar ar fi fain să înțelegem cum trebuie făcute lucrurile corect.