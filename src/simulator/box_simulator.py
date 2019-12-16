""" Box Simulator class

Author: Henry Zhang
Date:August 22, 2019
"""

# module
import random
import matplotlib.pyplot as plt

from src.simulator.simulator import Simulator
from src.simulator.car import Car
from src.simulator.box import Box

# parameters


# classes
class BoxSimulator(Simulator):

  def __init__(self, gen_mode = 'constant', fig_name=None, object_num = 1, probability = 0.1, obj_mode='static'):
    ''' Box Simulator class
    
    Args:
      mode='constant': defines the mode of generating objects, 
                      'constant' keeps the number of object specified by object_num,
                      'random' keeps the probability of generating object
      object_num=1: defines the number of objects expected
      probability=0.1: defines the probability of generating objects
      obj_mode='static': defines the motion type of the generated objects.
                         'static' for not moving
                         'keeping' for random speed but keep it.
                         'accelerate' for random acceleration from zero velocity.
    '''
    self.gen_mode = gen_mode
    self.object_num = object_num
    self.gen_prob = probability
    self.obj_mode = obj_mode
    self.objects = []
    self.boundary = [-20, -10, 20, 10]
    self.lane_width=4
    self.box = Box(self.boundary, start=(0,0,0), end=(100,0,0))
    self.fig_name = fig_name
    self.time_acc = 0
    self.velocity_max = 20
    self.velocity_gen = self.velocity_max
  

  def simulate(self, dt):
    ''' simulate the system dynamics for dt 
    
    param:
      dt: time length
    return:
      objs: objects information for sensors
      time_acc: accumulated simulation time
    '''
    self.clean_objects()
    self.generate_objects()
    
    for obj in self.objects:
      if not obj.b_static:
        obj.simulate(dt)
    
    self.viz(dt)

    objs = self.get_objects()
    self.time_acc += dt

    return objs, self.time_acc
  
  def get_objects(self):
    objs = [obj.get_object() for obj in self.objects]
    return objs
  

  def clean_objects(self):
    """ clean up the out of bound objects """
    new_objects = []

    for obj in self.objects:
      if self.is_pos_in_boundary(obj.pos):
        new_objects.append(obj)

    self.objects = new_objects
  

  def generate_objects(self):
    """ generate objects at the boundary """
    pos, orientation = self.get_generating_point()
    for obj in self.objects:
      if obj.is_distance_safe(pos) == False:
        return
    
    if self.gen_mode == 'constant':
      self.generate_objects_constant(pos, orientation)
    elif self.gen_mode == 'random':
      self.generate_objects_random(pos, orientation)

  def generate_objects_constant(self, pos, orientation):
    if len(self.objects) < self.object_num:
      self.generate_an_object(pos, orientation)
  

  def generate_objects_random(self, pos, orientation):
    if random.random() < self.gen_prob:
      self.generate_an_object(pos, orientation)
  

  def generate_an_object(self, pos, orientation):
    mode = 'constant acceleration'
    
    if self.obj_mode == 'static':
      v = 0
      a = 0
    elif self.obj_mode == 'keeping':
      v = random.randint(0,self.velocity_max)
      a = 0
    elif self.obj_mode == 'accelerating':
      v = 0
      a = random.randint(0,10)
    else:
      raise NotImplementedError

    self.objects.append(Car(pos, orientation, v, a, mode))
  

  def get_generating_point(self):
    ''' return the position and orientation an object an be generated.'''
    return self.box.get_generating_point()
  

  def is_pos_in_boundary(self, pos):
    if ( self.boundary[0] <= pos[0] <= self.boundary[2] and \
      self.boundary[1] < pos[1] < self.boundary[3]):
      return True
    else:
      return False


  def viz(self, dt):
    if self.fig_name is None:
      pass
    else:
      plt.figure(self.fig_name)
      plt.gca().set_xlim([self.boundary[0], self.boundary[2]])
      plt.gca().set_ylim([self.boundary[1], self.boundary[3]])
      self.box.viz()
      for obj in self.objects:
        obj.viz()
      plt.title('world {:.3f}, dt={:.3f}'.format(self.time_acc, dt))

    

# functions


# main
def main():
  pass

if __name__ == "__main__":
  main()