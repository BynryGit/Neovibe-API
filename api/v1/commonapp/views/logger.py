from sentry_sdk import configure_scope, capture_exception


class logger():
    def log(self,error,severity,message=None,**kwargs):
        with configure_scope() as scope:
            scope.set_level(severity)
            scope.set_extra('message',message)
            for key, val in kwargs.items():
                scope.set_extra(key,val)
            capture_exception(error)
