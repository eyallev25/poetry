import os
import time
from pathlib import Path


LOG_PATH = Path("/tmp/anun.*.log")


def invoke_events():
    os.system("ls")
    print("ls")
    os.system("sleep 1")
    os.system("echo $$")
    os.system("ls -al /tmp/")
    os.system("ls")
    os.system("ls -l")
    time.sleep(10)
    # os.system("/tmp/anun.*.log")
    print("invoke_events")


if __name__ == "__main__":
    invoke_events()
    print("__main__")
