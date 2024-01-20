# Casserole Singleton Infrastructure
# Based on https://stackoverflow.com/q/6760685 - creating
# singletons with metaclasses. Namely, any class which should
# be a singleton should inherit `metaclass=Singleton` in its constructor
# On the first instantiaion, the single instance will be created and added
# to the global _instances dictionary

# When the instance is destroyed,

_instances = {}


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if cls not in _instances:
            _instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return _instances[cls]


def destroyAllSingletonInstances():
    global _instances
    _instances = {}

def noSingletonsAround():
    return len(_instances)==0
    
class ShortSingltonLivesUnderTest:
    # https://stackoverflow.com/questions/26405380/how-do-i-correctly-setup-and-teardown-for-my-pytest-class-with-tests

    @classmethod
    def setup_class(cls): # pylint: disable=invalid-name
        assert noSingletonsAround()


    @classmethod
    def teardown_class(cls): # pylint: disable=invalid-name
        destroyAllSingletonInstances()
