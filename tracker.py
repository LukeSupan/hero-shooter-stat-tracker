from collections import defaultdict



# MUST BE FORMATTED AS FOLLOWS:
# tank,tank2/dps1,dps2/support1,support2/win(orloss)
# you dont need to fill every slot. use none when you dont have someone you know
# examples:
# luke/mar/kayla/win
# none/mar/kayla/loss
# none/luke,mar/kayla/win
# luke,mar/aiden,ray/kayla,dalton/win
# comments are separators for multiple players in a role
# slashes are separators for different roles
# if you are playing marvel rivals or want to add a mvp for whatever reason:
# luke(mvp),aiden/mar/kayla/win
# in this case, luke is the mvp.
# i treat mvp and svp the same, just say mvp. you can see the win loss ratio for mvps
# THIS IS ALL IN THE README. ITS JUST ALSO HERE TO BE SAFE



# open the formatted file (look in README to generate)
with open("games.txt") as f:
    games = [line.strip() for line in f if line.strip()]



# || DATA SETUP
# make a player, contains most data
def make_player():
    return {
        "tankwins": 0, "tankloss": 0,
        "dpswins": 0, "dpsloss": 0,
        "supportwins": 0, "supportloss": 0,
        "wins": 0, "losses": 0, "games": 0,
        "mvps": 0,
        "mvpwins": 0,
        "mvploss": 0
    }

# make comp. these dont consider the roles of the team at all
# purely just players, interesting to have. better in small datasets
def make_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# make role comp, considers the roles of the team
# better in large datasets but super interesting
def make_role_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# create dicts to save multiple players/comps
# data storing is setup. parse next
player_stats = defaultdict(make_player)
comp_stats = defaultdict(make_comp)
role_comp_stats = defaultdict(make_role_comp)



# || PARSING

# parse roles and win from game with /'s

# parse names from roles with ,'s

# parse mvps