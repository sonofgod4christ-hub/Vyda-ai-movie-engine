"""
VYDA AI MOVIE ENGINE
Provider Interface — Build 025

Defines the universal interface between VYDA workers
and external or self-hosted AI providers.

Architecture:

VYDA
  ↓
Worker
  ↓
Provider Adapter
  ↓
AI Model / Service

The core VYDA engine must not depend directly
on a specific provider.

Providers can eventually be:

- External APIs
- Open-source models
- Self-hosted models
- VYDA-owned infrastructure

The user creates the world.
VYDA adapts to it.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class AIProvider(ABC):

    """
    Base interface for all VYDA AI providers.
    """

    provider_name: str = ""

    def describe(self) -> dict:
        """
        Return basic provider information.
        """

        return {
            "provider_name":
                self.provider_name,
        }

    @abstractmethod
    def generate(
        self,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate an output from the supplied payload.

        The provider must return a structured result.
        """

        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Report whether the provider is currently
        available for use.
        """

        raise NotImplementedError
