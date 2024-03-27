def service():
    def decorator(cls):
        class ServiceWrapper(cls):
            __instance = None

            def __constructor__(self) -> None:
                pass

            @classmethod
            def get_instance(cls):
                if cls.__instance == None:
                    cls.__instance = cls.__new__(cls)
                    if hasattr(cls.__instance, '_constructor'):
                        cls.__instance._constructor()
                    cls.__instance.__constructor__()
                return cls.__instance

            def __init__(self):
                raise RuntimeError("This is a Singleton, invoke get_instance() insted.")

        if hasattr(cls, '__constructor__'):
            ServiceWrapper._constructor = cls.__constructor__
        else:
            ServiceWrapper._constructor = lambda self: None
        return ServiceWrapper
    return decorator