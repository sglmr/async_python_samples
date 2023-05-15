import asyncio
import logging
from random import randint

"""
    This is a simple demonstration of how to use a asyncio.TaskGroup()
    in Python to run multiple producer tasks that all pass to a single
    consumer task.
"""

# Create a logger
logger = logging.getLogger(__name__)


async def producer(name: str, q: asyncio.Queue, times: int = 5):
    """A function to create a string and write it onto a queue for processing."""

    # Loop times times
    for i, x in enumerate(range(times), 1):
        # Create a sleep # of seconds
        t = randint(1, 3)
        # Send a string to print to the queue
        _s = f"{name}: {i}/{times}, sleep {t}."
        logger.info(f"produced > {_s}")
        await q.put(f"{_s}")
        # Await the sleep time
        await asyncio.sleep(t)


async def consumer(q: asyncio.Queue):
    """A function to consume and log strings off of a queue"""

    # Starting the consumer task
    logger.info("Starting the consumer task")

    # Consume work indefinitely.
    while True:
        try:
            # await the awaitable with a timeout > the max random sleep time
            item = await asyncio.wait_for(q.get(), 5)
            # log the item
            logger.info(f"consumed > {item}")
        # Stop consuming tasks if the timeout is reached.
        except asyncio.TimeoutError:
            logger.warning("Consumer gave up waiting.")
            break

    # Closing the consumer task
    logger.info("Closing the consumer task")


async def main():
    """The main() function to create and run tasks"""
    # Starting
    logger.info("Starting main()")

    # Create a task queue to handle the logging statements
    q = asyncio.Queue(maxsize=1)

    # Create a task group to run tasks
    async with asyncio.TaskGroup() as tg:
        # Create the consumer task
        tg.create_task(consumer(q=q))
        # Create producer tasks
        logger.info("Creating producers")
        for i, x in enumerate(range(3), 1):
            tg.create_task(producer(name=f"task {i}", q=q))

    # Completed
    logger.info("Closing main()")


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
