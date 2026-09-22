"""
VYDA AI MOVIE ENGINE
Worker Interface — Build 023

Defines the universal contract for production workers.

A worker is responsible for executing one type
of production job.

Examples:

- Image Worker
- Video Worker
- Voice Worker
- Lip-sync Worker
- Music Worker
- Sound Effects Worker
- Movie Assembly Worker

The worker interface does not depend on any
specific AI provider.

The user creates the world.
VYDA adapts to it.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from job_queue import ProductionJob


class ProductionWorker(ABC):

    """
    Base interface for every VYDA production worker.
    """

    worker_name: str = ""

    supported_job_type: str = ""

    @abstractmethod
    def can_handle(
        self,
        job: ProductionJob,
    ) -> bool:
        """
        Return True when this worker can process
        the supplied job.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        job: ProductionJob,
    ) -> Dict[str, Any]:
        """
        Execute the production job.

        The worker should return a structured result.
        """
        raise NotImplementedError

    def describe(self) -> dict:
        """
        Return worker information.
        """

        return {
            "worker_name":
                self.worker_name,

            "supported_job_type":
                self.supported_job_type,
        }
