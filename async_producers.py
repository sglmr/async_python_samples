import asyncio
import logging
from random import randint

"""
    This is a simple demonstration of how to use a asyncio.TaskGroup()
    in Python to run multiple producer tasks.
"""

# Create a logger
logger = logging.getLogger(__name__)


async def producer(name: str, times: int = 5):
    """A function to just print a few things at random times"""

    # Loop times times
    for i, x in enumerate(range(times), 1):
        # Create a sleep # of seconds
        t = randint(1, 3)
        logger.info(f"{name}: {i}/{times}, sleep {t}.")
        # Await the sleep time
        await asyncio.sleep(t)


async def main():
    """The main() function to create and run tasks"""

    logger.info("Creating tasks")

    # Create a task group to run tasks
    async with asyncio.TaskGroup() as tg:
        # Create producer tasks
        for i, x in enumerate(range(3), 1):
            tg.create_task(producer(name=f"task {i}"))
    # Tasks completed
    logger.info("Both tasks have created")


if __name__ == "__main__":
    # Choose a logging handler
    try:
        from rich.logging import RichHandler

        logging_handlers = [RichHandler()]
    except ModuleNotFoundError:
        logger.warning("Rich text package unavailable.")
        logging_handlers = [logging.StreamHandler()]

    # Configure the logger
    logging.basicConfig(
        format="%(name)s: %(message)s",
        datefmt="[%X]",
        level=logging.INFO,
        handlers=logging_handlers,
    )

    asyncio.run(main())
