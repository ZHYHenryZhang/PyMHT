""" the Tracker class that handles tracking using filter

Author: Henry Zhang
Date:August 23, 2019
"""

# module
import math
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(precision=3)

from src.fusion.kalman_filter import KalmanFilter
from src.fusion.point import Point2D
from src.fusion.box import Box2D
from src.util.utils import is_angle_match

# parameters


# classes
class Estimation():
  def __init__(self, obj_id, state, variance, innovation):
    self.id = obj_id
    self.state = state
    self.variance = variance
    self.innovation = innovation
  
  def is_close(self, estimate):
    state_diff = self.state - estimate.state
    diff_norm = np.linalg.norm(state_diff)
    print("diff_norm", diff_norm, self.id, estimate.id, state_diff)
    print(self.state, estimate.state)
    return diff_norm < 2

class Tracker():
  def __init__(self, time, model):
    self.model = self.initialize(time, model)
    self.observation = None
    self.id = self.model.id
    self.estimate = Estimation(self.id, \
                               self.model.filter.x_post, \
                               self.model.filter.P_post, \
                               self.model.filter.innovation)
    self.threshold_associate = 2
    self.trajectory = [[self.estimate.state[0,0]], [self.estimate.state[1,0]]]
  
  def initialize(self, time, model):
    self.update_time = time
    self.predict_time = time
    model.generate_filter()
    return model 

  def predict(self, time_acc):
    self.model.predict(time_acc - self.predict_time)
    self.estimate = Estimation(self.id, \
                               self.model.filter.x_pre, \
                               self.model.filter.P_pre, \
                               self.model.filter.innovation)
    self.predict_time = time_acc
  
  def update(self):
    if not self.observation is None:
      self.model.update(self.observation)
      self.estimate = Estimation(self.id, \
                                 self.model.filter.x_post, \
                                 self.model.filter.P_post, \
                                 self.model.filter.innovation)
      self.update_time = self.predict_time
    else:
      pass
    
    self.observation = None
    self.trajectory[0].append(self.estimate.state[0,0])
    self.trajectory[1].append(self.estimate.state[1,0])
  
  def find_associate_score(self, model):
    ''' associate track and proposal, return score if success and update observation, None if not associated '''
    threshold = self.threshold_associate
    score = math.hypot(model.x - self.estimate.state[0,0], model.y - self.estimate.state[1,0])
    b_angle_match = is_angle_match(model.get_orientation(), self.model.get_orientation())
    if score < threshold and b_angle_match:
      return score
    else:
      return None
  
  def associate(self, model):
    ''' associate track and proposal, return True if success and update observation, False if not associated '''
    threshold = self.threshold_associate
    if math.hypot(model.x - self.estimate.state[0,0], model.y - self.estimate.state[1,0]) < threshold:
      self.observation = model.generate_observation(self.model.type)
      return True
    else:
      self.observation = None
      return False
  
  def is_close(self, tracker):
    return self.estimate.is_close(tracker.estimate)
  
  def merge(self, tracker):
    ''' return the one with a smaller innovation '''
    norm_self = np.linalg.norm(self.estimate.innovation)
    norm_else = np.linalg.norm(tracker.estimate.innovation)
    if norm_self < norm_else:
      return self
    else:
      return tracker
  
  def viz(self):
    plt.scatter(self.estimate.state[0,0], \
                self.estimate.state[1,0], \
                c='r', marker='o', label='tracker')
    plt.plot(self.trajectory[0], self.trajectory[1])
    """plt.text(self.estimate.state[0,0], \
             self.estimate.state[1,0] + 2, \
             'Tid:{:d}, v:({:.1f}, {:.1f})'.format(self.id, \
                                                   self.estimate.state[2,0], \
                                                   self.estimate.state[3,0]))
    """             
  
    
# functions


# main
def main():
  pass

if __name__ == "__main__":
  main()