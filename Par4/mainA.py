# -*- coding: utf-8 -*-
# Main code
from ControllerA import ControllerA
import cv2
import time

def main():
    while not ControllerA.start():
        continue

 
if __name__ == "__main__":
    main() 

