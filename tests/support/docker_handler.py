import docker
import logging
from docker.errors import APIError, ImageNotFound, ContainerError, NotFound


logger = logging.getLogger(__name__)  # pylint: disable=C0103
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

client = docker.from_env()


def run_container(image: str, **kwargs):
    """Run a docker container using a given image; passing keyword arguments
    documented to be accepted by docker's client.containers.run function.
    """
    container = None
    try:
        container = client.containers.run(image, **kwargs)
        logger.info(f"Running container with container id: {container.id}")
        if "name" in kwargs.keys():
            logger.info("Container", kwargs["name"], "is now running.")
    except ContainerError as err:
        logger.error("Failed to run container")
        raise err
    except ImageNotFound as err:
        logger.error("Failed to find image to run as a docker container")
        raise err
    except APIError as err:
        logger.error("Unhandled error")
        raise err

    return container


def get_container(name_or_id: str):
    """Get the container with the given name or ID"""

    container = None
    try:
        container = client.containers.get(name_or_id)
        logger.info(f"container id: {container.id}")
    except NotFound as err:
        # Return None when the container is not found
        pass
    except APIError as err:
        logger.error("Unhandled error")
        raise err

    return container


def is_container_running(name_or_id: str):
    """Check if container with the given name or ID is running. Returns True if running, False if not."""

    try:
        container = get_container(name_or_id)

        if container:
            if container.status == "created":
                return False
            elif container.status == "running":
                logger.info(f"container status: {container.status}")
                return True
            elif container.status == "removing":
                return False
            elif container.status == "paused":
                return False
            elif container.status == "exited":
                return False
            elif container.status == "dead":
                return False
            else:
                return False
    except NotFound as err:
        return False

    return False


def get_container_stats(container):
    """
    Arguments:
        container (object) : The container object.
    Return:
        mem_usage (int) : container's mem usage metric.
        total_cpu_usage (int) : container's total cpu usage metric.
    """
    mem_usage = None
    total_cpu_usage = None
    status = container.stats(decode=None, stream=False)

    if "usage" in status["memory_stats"]:
        mem_usage = status["memory_stats"]["usage"]
        total_cpu_usage = status["cpu_stats"]["cpu_usage"]["total_usage"]

    return mem_usage, total_cpu_usage


class ContainerResponse:
    def __init__(self, image_name):
        self.image_name = image_name
        self.mem_usage_list = []
        self.cpu_usage_list = []

    def add_metrics(self, mem_usage, cpu_usage):
        self.mem_usage_list.append(mem_usage)
        self.cpu_usage_list.append(cpu_usage)
