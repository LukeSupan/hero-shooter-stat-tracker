from collections import defaultdict

# I AM GOING TO EXTREMELY OVEREXPLAIN THE CODE IN THESE COMMENTS
# I WANT ANYONE TO BE ABLE TO EDIT THIS HOWEVER THEY WOULD LIKE.
# I FOUND MYSELF MAKING A TON OF SMALL TWEAKS TO VIEW THE DATA DIFFERENTLY WHILE USING IT MYSELF
# IT WILL BE SOME WORK TO READ THROUGH. HOWEVER, I BELIEVE IN YOU.

# MUST BE FORMATTED AS FOLLOWS:
# tank,tank2/dps1,dps2/support1,support2/win(orloss)
# change file name below. a clear explanation and examples are in README, mvp is entirely optional
#            |
#            |
#            V
# --------------------------
# INPUT FILE (what you are looking for most likely)
# --------------------------
# open the formatted file (look in README to generate)
with open("games.txt") as f: # CHANGE games.txt TO MATCH YOUR TEXT FILE. GAMES.TXT IS JUST MY CHOICE
    games = [line.strip() for line in f if line.strip()]


# --------------------------
# DATA MODELS
# --------------------------
# make a new player, contains all individual data. bulk of information.
# you can see most of these things on tracking sites. but you can control the data here
# theres also all that other stuff
def make_player():
    return {
        "tankwins": 0, "tanklosses": 0,
        "dpswins": 0, "dpslosses": 0,
        "supportwins": 0, "supportlosses": 0,
        "wins": 0, "losses": 0, "games": 0,
        "mvps": 0,
        "mvpwins": 0,
        "mvplosses": 0
    }

# make a new comp. these dont consider the roles of the team at all
# purely just players, interesting to have. better in small datasets
def make_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# make a new role comp, considers the roles of the team
# better in large datasets but super interesting. you'll see if you fill it out.
def make_role_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# defaultdict automatically intitializes new keys when they appear
# create dicts to save multiple players/comps
# data storing is setup. parse next
player_stats = defaultdict(make_player)
comp_stats = defaultdict(make_comp)
role_comp_stats = defaultdict(make_role_comp)



# --------------------------
# PARSING FUNCTIONS
# --------------------------
# parse mvps out of names.
# result is the name minus (mvp) if present and true (for removal) or false (for no need).
def parse_name_and_mvp(name):
    name = name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True
    return name, False

# parse the notable game stats out of the line, mvp is still included for now
# result is dictionary of the game, showing the tanks, dps, and support, and then a result win or loss
# at this point tank could still be something like: luke,mar(mvp).
def parse_game_line(line):
    tank_player, dps_player, support_player, result = line.split("/")
    return { "tank": tank_player, "dps": dps_player, "support": support_player }, result # return 2-tuple with dictionary and result



# --------------------------
# PROCESSING FUNCTIONS
# --------------------------
# result is winrate, given wins and games, returns 0 for no games
def winrate(wins, games):
    return (wins / games * 100) if games else 0

# extract a set of all player names from the parsed team dict from parse_game_line
# mvp is cut away here.
# result is the set of the comp to be updated
def extract_players(team):
    players = set()

    # for each slot of value, split if needed and add to the players set
    for slot in team.values():
        if slot != "none":
            for names in slot.split(","):
                name, _ = parse_name_and_mvp(names) # we arent using is_mvp here. hence _
                players.add(name)
    return players

# sort the comps of a certain size by winrate (games if equal)
# works for both role-based and non role-based
# returns a tuple (winrate, games) for sorting the comps when given a comps stats from dict
def sized_comps_sort_key(comp_stats):
    _, stats = comp_stats
    return (
        winrate(stats["wins"], stats["games"]),
        stats["games"]
    )

# generate a string as a key for a role-based comp
# gets rid of MVP, sorts alphabetically per role, then joins the roles with a /. making a final string key
# IF YOU WANT YOUR FINAL RESULT OF THE PRINTING TO LOOK DIFFERENT. CHANGE IT HERE. BUT. YOU NEED TO ACCOUNT FOR THIS CHANGE IN role_comp_team_size BELOW
def get_role_comp_key(team):
    players = [] # players like above but as a list. so it matters 

    # we need to get member for tank, dps, and support, just like before. sort each slot alphabetically so it doesnt matter
    for role in ("tank", "dps", "support"):
        slot = team[role] # check each slot
        if slot == "none":
            players.append(f"{role}: none") # this role is empty
        else:
            
            # before adding them to the key. we need to get rid of mvp, otherwise we get duplicate comps.
            clean_names = []
            for raw in slot.split(","):
                name, _ = parse_name_and_mvp(raw)
                clean_names.append(name)

            sorted_players = sorted(clean_names)
            names = ", ".join(sorted_players) # rejoin the list back into a string with a comma (with a space to look better), basically just makes sure we have no duplicate role comp
            players.append(f"{role}: {names}") # add the final string to its slot in the list (THIS IS WHERE YOU WOULD CHANGE THE FORMATTING. IF YOU DO ANOTHER FUNCTION (role_comp_team_size) NEEDS TO CHANGE A GOOD BIT.
    return " / ".join(players) # make one final string by joining with /

# count the number of unique players in role-based comp key
# cant just do length like with the other because the string is formatted
# if you change the formatting above, you are going to have to change this to account for it. sorry.
def role_comp_team_size(role_comp_key):
    slots = role_comp_key.split(" / ")
    players = set()
    for slot in slots:
        _, names = slot.split(":")
        names = names.strip()
        if names != "none":
            for name in names.split(", "):
                players.add(name)
    return len(players)

    

