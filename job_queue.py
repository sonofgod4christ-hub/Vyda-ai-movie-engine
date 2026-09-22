"""
VYDA AI MOVIE ENGINE
Production Job Queue — Build 022

Purpose:
Manage production jobs before they are handled
by specialized generation workers.

Examples:

- Character reference generation
- Scene image generation
- Scene video generation
- Voice generation
- Lip-sync
- Music
- Sound effects
- Movie assembly

The queue does not perform generation itself.

It only manages production work.

This keeps VYDA independent from any specific
AI provider or generation model.

The user creates the world.
VYDA adapts to it.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from uuid import uuid4


@dataclass
class ProductionJob:

    job_id: str

    job_type: str

    scene_id: str = ""

    character_id: str = ""

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    status: str = "QUEUED"

    priority: int = 0

    worker: str = ""

    error: str = ""


class ProductionJobQueue:

    def __init__(self):

        self.jobs: Dict[
            str,
            ProductionJob
        ] = {}

    def create_job(
        self,
        job_type: str,
        payload: Dict[str, Any],
        scene_id: str = "",
        character_id: str = "",
        priority: int = 0,
    ) -> ProductionJob:
        """
        Create a new production job.
        """

        job = ProductionJob(
            job_id=str(
                uuid4()
            ),

            job_type=job_type,

            scene_id=scene_id,

            character_id=character_id,

            payload=payload,

            priority=priority,
        )

        self.jobs[
            job.job_id
        ] = job

        return job

    def get_job(
        self,
        job_id: str,
    ) -> ProductionJob:

        if job_id not in self.jobs:

            raise ValueError(
                f"Production job "
                f"'{job_id}' was not found."
            )

        return self.jobs[
            job_id
        ]

    def update_status(
        self,
        job_id: str,
        status: str,
        error: str = "",
    ):

        job = self.get_job(
            job_id
        )

        job.status = status

        if error:
            job.error = error

    def assign_worker(
        self,
        job_id: str,
        worker: str,
    ):

        job = self.get_job(
            job_id
        )

        job.worker = worker

    def get_queued_jobs(
        self,
    ) -> List[ProductionJob]:
        """
        Return queued jobs ordered by priority.
        """

        queued = [
            job
            for job in self.jobs.values()
            if job.status == "QUEUED"
        ]

        return sorted(
            queued,
            key=lambda job: job.priority,
            reverse=True,
        )

    def cancel_job(
        self,
        job_id: str,
    ):

        job = self.get_job(
            job_id
        )

        if job.status in (
            "COMPLETED",
            "FAILED",
        ):

            return

        job.status = "CANCELLED"

    def complete_job(
        self,
        job_id: str,
    ):

        self.update_status(
            job_id,
            "COMPLETED",
        )

    def fail_job(
        self,
        job_id: str,
        error: str,
    ):

        self.update_status(
            job_id,
            "FAILED",
            error=error,
        )

    def get_queue_snapshot(
        self,
    ) -> dict:

        return {
            "total_jobs":
                len(self.jobs),

            "queued":
                sum(
                    1
                    for job
                    in self.jobs.values()
                    if job.status == "QUEUED"
                ),

            "running":
                sum(
                    1
                    for job
                    in self.jobs.values()
                    if job.status == "RUNNING"
                ),

            "completed":
                sum(
                    1
                    for job
                    in self.jobs.values()
                    if job.status == "COMPLETED"
                ),

            "failed":
                sum(
                    1
                    for job
                    in self.jobs.values()
                    if job.status == "FAILED"
                ),

            "cancelled":
                sum(
                    1
                    for job
                    in self.jobs.values()
                    if job.status == "CANCELLED"
                ),
  }
