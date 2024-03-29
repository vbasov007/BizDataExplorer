import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


class ColorFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        # can't do super(...) here because Formatter is an old school class
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        levelname = record.levelname
        color = COLOR_SEQ % (30 + COLORS[levelname])
        message = logging.Formatter.format(self, record)
        message = message.replace("$RESET", RESET_SEQ) \
            .replace("$BOLD", BOLD_SEQ) \
            .replace("$COLOR", color)
        for k, v in COLORS.items():
            message = message.replace("$" + k, COLOR_SEQ % (v + 30)) \
                .replace("$BG" + k, COLOR_SEQ % (v + 40)) \
                .replace("$BG-" + k, COLOR_SEQ % (v + 40))
        return message + RESET_SEQ


def init_mylogger(*, level_=r'DEBUG', file_=r'logs\par.log',
                  format_=r'%(levelname)s %(asctime)s %(funcName)s: %(message)s'):
    my_logger_name = file_

    my_logger = logging.getLogger(my_logger_name)

    if not my_logger.hasHandlers():
        level = level_

        my_logger.setLevel(level)

        logger_file_handler = logging.FileHandler(file_)

        logger_file_handler.setLevel(level)

        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(level)

        logger_formatter = ColorFormatter(format_)

        logger_console_handler.setFormatter(logger_formatter)
        logger_file_handler.setFormatter(logger_formatter)

        my_logger.addHandler(logger_console_handler)
        my_logger.addHandler(logger_file_handler)

    return my_logger


mylog: logging.Logger = init_mylogger(
    format_=r'$COLOR%(levelname)s $RESET %(relativeCreated)d %(funcName)s: %(message)s'
)
