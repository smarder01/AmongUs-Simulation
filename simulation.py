#making a simulation of an among us game based on the stats in the xlsx file
# %%
# Import necessary libraries
import pandas as pd
import numpy as np
import random
from collections import Counter

# %%
# Define file path
file_path = "./Sidemen Among Us.xlsx"

# Load Excel sheets
df_players = pd.read_excel(file_path, sheet_name="Player Stats")  # Player statistics
df_imposter_combos = pd.read_excel(file_path, sheet_name="Imposter Combinations")  # Imposter pair data
df_game_stats = pd.read_excel(file_path, sheet_name="Game Stats")  # Overall game stats

# Fill missing values with 0
df_players.fillna(0, inplace=True)
df_imposter_combos.fillna(0, inplace=True)
df_game_stats.fillna(0, inplace=True)

# %%
# Define relevant columns for player stats
relevant_columns = [
    'Name', 'Games Played', 'Win %', 
    'Kills as Imposter', 'Kills Per Imposter Game', 'Imposter Games', 'Imposter Win %',
    'Crewmate Games', 'Crewmate Win %', 'Tasks Completed', 'Task Completion %',
    'Total Tasks', 'All Tasks Completed',
    'Voted out', 'Voted out First', 'Emergency Meetings',
    'Deaths', 'First Death of Game', 'Death in First Round',
    'Bodies Reported', 'Disconnected', 'Rage Quit'
]

# Create a list of players with their stats from Player Stats sheet
players = []
for _, row in df_players.iterrows():
    player = {col: row[col] for col in relevant_columns}  # Extract relevant stats dynamically
    player["Role"] = None  # Role assigned later
    player["Alive"] = True  # Default alive status
    players.append(player)

# %%
# Function to select imposters based on Imposter Win % for more realistic selection
def weighted_imposter_selection(selected_players, num_imposters=2):
    """ Selects imposters based on their historical Imposter Win % """
    weights = [p["Imposter Win %"] if p["Imposter Win %"] > 0 else 1 for p in selected_players]
    imposters = random.choices(selected_players, weights=weights, k=num_imposters)
    return imposters

# %%
# Function to set up the game
def setup_game(players, total_players=10):
    """ Sets up the game by selecting players and assigning roles """
    selected_players = random.sample(players, total_players)

    # Assign imposters based on weighted selection
    imposters = weighted_imposter_selection(selected_players, num_imposters=2)
    
    for player in selected_players:
        player["Role"] = "Imposter" if player in imposters else "Crewmate"

    # Get final counts
    num_imposters = sum(1 for p in selected_players if p["Role"] == "Imposter")
    num_crewmates = total_players - num_imposters

    # Print setup details
    print("\nGame Setup:")
    for player in selected_players:
        print(f"{player['Name']}: {player['Role']}")

    print(f"\nNumber of Imposters: {num_imposters}")
    print(f"Number of Crewmates: {num_crewmates}")

    return selected_players

# %%
# function to simulate task completion
def crewmates_do_tasks(players, total_tasks = 50):
    """ Crew completes tasks based on their task completion %"""
    completed_tasks = 0
    for player in players:
        if player["Role"] == "Crewmate" and player["Alive"]:
            task_success = random.random() < player["Task Completion %"] / 100
            if task_success:
                completed_tasks += 1

    return completed_tasks

# %%
# function to check win conditions
def check_win_conditions(players):
    """ Determines if imposters or crewmates have won """
    alive_imposters = sum(1 for p in players if p["Role"] == "Imposter" and p["Alive"])
    alive_crewmates = sum(1 for p in players if p["Role"] == "Crewmate" and p["Alive"])
    total_tasks_completed = crewmates_do_tasks(players)

    if alive_imposters == alive_crewmates:
        return "Imposters Win!"
    elif alive_imposters == 0:
        return "Crewmates Win!"
    elif total_tasks_completed == 50:
        return "Crewmates Win!"
    else:
        return None

# %%
# function to simulate imposters killing a crewmate
imposter_last_kill = {}

def imposter_kill(players_in_game, imposters, current_round, kill_cooldown=2):
    global imposter_last_kill  # Ensure cooldown tracking persists

    # Ensure imposters have a last kill entry
    for imposter in imposters:
        imposter_name = imposter["Name"]  # Extract name
        if imposter_name not in imposter_last_kill:
            imposter_last_kill[imposter_name] = -kill_cooldown

    # Get available imposters based on cooldown
    available_imposters = [
        imposter for imposter in imposters 
        if (current_round - imposter_last_kill[imposter["Name"]]) >= kill_cooldown
    ]

    if not available_imposters:
        return "Imposters on cooldown. No kills this round."

    # Choose an imposter and kill a crewmate
    killing_imposter = random.choice(available_imposters)
    crewmates = [player for player in players_in_game if player not in imposters]

    if not crewmates:
        return "No crewmates left to kill."

    killed_player = random.choice(crewmates)
    players_in_game.remove(killed_player)

    # Update last kill round for chosen imposter
    imposter_last_kill[killing_imposter["Name"]] = current_round

    return [killed_player]

