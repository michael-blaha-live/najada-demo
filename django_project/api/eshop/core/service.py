import functools
from .singleton import Singleton


class Service(metaclass=Singleton):
    def serializer(serializer_class):
        def decorator_serializer(func):
            @functools.wraps(func)
            def wrapper_serializer(*args, **kwargs):
                if serializer_class:
                    return serializer_class(func(*args, **kwargs))
                return func(*args, **kwargs)
        return serializer

    # @serializer(Serializer)
    # def do_foo()
    #     return foo
