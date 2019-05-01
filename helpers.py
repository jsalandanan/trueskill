import trueskill
from trueskill import rate_1vs1, Rating
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

def record_result(winner, loser):
  """
  Records the result of a match and updates their ratings.
  Args:
    winner (str): The winner's name.
    loser (str): The loser's name.
  """
  player = Query()
  # get the ratings for both players (assumes existence and one record for now)
  winner_record = DB.search(player.name == winner)[0]
  loser_record = DB.search(player.name == loser)[0]
  # calculate and update their respective ratings
  winner_old_rating = Rating(mu=winner_record['mu'], sigma=winner_record['sigma'])
  loser_old_rating = Rating(mu=loser_record['mu'], sigma=loser_record['sigma'])
  winner_new_rating, loser_new_rating = rate_1vs1(winner_old_rating, loser_old_rating)

  winner_new_record = {'name': winner, 'mu': winner_new_rating.mu, 'sigma': winner_new_rating.sigma}
  loser_new_record = {'name': loser, 'mu': loser_new_rating.mu, 'sigma': loser_new_rating.sigma}
  DB.update(winner_new_record, player.name == winner)
  DB.update(loser_new_record, player.name == loser)
  # insert the match record into the DB
