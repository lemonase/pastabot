""" Logging helper module

This module has some common log messages for the context of the bot.
"""
import logging
import sys
import bot


# TODO: Add configuration to control log
# and put logs somewhere that makes sense
def set_basic_logger():
    """ Configures the python logger with basic parameters """
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.FileHandler(
            "pastabot.log"), logging.StreamHandler()],
    )


def get_advanced_logger():
    """ Uses a more advanced configuration for logging,
    Returns a logging object """
    adv_logger = logging.getLogger(__name__)
    adv_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        filename="pastabot.log", encoding="utf-8")
    stdout_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    adv_logger.addHandler(file_handler)
    adv_logger.addHandler(stdout_handler)

    return adv_logger


def log_discord_command(command_name: str, discord_user: str):
    """ Log message for when someone executes a command """
    logging.info("%s command issued by %s", command_name, discord_user)


def log_begin():
    """ Log when the bot starts up """
    logging.info("*" * 10)
    logging.info("PastaBot %s has started", bot.__version__)
    logging.info("*" * 10)


def log_end():
    """ Log when the bot shuts down """
    logging.info("*" * 10)
    logging.info("PastaBot %s has shut down", bot.__version__)
    logging.info("*" * 10)
