""" the methods for association

Author: Henry Zhang
Date:August 23, 2019
"""

# module


# parameters


# classes
class Association():
  def __init__(self, mode = "GNN"):
    self.mode = mode

  def associate(self, proposals, trackers):
    if self.mode == "GNN":
      return self.associate_global_nearest_neighbour(proposals, trackers)
    elif self.mode == "MHT":
      return self.associate_multiple_hypothesis(proposals, trackers)
    elif self.mode == "JPDA":
      return self.associate_joint_probabilistic_data_association(proposals, trackers)
    else:
      raise NotImplementedError
  
  def associate_global_nearest_neighbour(self, proposals, trackers):
    new_proposals = []
    matched_pairs = []
    
    for proposal in proposals:
      matched_pair = self.find_best_associate_pair(proposal, trackers)
      if len(matched_pair) > 0:
        matched_pairs.append(matched_pair)
      else:
        new_proposals.append(proposal)

    return matched_pairs, new_proposals

  def find_best_associate_pair(self, proposal, trackers):
    ''' return the best association pair between tracker and model, empty list if no match.
    Best in a sense of matching score. '''
    pairs = []
    for model in proposal.models:
      for tracker in trackers:
        score = tracker.find_associate_score(model)
        if not score is None:
          pairs.append((score, tracker, model))
    if len(pairs) == 0:
      return []
    else:
      sorted(pairs, key=lambda x: x[0])
      return (pairs[0][1], pairs[0][2])
  
  def associate_multiple_hypothesis(self, proposals, trackers):
    new_proposals = []
    matched_pairs = []
    
    for tracker in trackers:
      matched_list = []
      for proposal in proposals:
        for model in proposal.models:
          # TODO at December 16, 2019: implement gating method in data association for tracker
          if tracker.is_in_gate(model):
            matched_list.append(model)
            proposal.associated = True
      if len(matched_list) > 1:
        # TODO at December 16, 2019: Tracker copy
        pass
      if len(matched_list) == 1:
        matched_pairs.append([tracker, matched_list[0]])
      else:
        pass
        
      for proposal in proposals:
        if proposal.associated == False:
          new_proposals.append(proposal)

    return matched_pairs, new_proposals
  
  def associate_joint_probabilistic_data_association(self, proposals, trackers):
    pass
# functions


# main
def main():
  pass

if __name__ == "__main__":
  main()