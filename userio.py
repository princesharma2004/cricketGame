from os import system
from tabulate import tabulate
from typing import Dict, Sequence, Any

# ---------- Inputs ----------

# ----- Cricketer Inputs -----
def add_cricketer() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Cricketer Name : ", end="")
    name = input()
    print("Enter Cricketer Type (batsman, bowler, allrounder) : ", end="")
    playerType = input()

    return {"name":name, "playerType":playerType}

def update_cricketer_name() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Cricketer ID : ", end="")
    id = input()
    print("Enter Cricketer new Name : ", end="")
    name = input()

    return {"id": id, "name": name}

def update_cricketer_playerType() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Cricketer ID : ", end="")
    id = input()
    print("Enter Cricketer new playerType : ", end="")
    playerType = input()

    return {"id": id, "playerType": playerType}

def delete_cricketer() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Cricketer ID : ", end="")
    id = input()

    return {"id": id}

# ----- Team Inputs -----
def add_team() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Team Name : ", end="")
    name = input()

    return {"name": name}

def update_team_name() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Team ID : ", end="")
    id = input()
    print("Enter Team new Name : ", end="")
    name = input()

    return {"id": id, "name": name}

def delete_team() -> Dict[str, str]:
    system('cls||clear')
    print("Enter Team ID : ", end="")
    id = input()

    return {"id": id}

def add_players_in_team(table: Dict[str, Sequence[Any]]) ->  Dict[str, Any]:
    print("Enter Team ID : ", end="")
    teamId = input()
    print()
    print_table(msg="***** Cricketers Table *****", table=table)
    print()
    print("Enter List of playersID in this Format -> [1, 2, 3] give 10 and add min 4 player who can ball : ", end="")

    return {"ids": eval(input()), "teamId": teamId}

def remove_players_in_team(table: Dict[str, Sequence[Any]]) ->  Dict[str, Any]:
    print_table(msg="***** Cricketers Table *****", table=table)
    print()
    print("Enter List of playersID in this Format -> [1, 2, 3] : ", end="")

    return {"ids": eval(input())}

# ----- Match Inputs -----
def enter_match_details(table: Dict[str, Sequence[Any]]) -> Dict[str, str]:
    system('cls||clear')
    print_table(msg="***** Teams Table *****", table=table)
    print()
    print("Enter team1 ID : ", end="")
    team1ID = input()
    print("Enter team2 ID : ", end="")
    team2ID = input()
    print("Enter overs : ", end="")
    overs = input()
    return {"team1ID": team1ID, "team2ID": team2ID, "overs": overs}

# ---------- Outputs ----------

def print_table(msg: str, table: Dict[str, Sequence[Any]]) -> None:
    system('cls||clear')
    print(msg)

    if not table["data"]:
        print("it is Empty!")
        return
    
    print(tabulate(table["data"], headers=table["headers"], tablefmt="rounded_grid"))
