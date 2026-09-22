"""
VYDA AI MOVIE ENGINE
Worker Manager — Build 024

Manages production workers.

Purpose:
- Register workers.
- Find the correct worker for a job.
- Prevent incompatible workers from executing jobs.
- Keep worker selection independent from the Movie Brain.

The user creates the world.
VYDA adapts to it.
"""

from typing import Dict, List

from job_queue import ProductionJob

from worker_interface import ProductionWorker


class WorkerManager:

    def __init__(self):

        self.workers: Dict[
            str,
            ProductionWorker
        ] = {}

    def register_worker(
        self,
        worker: ProductionWorker,
    ):

        if not worker.worker_name:

            raise ValueError(
                "Worker must have a worker_name."
            )

        if worker.worker_name in self.workers:

            raise ValueError(
                f"Worker "
                f"'{worker.worker_name}' "
                "is already registered."
            )

        self.workers[
            worker.worker_name
        ] = worker

    def remove_worker(
        self,
        worker_name: str,
    ):

        if worker_name in self.workers:

            del self.workers[
                worker_name
            ]

    def get_worker(
        self,
        worker_name: str,
    ) -> ProductionWorker:

        if worker_name not in self.workers:

            raise ValueError(
                f"Worker "
                f"'{worker_name}' "
                "was not found."
            )

        return self.workers[
            worker_name
        ]

    def find_worker(
        self,
        job: ProductionJob,
    ) -> ProductionWorker:

        for worker in self.workers.values():

            if worker.can_handle(job):

                return worker

        raise ValueError(
            f"No worker is available "
            f"for job type "
            f"'{job.job_type}'."
        )

    def list_workers(
        self,
    ) -> List[dict]:

        return [
            worker.describe()
            for worker in self.workers.values()
        ]

    def has_worker_for(
        self,
        job: ProductionJob,
    ) -> bool:

        for worker in self.workers.values():

            if worker.can_handle(job):

                return True

        return False
