import os
import sys
def check_environment():
    print("Environment Details:")
    print("---------------------")
    print("Operating System: " + os.name)
    print("Python Version: " + sys.version)
    print("Python Executable Path: " + sys.executable)
    print("---------------------")

if __name__=='__main__':
  check_environment()