# %%
# function to simulate reporting a body
def report_body(players):
    """ Players have a chance to report a body based on historical data"""
    alive_players = [p for p in players if p["Alive"]]
    for player in alive_players:
        report_chance = random.random() < (player["Bodies Reported"] / player["Games Played"])
        if report_chance:
            return True
    return False
    
# %%
# function to simulate emergency meeting
def emergency_meeting(players):
    """ randomly triggers an emergency meeting"""
    alive_players = [p for p in players if p["Alive"]]
    for player in alive_players:
        meeting_chance = random.random() < (player["Emergency Meetings"] / player["Games Played"])
        if meeting_chance:
            return True
    return False

# %%
# function to simulate 
def voting_phase(players):
    """ Simulate a voting round where players vote to eject someone or skip, 
    with votes influenced by suspicion from body reports and other stats."""
    
    votes = {}  # Store votes for each player
    skip_votes = []  # Track players who skipped voting
    suspicions = {}  # Track suspicion scores for each player

    # Calculate suspicion score based on body reports and other stats
    for player in players:
        suspicion_score = 0
        
        # Increase suspicion if a player has reported more bodies
        if player["Bodies Reported"] > 0:
            suspicion_score += (player["Bodies Reported"] / player["Games Played"]) * 10  # Scale this factor

        # Additional suspicion factors can be added here (e.g., deaths, first death, etc.)
        if player["Deaths"] > 0:
            suspicion_score += (player["Deaths"] / player["Games Played"]) * 5  # Scale the death factor

        # Store the suspicion score
        suspicions[player["Name"]] = suspicion_score

    # Sort players by their suspicion score (higher scores mean more suspicious)
    sorted_suspects = sorted(suspicions.items(), key=lambda item: item[1], reverse=True)

    # Display the suspicion scores for debugging
    print("\nSuspicion Scores (Higher is more suspicious):")
    for player_name, score in sorted_suspects:
        print(f"{player_name}: {score}")

    # Each player votes, with different strategies for crewmates and imposters
    for player in players:
        if random.random() < 0.1:  # 10% chance that player skips voting
            skip_votes.append(player["Name"])
            votes[player["Name"]] = "Skip"  # Player skips voting
            continue

        # Crewmates vote for imposters, imposters vote to eject crewmates
        if player["Role"] == "Crewmate":
            # Crewmates vote for the most suspicious imposter
            possible_victims = [p["Name"] for p in players if p["Role"] == "Imposter" and p["Alive"]]
        else:
            # Imposters vote for the most suspicious crewmate
            possible_victims = [p["Name"] for p in players if p["Role"] == "Crewmate" and p["Alive"]]

        # Prioritize voting for the most suspicious player
        suspicious_victim = None
        for suspect_name, _ in sorted_suspects:
            if suspect_name in possible_victims:
                suspicious_victim = suspect_name
                break

        # If no suspicious player found in the list, vote randomly
        if not suspicious_victim:
            suspicious_victim = random.choice(possible_victims)
        
        votes[player["Name"]] = suspicious_victim

    # Count votes and find the person with the most votes
    vote_counts = Counter(votes.values())

    # Display voting results
    print("\nVoting Results:")
    for voter, voted in votes.items():
        print(f"{voter} voted for {voted}")

    # Handle skips: If all voted to skip, no one is ejected
    if "Skip" in vote_counts and vote_counts["Skip"] == len(players):
        print("\nAll players skipped voting. No one was ejected.")
        return None

    # Handle ties: If there's a tie for the most votes, no one is ejected
    max_votes = vote_counts.most_common(1)[0][1]
    tied_players = [player for player, count in vote_counts.items() if count == max_votes]
    
    if len(tied_players) > 1:
        print("\nVoting tied. No one was ejected.")
        return None

    # Eject the player with the most votes
    ejected_player = tied_players[0] if len(tied_players) == 1 else None
    print(f"\n{ejected_player} was ejected!")
    return ejected_player
    
# %%
# main game loop
def simulate_game():
    """ Runs a full game simulation """
    players_in_game = setup_game(players)
    total_tasks_completed = 0
    round_num = 1
    imposters = [p for p in players_in_game if p["Role"] == "Imposter"]

    while len(imposters) > 0 and len(imposters) < len(players_in_game):
        print(f"\n--- Round {round_num} ---\nPlayers left: {len(players_in_game)}")

        # Crewmates completing tasks
        tasks_completed = random.randint(1, 5)
        print(f"Tasks Completed This Round: {tasks_completed}")

        # Imposter attempts to kill
        killed_player = imposter_kill(players_in_game, imposters, round_num)

        if isinstance(killed_player, list):  # Ensure kill happened
            print(f"{killed_player[0]['Name']} was killed by an Imposter.")
        else:
            print("No kill happened this round.")

        # Conduct voting
        ejected_player = voting_phase(players_in_game)
        if ejected_player:
            players_in_game = [p for p in players_in_game if p["Name"] != ejected_player]
            imposters = [p for p in players_in_game if p["Role"] == "Imposter"]

        # Check for game-ending conditions
        if len(imposters) == 0:
            print("\n🎉 Crewmates Win!")
            return
        if len(imposters) >= len(players_in_game) / 2:
            print("\n🔥 Imposters Win!")
            return

        round_num += 1

# %%
# Run the game simulation
simulate_game()