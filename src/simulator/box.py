""" the Road class

Author: Henry Zhang
Date:August 22, 2019
"""

# module
from matplotlib import pyplot as plt
import math
import random

# parameters


# classes
class Box():

  def __init__(self, boundary, start=(0,0,0), end=(10000,0,0)):
    self.boundary = boundary
    self.start = start
    self.end = end
    self.b_static = True
    self.b_bidirection = True
  

  def get_generating_point(self):
    pos_x = random.random() * (self.boundary[2] - self.boundary[0]) + self.boundary[0]
    pos_y = random.random() * (self.boundary[3] - self.boundary[1]) + self.boundary[1]
    pos_z = 0
    orientation = math.pi + math.atan2(pos_y, pos_x)
    return [pos_x, pos_y, pos_z], orientation
  


  def viz(self):
    pass

# functions


# main
def main():
  pass

if __name__ == "__main__":
  main()