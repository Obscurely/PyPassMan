import logging
import inspect
import datetime
import os
import json
from others import accounts, PyPassMan_init


def get_lineno():
    """
    Returns the current line number in the program.
    """
    line = inspect.currentframe().f_back.f_lineno
    return {"line_no": line}


class Logger:
    """
    Class for logging what happens with the program.
    """

    date_format = "%d-%m-%Y %H:%M:%S"

    @staticmethod
    def create_log_file():
        """
        Creates a log file for the current session.

        :return: Nothing.
        """
        current_dir = os.getcwd()
        file_name = str(datetime.datetime.now()).split(".")[0] + ".log"
        path_separator = accounts.Checker.check_platform()
        full_path = current_dir + path_separator + "Logs" + path_separator + file_name
        try:
            with open(full_path, "w") as f:
                f.write("")
        except NotADirectoryError:
            PyPassMan_init.window_prompt(
                "Error", "Logs folder does not exist! Trying to create it!"
            )
            os.mkdir(current_dir + path_separator + "Logs")
        config_file = (
            current_dir
            + path_separator
            + "PyPassMan_Files"
            + path_separator
            + "config.json"
        )
        with open(config_file, "r") as f:
            config = json.load(f)
        config["last_log_file"] = file_name
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)

    def get_current_log_file(self):
        """
        Gets the current log file using in this session in order to know to which one to write.

        :return: Name of the log file to write to.
        """

        path_separator = accounts.Checker.check_platform()
        config_file = (
            self.program_location
            + path_separator
            + "PyPassMan_Files"
            + path_separator
            + "config.json"
        )
        with open(config_file, "r") as f:
            config = json.load(f)
        current_log_file = config["last_log_file"]
        log_file_location = (
            self.program_location
            + path_separator
            + "Logs"
            + path_separator
            + current_log_file
        )
        return log_file_location

    def debug_log(self, message: str, line_no: dict):
        """
        Writes a log line with the {DEBUG} tag.

        :param message: Log message.
        :param line_no: Log line number.
        :return: Nothing, just outputs to the log file.
        """
        logger = logging.getLogger("DebugLogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.get_current_log_file())
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.debug(message, extra=line_no)
        logger.removeHandler(handler)

    def info_log(self, message, line_no):
        """
        Writes a log line with the {INFO} tag.

        :param message: Log message.
        :param line_no: Log line number.
        :return: Nothing, just outputs to the log file.
        """
        logger = logging.getLogger("InfoLogger")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.get_current_log_file())
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(message, extra=line_no)
        logger.removeHandler(handler)

    def warning_log(self, message, line_no):
        """
        Writes a log line with the {WARNING} tag.

        :param message: Log message.
        :param line_no: Log line number.
        :return: Nothing, just outputs to the log file.
        """
        logger = logging.getLogger("WarningLogger")
        logger.setLevel(logging.WARNING)
        handler = logging.FileHandler(self.get_current_log_file())
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.warning(message, extra=line_no)
        logger.removeHandler(handler)

    def error_log(self, message, line_no):
        """
        Writes a log line with the {ERROR} tag.

        :param message: Log message.
        :param line_no: Log line number.
        :return: Nothing, just outputs to the log file.
        """
        logger = logging.getLogger("ErrorLogger")
        logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(self.get_current_log_file())
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(self, message, extra=line_no, exc_info=True)
        logger.removeHandler(handler)

    def critical_log(self, message, line_no):
        """
        Writes a log line with the {CRITICAL} tag.

        :param message: Log message.
        :param line_no: Log line number.
        :return: Nothing, just outputs to the log file.
        """
        logger = logging.getLogger("CriticalLogger")
        logger.setLevel(logging.CRITICAL)
        handler = logging.FileHandler(self.get_current_log_file())
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.critical(message, extra=line_no, exc_info=True)
        logger.removeHandler(handler)

    def __init__(self, file_name):
        self.log_format = (
            "{%(levelname)s} - [%(asctime)s] - ["
            + file_name
            + "] - [line:%(line_no)s]: %(message)s"
        )
        self.program_location = os.getcwd()
