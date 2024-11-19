import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

error_handler_logger = logging.getLogger("error_handler")
user_activity_logger = logging.getLogger("user_act")
injection_notifier_logger = logging.getLogger("injection_notifier")