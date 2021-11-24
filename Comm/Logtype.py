import time
from loguru import logger
from pathlib import Path

project_path = Path.cwd().parent
log_path = Path(project_path, "log")
t = time.strftime("%Y_%m_%d")


class Loggings:
    __instance = None
    logger.add(f"{log_path}/test_log_{t}.log", rotation="500MB", encoding="utf-8", enqueue=True,
               retention="1 days")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)


loggings = Loggings()
# if __name__ == '__main__':
#     loggings.info("test")
#     loggings.debug("test")
#     loggings.warning("test")
#     loggings.error("test")
