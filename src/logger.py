""" Logging helper module

This module has some common log messages for the context of the bot.
"""
import argparse
import logging
import os
import pathlib
import sys

import bot


def get_log_filename(args: argparse.Namespace) -> str:
    """Returns the path to a log file. A tempfile is used if log_path is not in args"""
    log_file = ""
    if not args.log_path:
        import tempfile

        log_file = pathlib.Path(tempfile.gettempdir()) / "pastabot" / "pastabot.log"
    else:
        log_file = args.log_path / "pastabot.log"

    log_file = log_file.expanduser().resolve()
    if not log_file.parent.exists():
        log_file.parent.mkdir(parents=True, exist_ok=False)
    log_file.touch(exist_ok=True)

    return str(log_file)


def set_basic_logger(
    filename: str = "pastabot.log", log_file: bool = True, log_stdout: bool = True
) -> logging.basicConfig:
    """ Configures the python logger with basic parameters like name, file, and stdout"""
    log_handlers = []
    if log_file:
        log_handlers.append(logging.FileHandler(filename))
    if log_stdout:
        log_handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        level=logging.INFO,
        encoding="utf-8",
        handlers=log_handlers,
    )


def get_advanced_logger() -> logging.Logger:
    """Uses a more advanced configuration for logging,
    Returns a logging object"""
    adv_logger = logging.getLogger(__name__)
    adv_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename="pastabot.log", encoding="utf-8")
    stdout_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    adv_logger.addHandler(file_handler)
    adv_logger.addHandler(stdout_handler)

    return adv_logger


def log_discord_command(command_name: str, discord_user: str) -> None:
    """ Log message for when someone executes a command """
    logging.info("%s command issued by %s", command_name, discord_user)


def log_action(action: str) -> None:
    """ Log bot actions"""
    log_char = "="
    if "started" in action.lower():
        log_char = "+"
    elif "shutdown" in action.lower():
        log_char = "-"

    log_msg = "PastaBot has {}".format(action)
    logging.info(log_char * len(log_msg))
    logging.info(log_msg)
    logging.info(log_char * len(log_msg))
