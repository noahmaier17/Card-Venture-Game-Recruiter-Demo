import pytest

from Dinosaur_Venture.logging import gameplay_logging as log


@pytest.fixture(autouse=True)
def reset_logger():
    """
    Before every test, creates a new instance of the logger.
    """
    log.new_in_memory_log_file()