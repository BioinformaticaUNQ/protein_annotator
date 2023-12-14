import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.DEBUG)

# adds the handler to the global variable: log
logger.addHandler(_stream_handler)
