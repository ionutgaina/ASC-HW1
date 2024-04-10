"""Module to manage TaskRunners."""
from queue import Queue, Empty
from threading import Thread
import os

class ThreadPool:
    """A ThreadPool class to manage TaskRunners"""

    def __init__(self, app=None):
        """
        Initialize the ThreadPool.

        You must implement a ThreadPool of TaskRunners.
        Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined.
        If the env var is defined, that is the number of threads to be used by the thread pool.
        Otherwise, you are to use what the hardware concurrency allows.
        You are free to write your implementation as you see fit, but
        you must NOT:
            * create more threads than the hardware concurrency allows
            * recreate threads for each task
        """
        self.nr_threads = int(os.environ.get('TP_NUM_THREADS', os.cpu_count()))
        self.task_queue = Queue()
        self.threads = [TaskRunner(self.task_queue, app) for _ in range(self.nr_threads - 1)]
        self.tasks = []
        self.app = app
        if not os.path.exists("results"):
            os.makedirs("results")

    def add_task(self, task_func, *args):
        """Add a task to the thread pool."""
        self.app.logger.info(f"Adding task {task_func.__name__} to ThreadPool")
        if self.app.shutdown:
            return None
        task_id = len(self.tasks) + 1
        task = Task(task_id, task_func, *args)
        self.tasks.append(task)
        self.task_queue.put(task)
        return task_id
    def get_tasks(self):
        """Get all tasks in the thread pool."""
        return self.tasks

    def shutdown(self):
        """Shutdown the ThreadPool."""
        self.app.logger.info("Shutting down ThreadPool")
        self.app.shutdown = True
        for thread in self.threads:
            thread.join()
        self.threads = []

class TaskRunner(Thread):
    """A TaskRunner class to execute tasks."""

    def __init__(self, task_queue, app=None):
        """Initialize TaskRunner with a task queue."""
        super().__init__()
        self.task_queue = task_queue
        self.app = app
        self.start()

    def run(self):
        """Run the TaskRunner."""
        while True:
            if self.task_queue.empty() and self.app.shutdown:
                self.app.logger.info("Shutting down thread")
                break
            try :
                task = self.task_queue.get(block=False)
                self.app.logger.info(f"Executing task {task.func.__name__}")
            except Empty:
                continue
            result = task.execute()
            with open(f"results/job_{task.job_id}.json", "w", encoding="utf-8") as f:
                f.write(result)
            task.task_done()

class Task:
    """A Task class representing a single task."""

    def __init__(self, job_id, func, *args):
        """Initialize a Task."""
        self.job_id = job_id
        self.func = func
        self.args = args
        self.status = "running"

    def execute(self):
        """Execute the task."""
        result = self.func(*self.args)
        return result

    def task_done(self):
        """Mark the task as done."""
        self.status = "done"
        