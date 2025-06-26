import os
from typing import Optional, Dict, Any, Sequence
from dotenv import load_dotenv
import psycopg2


class DB:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    

    def __init__(self) -> None:
        if self._initialized:
            return

        self._conn = None
        self._cur = None

        try:
            load_dotenv()

            dbname = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")

            self._conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
            self._cur = self._conn.cursor()

            self._cur.execute("""CREATE TABLE IF NOT EXISTS teams (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(50) UNIQUE NOT NULL
                                );""")
            
            self._cur.execute("""CREATE TABLE IF NOT EXISTS cricketers (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(50) NOT NULL,
                                    playerType VARCHAR(11) CHECK (playerType IN ('batsman', 'bowler', 'allrounder')),
                                    teamId INT DEFAULT NULL,
                                    CONSTRAINT fk_team FOREIGN KEY (teamId) REFERENCES teams(id) ON DELETE SET NULL
                                );""")
            
            self._cur.execute("""CREATE TABLE IF NOT EXISTS matches (
                                    id SERIAL PRIMARY KEY,
                                    team1Id INT NOT NULL,
                                    team2Id INT NOT NULL,
                                    team1Runs INT NOT NULL,
                                    team2Runs INT NOT NULL,
                                    overs INT NOT NULL,
                                    result VARCHAR(20) NOT NULL CHECK (result IN ('team1', 'team2', 'tie')),
                                    CONSTRAINT fk_team1 FOREIGN KEY (team1Id) REFERENCES teams(id) ON DELETE CASCADE,
                                    CONSTRAINT fk_team2 FOREIGN KEY (team2Id) REFERENCES teams(id) ON DELETE CASCADE
                                );""")

            self._conn.commit()
            self._initialized = True

        except Exception as error:
            print(error)


    # ---------- CRICKTER CRUD ----------
    def create_cricketer(self, name: str, playerType: str) -> None:
        if playerType not in ['batsman', 'bowler', 'allrounder']:
            print("Player Type is invalid!")
            return

        if self._cur is None or self._conn is None:
            print("Database connection is not available!")
            return

        try:
            self._cur.execute("INSERT INTO cricketers (name, playerType) VALUES (%s, %s);", (name, playerType))
            self._conn.commit()
            print("Cricketer created successfully!")
        except Exception as error:
            self._conn.rollback()
            print("Error inserting cricketer:", error)


    def read_cricketers(self) -> Dict[str, Sequence[Any]]:
        if self._cur is None or self._conn is None:
            print("Database connection is not available!")
            return {}
        
        try:
            self._cur.execute("SELECT id, name, playerType, teamId FROM cricketers;")
            rows = self._cur.fetchall()
            return {"headers": ["id", "name", "playerType", "teamId"], "data": rows}
        except Exception as e:
            print("Error:", e)
            return {}


    def update_cricketer(self, id: int, name: Optional[str] = None, playerType: Optional[str] = None, teamId: Optional[int] = None) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return

        try:
            if name is not None:
                self._cur.execute("UPDATE cricketers SET name=%s WHERE id=%s", (name, id))
            if playerType is not None:
                self._cur.execute("UPDATE cricketers SET playerType=%s WHERE id=%s", (playerType, id))
            if teamId is not None:
                self._cur.execute("UPDATE cricketers SET teamId=%s WHERE id=%s", (teamId, id))
            if name is None and playerType is None and teamId is None:
                self._cur.execute("UPDATE cricketers SET teamId=%s WHERE id=%s", (None, id))
            self._conn.commit()
            print("Cricketer updated successfully!")
        except Exception as error:
            self._conn.rollback()
            print("Error updating cricketer", error)


    def delete_cricketer(self, id: int) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return
        
        try:
            self._cur.execute("DELETE FROM cricketers WHERE id=%s", (id,))
            self._conn.commit()
            print("Cricketer deleted successfully!")
        except Exception as error:
            self._conn.rollback()
            print("Error deleting cricketer", error)


    # ---------- TEAM CRUD ----------
    def create_team(self, name: str) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return

        try:
            self._cur.execute("INSERT INTO teams (name) VALUES (%s);", (name,))
            self._conn.commit()
            print("Team created successfully!")
        except Exception as e:
            self._conn.rollback()
            print("Error creating team:", e)

    def read_teams(self) -> Dict[str, Sequence[Any]]:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return {}

        try:
            self._cur.execute("SELECT id, name FROM teams;")
            rows = self._cur.fetchall()
            return {"headers": ["id", "name"], "data": rows}
        except Exception as e:
            print("Error reading teams:", e)
            return {}

    def update_team(self, id: int, name: str) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return

        try:
            self._cur.execute("UPDATE teams SET name=%s WHERE id=%s;", (name, id))
            self._conn.commit()
            print("Team updated successfully!")
        except Exception as e:
            self._conn.rollback()
            print("Error updating team:", e)

    def delete_team(self, id: int) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return

        try:
            self._cur.execute("DELETE FROM teams WHERE id=%s;", (id,))
            self._conn.commit()
            print("Team deleted successfully!")
        except Exception as e:
            self._conn.rollback()
            print("Error deleting team:", e)


    # ---------- MATCH CR ----------
    def create_match(self, team1Id: int, team2Id: int, team1Runs: int, team2Runs: int, overs: int) -> None:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return

        try:
            if team1Runs > team2Runs:
                result = "team1"
            elif team2Runs > team1Runs:
                result = "team2"
            else:
                result = "tie"

            self._cur.execute("""INSERT INTO matches (team1Id, team2Id, team1Runs, team2Runs, overs, result)
                              VALUES (%s, %s, %s, %s, %s, %s);""",(team1Id, team2Id, team1Runs, team2Runs, overs, result))

            self._conn.commit()
            print("Match created successfully!")
        except Exception as e:
            self._conn.rollback()
            print("Error creating match:", e)

    def read_matches(self) -> Dict[str, Sequence[Any]]:
        if self._cur is None or self._conn is None:
            print("Database connection is not available.")
            return {}

        try:
            self._cur.execute("""SELECT id, team1Id, team2Id, team1Runs, team2Runs, overs, result FROM matches;""")
            rows = self._cur.fetchall()
            return {"headers": ["id", "team1Id", "team2Id", "team1Runs", "team2Runs", "overs", "result"], "data": rows}
        except Exception as e:
            print("Error reading matches:", e)
            return {}
        
    def close(self):
        if self._cur:
            self._cur.close()
            self._cur = None
        if self._conn:
            self._conn.close()
            self._conn = None
        print("Database connection closed.")
