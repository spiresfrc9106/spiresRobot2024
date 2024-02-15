from utils.singleton import Singleton

class Debug(metaclass=Singleton):
    def __init__(self):
        """
        This is a class for efficiently logging data using the tradition print method while maintaining high speeds by
        only selecting log types that as needed for the given testing environment
        """

        ### LOG TYPE SETUP ###
        self.piece = True
        self.robot = False
        self.toPrint = {}

    def print(self, tag, data):
        if tag in self.toPrint.keys() and self.toPrint[tag]: # pylint: disable=consider-iterating-dictionary
            print(f"{tag}: {data}")
