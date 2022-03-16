import logging
import time
from tests.support.docker_handler import (
    run_container,
    is_container_running,
    get_container_stats,
    ContainerResponse,
)
from tests.support.bucket_handler import put_logs_on_results_bucket
from tests.support.files_handler import write_csv_file

logger = logging.getLogger(__name__)  # pylint: disable=C0103
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

IMAGE_NAME = "anun/baseline_image:0.0.1"
LOG_FILE_NAME = "baseline_run.csv"
TIMEOUT = 300


def test_tracer_container():

    container = run_container(IMAGE_NAME, detach=True)

    container_response = ContainerResponse(IMAGE_NAME)
    timeout_start = time.time()

    while is_container_running(container.id) and time.time() < timeout_start + TIMEOUT:
        mem_usage, cpu_usage = get_container_stats(container)
        logger.info(f"mem usage: {mem_usage}, cpu_usage: {cpu_usage}")
        if mem_usage or cpu_usage is not None:
            container_response.add_metrics(mem_usage, cpu_usage)

    write_csv_file(LOG_FILE_NAME, container_response)
    # put_logs_on_results_bucket(LOG_FILE_NAME)
