from pyprocess.cat import Cat
from pyprocess.interfaces import Event, Command
import logging

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    state = Cat.initial_state()
    commands: list[Command] = list(Cat.resume(state))
    events: list[Event] = []
    while not Cat.is_terminal(state):
        while len(commands) > 0:
            
            command = commands.pop(0)
            logger.debug(f"Proessing  {command=} {state=}")
            events.extend(Cat.decide(command, state))
            while len(events) > 0:
                event = events.pop(0)
                logger.debug(f"Proessing {event=} {state=}")
                state = Cat.evolve(state, event)
                logger.debug(f"New {state=}")
                commands.extend(Cat.react(state, event))
