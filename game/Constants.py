''' keep all constants here '''

# client send this events as requests
BUY_FUEL = "buy_fuel"
RETURN_TO_EARTH = "return_to_earth"
LANDED_SUCCESSFULLY = "spaceship_landed"
CRASH_LANDED = "spaceship_crashed"
REQUEST_PLOT = "choose_plot_to_land"
QUIT_GAME = "quit_game"
SPACESHIP_FUEL_KEY = "Spaceship Fuel Level"

# server sends this events to clients
REQUEST_PLOT_DENIED = "request_plot_denied"
REQUEST_PLOT_APPROVED = "request_plot_approved"
PRINT_LEADERBOARD = "leaderboard_changed"
BASE_STATION_FUEL_UPDATED = "base_fuel_changed"
PRINT_GAME_GOAL = "print_game_goal"
UPDATE_GAME_SCORE = "update_game_score"
GAME_START = "game_start"
GAME_GOAL_ACHIEVED = "game_goal_achieved"
GAME_OVER_FOR_CLIENT = "game_over_for_client"
GAME_OVER_ALL = "game_over_all"
UPDATE_PLOT_GRID = "mining_grid_changed"
FUEL_REQUEST_DENIED = "fuel_request_denied"
UPDATE_GRID_STATUS = "update_grid_status"
UPDATE_SPACESHIP_STATE = "update_spaceship_state"


# others
NOTIFICATION = "notification"
MAX_FUEL_BASE_STATION = 100
GOLD_PLOT_TOTAL = 10
COPPER_PLOT_TOTAL = 15
IRON_PLOT_TOTAL = 30
GOLD = "gold"
COPPER = "copper"
IRON = "iron"
BUY_RATE = 5
FUEL_EXCHANGE = 10 # this much units of fuel will be bought per transaction
GOLD_MINE_LIMIT = 5
COPPER_MINE_LIMIT = 10
IRON_MINE_LIMIT = 15
SPACESHIP_OWN_MASS = 50
SPACESHIP_CARGO_CAPACITY = 100
SPACESHIP_FUEL_CAPACITY = 100

