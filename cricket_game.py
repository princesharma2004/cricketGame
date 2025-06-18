from os import system
from typing import List

from cricketer import Cricketer

team1Batsmans : List[Cricketer] = []
team1Bowlers : List[Cricketer] = []
team1Run = 0

team2Batsmans : List[Cricketer] = []
team2Bowlers : List[Cricketer] = []
team2Run = 0

# team1 data entry
print("********** team 1 **********")
print()
print("6 Batsman in team 1 :")
for jerseyNumber in range(1, 6+1):
    print("Enter name of player : ", end="")
    name = input()
    cricketer = Cricketer(name, jerseyNumber)
    team1Batsmans.append(cricketer)
print("4 Bowler in team 1 :")
for jerseyNumber in range(7, 10+1):
    print("Enter name of player : ", end="")
    name = input()
    cricketer = Cricketer(name, jerseyNumber)
    team1Bowlers.append(cricketer)
print()

# team2 data entry
print("********** team 2 **********")
print()
print("6 Batsman in team 2 :")
for jerseyNumber in range(1, 6+1):
    print("Enter name of player : ", end="")
    name = input()
    cricketer = Cricketer(name, jerseyNumber)
    team2Batsmans.append(cricketer)
print("4 Bowler in team 2 :")
for jerseyNumber in range(7, 10+1):
    print("Enter name of player : ", end="")
    name = input()
    cricketer = Cricketer(name, jerseyNumber)
    team2Bowlers.append(cricketer)
print()

# game data entry
system('cls||clear')
print("Enter overs : ", end="")
overs = int(input())

# team1 batting
currOver=0
currBatsman=0
battingTeam = team1Batsmans + team1Bowlers

currBowler=0
bowlingTeam = team2Bowlers

while currOver<overs and currBatsman<len(battingTeam):
    balls=0

    while balls<6 and currBatsman<len(battingTeam):
        batsmanNumber = battingTeam[currBatsman].batting()
        bowlerNumber = bowlingTeam[currBowler].bowling()

        if batsmanNumber == bowlerNumber:
            currBatsman+=1
        else:
            team1Run+=batsmanNumber

        balls+=1

    currBowler=(currBowler+1)%4
    currOver+=1

# team2 batting
currOver=0
currBatsman=0
battingTeam = team2Batsmans + team2Bowlers

currBowler=0
bowlingTeam = team1Bowlers

while currOver<overs and currBatsman<len(battingTeam):
    balls=0

    while balls<6 and currBatsman<len(battingTeam):
        batsmanNumber = battingTeam[currBatsman].batting()
        bowlerNumber = bowlingTeam[currBowler].bowling()

        if batsmanNumber == bowlerNumber:
            currBatsman+=1
        else:
            team2Run+=batsmanNumber

        balls+=1

    currBowler=(currBowler+1)%4
    currOver+=1

# result
system('cls||clear')
print(f'team1 run: {team1Run} / team2 run: {team2Run}')
print()

if team1Run > team2Run:
    print(f'team1 wins with {team1Run-team2Run} runs!')
elif team2Run > team1Run:
    print(f'team2 wins with {team2Run-team1Run} runs!')
else:
    print('match draw!')
