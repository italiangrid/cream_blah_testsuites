import ConfigParser, testsuite_exception
import os

class CreamTestsuiteConfSingleton(object):
    """ This class is a python singleton not inheritable.
        It is used to read the configuration """

    __instance = None
    __config = None
      
    def __new__(cls, *args, **kargs): 
        return cls.getInstance(cls, *args, **kargs)

    def __init__(self):
        pass

    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        if cls.__instance is None:
            # Initialize **the unique** instance
            cls.__instance = object.__new__(cls)

            '''Initialize object **here**, as you would do in __init__()...'''
            cls.__config = ConfigParser.RawConfigParser()
            cls.__config.read(os.environ['CREAM_TESTSUITE_HOME'] + '/lib/conf/cream_testsuite_conf.ini')

        return cls.__instance

    getInstance = classmethod(getInstance)

    def getParam(cls, sectionName, paramName):
        return cls.__config.get(sectionName, paramName)

    def checkIfParamIsNull(cls, paramName, paramValue):
        if len(paramValue) == 0:
            raise testsuite_exception.TestsuiteError("Parameter %s is empty. Check configuration" % paramName)

#Usage
#mySingleton1 =  Singleton()
#mySingleton2 =  Singleton()
#
#mySingleton1 and  mySingleton2 are the same instance.
#assert mySingleton1 is mySingleton2



