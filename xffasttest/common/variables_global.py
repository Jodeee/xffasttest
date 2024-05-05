class GlobalVariables(object):

    def __getattr__(self, name: str) -> object:
        try:
            value = self.__getattribute__(name)
            return value
        except:
            return None
    
    def __getitem__(self, name: str) -> object:
        try:
            value = self.__getattribute__(name)
            return value
        except:
            return None

    def __setattr__(self, key: str, value: object) -> None:
        object.__setattr__(self, key, value)

    def __setitem__(self, key: str, value: object) -> None:
        object.__setattr__(self, key, value)