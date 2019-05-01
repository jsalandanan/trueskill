import trueskill
from tinydb import TinyDB, Query
from settings import DB_PATH, DEFAULT_MU, DEFAULT_SIGMA

DB = TinyDB(DB_PATH)

trueskill.setup(mu=DEFAULT_MU, sigma=DEFAULT_SIGMA)

def add_player(name):
  """
  Adds a player to the rating system.
  Args:
    name (str): The player's name.
  """
  DB.insert({'name': name, 'mu': DEFAULT_MU, 'sigma': DEFAULT_SIGMA})
