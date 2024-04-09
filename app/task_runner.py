from queue import Queue
from threading import Thread, Event
import time
import os

from flask import Response, json

class ThreadPool:
    def __init__(self, app=None):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.nr_threads = os.environ.get('TP_NUM_THREADS')
        if not self.nr_threads:
            self.nr_threads = os.cpu_count()
            
        self.task_queue = Queue()
        self.threads = [TaskRunner(self.task_queue) for _ in range(self.nr_threads)]
        self.tasks = []
        self.app = app
        if not os.path.exists("results"):
            os.makedirs("results")
        
    def add_task(self, task_func, *args):
        if self.app.shutdown:
            return None
        
        task_id = len(self.tasks) + 1
        task = Task(task_id, task_func, *args)
        self.tasks.append(task)
        self.task_queue.put(task)
        return task_id

class TaskRunner(Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue
        self.start()

    def run(self):
        while True:
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            task = self.task_queue.get()
            
            result = task.execute()
            
            with open(f"results/job_{task.job_id}.json", "w") as f:
                f.write(result)
                
            task.task_done()
            
class Task():
    def __init__(self, job_id, func, *args):
        self.job_id = job_id
        self.func = func
        self.args = args
        self.status = "running"
        
    def execute(self):
        result = self.func(*self.args)
        return result
    
    def task_done(self):
        self.status = "done"