from queue import Queue
from threading import Thread, Event
import time

# * creați un nr de threaduri (pool-ul)
# * threadurile partajează obiectele de sincronizare și notificare, plus o structură de date prin care își partajează joburile pe care le au de prelucrat
# * fiecare thread, într-un loop infinit verifică dacă există un job în pending (în structura aia de mai sus)
# - dacă da, procesează jobul și salvează rezultatul
# - dacă nu, așteaptă până este ceva disponibil
# - rinse & repeat
# * la un moment dat, o să vină un shutdown care va notifica threadurile că trebuie să termine execuția

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        pass

class TaskRunner(Thread):
    def __init__(self):
        # TODO: init necessary data structures
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
