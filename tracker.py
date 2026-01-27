from collections import defaultdict

# MUST BE FORMATTED AS FOLLOWS:
# tank,tank2/dps1,dps2/support1,support2/win(orloss)
# clear explanation and examples are in README, mvp is entirely optional



# || FILE FOR INPUT (THIS IS WHAT YOU ARE LOOKING FOR MOST LIKELY)
# open the formatted file (look in README to generate)
with open("games.txt") as f: # CHANGE games.txt TO MATCH YOUR TEXT FILE. GAMES.TXT IS JUST MY CHOICE
    games = [line.strip() for line in f if line.strip()]



# || DATA MODELS
# make a player, contains most data
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
# helper function to parse mvps out of names
# result is the name minus (mvp) if present and true (for removal) or false (for no need).
def parse_name(name):
    name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True
    return name, False

# parse the notable game stats out of the line, mvp is still included for now
# result is dictionary of the game, showing the tanks, dps, and support, and then a result win or loss
# at this point tank could be something like: luke,mar(mvp).
def parse_game(line):
    tank_player, dps_player, support_player, result = line.split("/")
    return { "tank": tank_player, "dps": dps_player, "support": support_player }, result # return dictionary and result



# helper function for printing
# result is winrate
def winrate(wins, games):
    return (wins / games * 100) if games else 0



# extract players for non role specific winrates
# result is the set of the comp to be updated
def extract_players(team):
    players = set()

    # for each slot of value, split if needed and add to the players set
    for slot in team.values():
        if slot != "none":
            for names in slot.split(","):
                name, _ = parse_name(names) # we arent using is_mvp here. hence _
                players.add(name)
    return players

# get the key of the role comp to be updated
def get_role_comp_key(team):
    players = [] # players like above but as a list. so it matters 

    # we need to get member for tank, dps, and support, just like before. sort each slot alphabetically so it doesnt matter
    for role in ("tank", "dps", "support"):
        slot = team[role] # check each slot
        if slot == "none":
            players.append(f"{role}:none") # this role is empty
        else:
            sorted_players = sorted(slot.split(",")) # split the slot at the ',' and sort the players alphabetically to get one consistent key
            names = ", ".join(sorted_players) # rejoin the list back into a string with a comma (with a space to look better), basically just makes sure we have no duplicate role comp
            players.append(f"{role}:{names}") # add the final string to the list
    return " / ".join(players) # make one final string by joining with /

# sort the comps of a certain size by winrate (games if equal)
def sized_comps_sort_key(comp_stats):
    _, stats = comp_stats
    return (
        winrate(stats["wins"], stats["games"]),
        stats["games"]
    )


    

# || AGGREGATION
# for each game, add relevant stats
for line in games:
    team, result = parse_game(line)

    # add stats for each player from the current game
    for role, names in team.items():
        if names == "none":
            continue

        # if multiple names, split with , and run for each
        for raw in names.split(","):
            name, is_mvp = parse_name(raw) # remove mvp if present

            player_stats[name]["games"] += 1 # yeah man they played a game

            if is_mvp:
                player_stats[name]["mvps"] += 1

            # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is
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



# || PRINTING
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
    print(f"\n----- {size}-PLAYER COMPS -----")

    # use list comprehension to make a new list
    # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
    # result is a list of tuples: (("aiden", "luke"), {"wins": 1.....}), and so on
    sized_comps = [
        (comp, stats) # we are adding comps and their stats to the list, output
        for comp, stats in comp_stats.items() # this gets all comps, iteration
        if len(comp) == size and stats["games"] > 0 # get only comps of this size, filter
    ]

    # sort by winrate, the key is winrate first, games played as backup
    sized_comps.sort(key=sized_comps_sort_key, reverse=True)
    
    # print the comps in order
    for comp, stats in sized_comps:
        names = ", ".join(comp) # combine names for the comp
        print(f"{names:30} {winrate(stats["wins"], stats["games"]):5.1f}% ({stats['games']} games)") # pad to reach 30 spaces, 5 spaces to have it line up nice


# print role comps (3 or more) would be really cluttered with less
# i also like this one. you can see who is weak on what. gotta play more though
print("\n===== ROLE-BASED COMPS =====")
# print in order of smallest to largest team size first
