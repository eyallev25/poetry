#!/usr/bin/env bash
(/root/.poetry/bin/poetry run pytest -vvv --suppress-tests-failed-exit-code --junitxml report.xml --html report.html) 2>&1 | tee output.log
/root/.poetry/bin/poetry run python3 -m demo_python