from xffasttest.common.log import Logger

def action(func, *args, **kwds):
    def wrapper(*args, **kwds):
        result = None
        try:
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            Logger().log_error(e)
            raise e

        return result
    return wrapper