# --------------------------
# AGGREGATION
# --------------------------
# for each game, add relevant stats
for line in games:
    team, result = parse_game_line(line)

    # add stats for each player from the current game
    for role, names in team.items():
        if names == "none":
            continue

        # if multiple names, split with , and run for each
        for raw in names.split(","):
            name, is_mvp = parse_name_and_mvp(raw) # remove mvp if present

            player_stats[name]["games"] += 1 # yeah man they played a game

            if is_mvp:
                player_stats[name]["mvps"] += 1

            # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is. future thing anyway. if youd like to add it go ahead
            if result == "win":
                player_stats[name][f"{role}wins"] += 1 # add 1 to role winrate
                player_stats[name]["wins"] += 1
                player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
            else:
                player_stats[name][f"{role}losses"] += 1 # add 1 to role winrate
                player_stats[name]["losses"] += 1
                player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvpwins


    # for this game, adjust the comp stats
    comp_key = tuple(sorted(extract_players(team))) # sort the set, make it a tuple so that we can use it as a key
    comp_stats[comp_key]["games"] += 1

    if result == "win":
        comp_stats[comp_key]["wins"] += 1
    else:
        comp_stats[comp_key]["losses"] += 1


    # for this game, adjust the role comp stats
    role_comp_key = get_role_comp_key(team)
    role_comp_stats[role_comp_key]["games"] += 1

    if result == "win":
        role_comp_stats[role_comp_key]["wins"] += 1
    else:
        role_comp_stats[role_comp_key]["losses"] += 1



# --------------------------
# PRINTING
# --------------------------
# print individual players stats
for player, stats in sorted(player_stats.items()):
    print(f"\n===== {player} =====") # 5 ='s on left plus a space centers it above the following
    print(f"  Tank:    {stats['tankwins']}W / {stats['tanklosses']}L")
    print(f"  DPS:     {stats['dpswins']}W / {stats['dpslosses']}L")
    print(f"  Support: {stats['supportwins']}W / {stats['supportlosses']}L")
    print(f"  Overall: {stats['wins']}W / {stats['losses']}L")
    print(f"  Winrate: {winrate(stats['wins'],stats['games']):.1f}%") # colon here is a format specifier. just set to 1 decimal point

    # im making it so mvp only prints if they have mvp stats. overwatch players have zero use for it.
    if stats['mvps'] > 0:
        print(f"    MVPs: {stats['mvps']}")
        print(f"    MVP Ratio: {stats['mvpwins']}W / {stats['mvplosses']}L")


# print non role comps (2 or more) to avoid some clutter, 1 is reasonable if you want to change this. i just prefer less clutter and who cares about 1 game.
# this is one of the most interesting parts. you can see who is weak. and strong i suppose
print("\n\n===== NON-ROLE-BASED COMPS =====")

# print in order of smallest to largest team size first
team_sizes = sorted({len(comp) for comp in comp_stats})

for size in team_sizes:

    # use list comprehension to make a new list
    # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
    # result is a list of tuples: (("aiden", "luke"), {"wins": 1.....}), and so on
    sized_comps = [
        (comp, stats) # we are adding comps and their stats to the list, output
        for comp, stats in comp_stats.items() # this gets all comps, iteration
        if len(comp) == size and stats["games"] > 0 # get only comps of this size, filter
    ]

    # if its empty, we dont print the title card and move on
    if not sized_comps:
        continue

    print(f"\n----- {size}-PLAYER COMPS -----")

    # sort by winrate, the key is winrate first, games played as backup
    sized_comps.sort(key=sized_comps_sort_key, reverse=True)
    
    # print the comps in order
    for comp, stats in sized_comps:
        names = ", ".join(comp) # combine names for the comp
        print(f"{names:30} {winrate(stats["wins"], stats["games"]):5.1f}% ({stats['games']} games)") # pad to reach 30 spaces, 5 spaces to have it line up nice


# print role comps (3 or more) would be really cluttered with less
# i also like this one. you can see who is weak on what. gotta play more though
# proccess is super similar to above, but role_comps have a function to get the size instead.
print("\n===== ROLE-BASED COMPS =====")

# print in order of smallest to largest team size first
team_sizes = sorted({role_comp_team_size(role_comp) for role_comp in role_comp_stats})

# print all games for each size
for size in team_sizes:
    # use list comprehension to make a new list
    # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
    # result is a list of tuples: (("aiden", "luke"), {"wins": 1.....}), and so on
    sized_role_comps = [
        (role_comp, stats) # we are adding comps and their stats to the list, output
        for role_comp, stats in role_comp_stats.items() # this gets all comps, iteration
        if role_comp_team_size(role_comp) == size and stats["games"] > 2 # need at least 3 games. theres not much of a pattern before that. the clutter is crazy. you can change it if youd like to play around
    ]

    # if its empty, we dont print the title card and move on
    if not sized_role_comps:
        continue
    
    print(f"\n----- {size}-PLAYER COMPS -----")

    # we have the comps for this size, print them nicely
    sized_role_comps.sort(key=sized_comps_sort_key, reverse=True)
    for role_comp, stats in sized_role_comps:
        print(f"{role_comp:50} {winrate(stats['wins'], stats['games']):5.1f}% ({stats['games']} games)")