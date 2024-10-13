from typing import Sequence
from pyprocess.process import Process
from pyprocess.interfaces import Event, Command, State
import time
import logging

logger = logging.getLogger(__name__)


class Cat(Process[Event, Command, State]):

    class WakeUp(Command):
        pass

    class Sleep(Command):
        pass

    class Asleep(State):
        pass

    class Awake(State):
        pass

    class Meowing(State):
        pass

    class BeginMeowing(Event):
        def __init__(self) -> None:
            logger.info("Meowing")
            time.sleep(0.5)

    class Meow(Command):
        pass

    class GoingToSleep(Event):
        def __init__(self) -> None:
            logger.info("Going to sleep")
            time.sleep(0.5)

    class WakingUp(Event):
        def __init__(self) -> None:
            logger.info("Waking Up")
            time.sleep(0.5)

    @classmethod
    def initial_state(cls) -> State:
        return cls.Asleep()

    @classmethod
    def is_terminal(cls, state: State) -> bool:
        return False

    @classmethod
    def decide(cls, command: Command, state: State) -> Sequence[Event]:
        match (command, state):
            case (cls.WakeUp(), cls.Asleep()):
                return [cls.WakingUp()]
            case (cls.Sleep(), cls.Meowing()):
                return [cls.GoingToSleep()]
            case (cls.Meow(), cls.Awake()):
                return [cls.BeginMeowing()]
            case _:
                logger.warning(
                    f"Irrefutable case hit in decicde() for {command=} {state=}"
                )
                return []

    @classmethod
    def evolve(cls, state: State, event: Event) -> State:
        match (state, event):
            case (cls.Meowing(), cls.GoingToSleep()):
                return cls.Asleep()
            case (cls.Asleep(), cls.WakingUp()):
                return cls.Awake()
            case (cls.Awake(), cls.BeginMeowing()):
                return cls.Meowing()
            case _:
                logger.warning(
                    f"Irrefutable case hit in evolve() for {state=} {event=}"
                )
                return state

    @classmethod
    def react(cls, state: State, event: Event) -> Sequence[Command]:
        match (state, event):
            case (cls.Awake(), cls.WakingUp()):
                return [cls.Meow()]
            case (cls.Asleep(), cls.GoingToSleep()):
                return [cls.WakeUp()]
            case (cls.Meowing(), cls.BeginMeowing()):
                return [cls.Sleep()]
            case _:
                return []

    @classmethod
    def resume(cls, state: State) -> Sequence[Command]:
        match state:
            case cls.Asleep():
                return [cls.WakeUp()]
            case cls.Awake():
                return [cls.Meow()]
            case cls.Meowing():
                return [cls.Sleep()]
            case _:
                return []
