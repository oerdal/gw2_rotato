class Player:

  def __init__(self, player_data):
    self.player_data = player_data
  
  
  def __repr__(self):
    return self.player_data['Name']