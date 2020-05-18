import logging
import sentry_sdk
from sentry_sdk import configure_scope, capture_exception
from sentry_sdk.integrations.logging import LoggingIntegration

__author__ = 'Rohan'


class logger():
    def log(self, error, severity, **kwargs):
        sentry_logging = LoggingIntegration(
            level=logging.ERROR,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )

        sentry_sdk.init(
            dsn="https://804e668152394b0c9035f875c31198c8@o391307.ingest.sentry.io/5237334",
            integrations=[sentry_logging],
            default_integrations=False,
            send_default_pii=False
        )
        with configure_scope() as scope:
            scope.set_level(severity)
            for key, val in kwargs.items():
                scope.set_extra(key,val)
            return capture_exception(error)


