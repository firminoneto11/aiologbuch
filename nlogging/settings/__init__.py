from os import getenv

raise_exceptions = getenv("NLOGGING_RAISE_EXCEPTIONS", "false").lower() == "true"
