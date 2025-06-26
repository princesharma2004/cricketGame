from os import system
from typing import List, Dict, Sequence, Any

from database import DB
from cricketer import Cricketer
from userio import add_cricketer, delete_cricketer, update_cricketer_name, update_cricketer_playerType
from userio import add_team, delete_team, update_team_name, add_players_in_team, remove_players_in_team
from userio import enter_match_details
from userio import print_table

database = DB()

def main():
    choice=0

    while True:
        try:
            system('cls||clear')
            print("********** Cricket Game **********")
            print()
            print("***** Crickter Functions *****")
            print("1. add cricketer")
            print("2. update cricketer name")
            print("3. update cricketer playerType")
            print("4. delete cricketer")
            print("5. print cricketers")
            print()
            print("***** Team Functions *****")
            print("6. add team")
            print("7. update team name")
            print("8. delete team")
            print("9. add players in team")
            print("10. remove players in team")
            print("11. print teams")
            print()
            print("***** Match Functions *****")
            print("12. play Match")
            print("13. print Matches")
            print()
            print("***** Game Functions *****")
            print("14. quit")
            print()
            print("Enter Your Choice: ", end="")
            choice=int(input())

            if choice==1:
                data = add_cricketer()
                database.create_cricketer(name=data["name"], playerType=data["playerType"])
            elif choice==2:
                data = update_cricketer_name()
                database.update_cricketer(id=int(data["id"]), name=data["name"])
            elif choice==3:
                data = update_cricketer_playerType()
                database.update_cricketer(id=int(data["id"]), playerType=data["playerType"])
            elif choice==4:
                data = delete_cricketer()
                database.delete_cricketer(id=int(data["id"]))
            elif choice==5:
                print_table(msg="***** Cricketers Table *****", table=database.read_cricketers())
            elif choice==6:
                data = add_team()
                database.create_team(name=data["name"])
            elif choice==7:
                data = update_team_name()
                database.update_team(id=int(data["id"]), name=data["name"])
            elif choice==8:
                data = delete_team()
                database.delete_team(id=int(data["id"]))
            elif choice==9:
                data = add_players_in_team(database.read_cricketers())
                for id in list(data["ids"]):
                    database.update_cricketer(id=id, teamId=data["teamId"])
            elif choice==10:
                data = remove_players_in_team(database.read_cricketers())
                for id in list(data["ids"]):
                    database.update_cricketer(id=id)
            elif choice==11:
                print_table(msg="***** Teams Table *****", table=database.read_teams())
            elif choice==12:
                data = enter_match_details(table=database.read_teams())
                if validate_team(int(data["team1ID"]), database.read_cricketers()) and validate_team(int(data["team2ID"]), database.read_cricketers()):
                    rows = database.read_cricketers().get("data", [])
                    team1=[Cricketer(id=int(row[0]), name=row[1], playerType=row[2]) for row in rows if row[3] == int(data["team1ID"])]
                    team2=[Cricketer(id=int(row[0]), name=row[1], playerType=row[2]) for row in rows if row[3] == int(data["team2ID"])]

                    update = play_match(team1=team1, team2=team2, overs=int(data["overs"]))
                    
                    database.create_match(team1Id=int(data["team1ID"]), team2Id=int(data["team2ID"]),
                                          team1Runs=update["team1Runs"], team2Runs=update["team2Runs"], overs=int(data["overs"]))
            elif choice==13:
                print_table(msg="***** Matches Table *****", table=database.read_matches())
            elif choice==14:
                break
            else:
                continue

        except Exception as error:
            print(error)
        finally:
            if choice!=14:
                print()
                print("Press Enter For Main Menu")
                input()
                continue
            else :
                database.close()

def validate_team(team_id: int, table: Dict[str, Sequence[Any]]) -> bool:
    rows = table.get("data", [])

    team_players = [row for row in rows if row[3] == team_id]
    total_players = len(team_players)

    bowlers = sum(1 for row in team_players if row[2] in ('bowler', 'allrounder'))

    if total_players == 10 and bowlers >= 4:
        return True
    else:
        return False
    
def play_match(team1: List[Cricketer], team2: List[Cricketer], overs: int) -> Dict[str, int]:
    team1Runs = 0
    team2Runs = 0
    # team1 batting
    currOver=0
    currBatsman=0
    battingTeam = team1

    currBowler = 0
    bowlingTeam = [cricketer for cricketer in team2 if cricketer.playerType in ['bowler', 'allrounder']]

    while currOver<overs and currBatsman<len(battingTeam):
        balls=0

        while balls<6 and currBatsman<len(battingTeam):
            batsmanNumber = battingTeam[currBatsman].batting()
            bowlerNumber = bowlingTeam[currBowler].bowling()

            if batsmanNumber == bowlerNumber:
                currBatsman+=1
            else:
                team1Runs+=batsmanNumber

            balls+=1

        currBowler=(currBowler+1)%4
        currOver+=1

    # team2 batting
    currOver=0
    currBatsman=0
    battingTeam = team2

    currBowler=0
    bowlingTeam = [cricketer for cricketer in team1 if cricketer.playerType in ['bowler', 'allrounder']]

    while currOver<overs and currBatsman<len(battingTeam):
        balls=0

        while balls<6 and currBatsman<len(battingTeam):
            batsmanNumber = battingTeam[currBatsman].batting()
            bowlerNumber = bowlingTeam[currBowler].bowling()

            if batsmanNumber == bowlerNumber:
                currBatsman+=1
            else:
                team2Runs+=batsmanNumber

            balls+=1

        currBowler=(currBowler+1)%4
        currOver+=1

    return {"team1Runs": team1Runs, "team2Runs": team2Runs}

main()
