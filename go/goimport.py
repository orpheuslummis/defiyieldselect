from ctypes import *

lib = cdll.LoadLibrary("/home/miguel/Dev/defiyieldoptimization/go/aave_api.so")

print(lib.display())