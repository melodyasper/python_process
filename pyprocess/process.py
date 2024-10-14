from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

E = TypeVar("E")
C = TypeVar("C")
S = TypeVar("S")


class Process(ABC, Generic[E, C, S]):

    @classmethod
    @abstractmethod
    def evolve(self, state: S, event: E) -> S:
        """Update the process state based on the current event.

        Paramters
            state: State of the current process
            event: Event

        Returns
            An sequence of commands to act on.
        """
        pass

    @classmethod
    @abstractmethod
    def resume(cls, state: S) -> Sequence[C]:
        """Resume to the next command from a starting state.

        Parameters
            state: State of the current process

        Returns
            An iterable set of commands to act on.
        """
        pass

    @classmethod
    @abstractmethod
    def react(cls, state: S, event: E) -> Sequence[C]:
        """React to an event by generating new commands.

        Parameters
            state: State of the current process
            event: Event being reacted to

        Returns
            A sequence of commands to act on.
        """
        pass

    @classmethod
    @abstractmethod
    def initial_state(cls) -> S:
        """Starting state for a process.

        Returns
            The base state to begin the process with
        """
        pass

    @classmethod
    @abstractmethod
    def is_terminal(cls, state: S) -> bool:
        """Checks if the current state is the end state for the process.

        Parameters
            state: State of the current process

        Returns
            A boolean indicating if a process is finished.
        """
        pass

    @classmethod
    @abstractmethod
    def decide(cls, command: C, state: S) -> Sequence[E]:
        """React to an event by generating new commands.

        Parameters
            command: Operation to be processed
            state: State of the current process

        Returns
            A sequence of events to evolve the state on.
        """
        pass
