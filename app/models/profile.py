from flask import current_app as app
import json
from datetime import datetime

from app.utils.swgoh import SWGOH


class Profile():
    def __init__(self, uid, ally_code, name, clan, join_date):
        self.id = uid
        self.ally_code = ally_code
        self.swgoh_name = name
        self.clan = clan
        self.join_date = join_date

    @staticmethod
    def initialize(uid):
        timestamp = datetime.utcnow()
        try:
            rows = app.db.execute(
                """
                INSERT INTO Profiles(userID, joinDate)
                VALUES(:uid, :timestamp)
                RETURNING id
                """,
                uid=uid,
                timestamp=timestamp)

            id = rows[0][0]
            return Profile.get(id)

        except Exception as e:
            # likely email already in use; improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def update(uid, ally_code):
        """ Retrieve data from SWGOH, update local DB """
        swgoh = SWGOH(ally_code)
        user_data = swgoh.get(["name", "clan"])
        if json is not None:
            try:
                rows = app.db.execute(
                    """
                    UPDATE Profiles
                    SET allyCode = :allyCode, clan = :clan, name = :name
                    WHERE userID = :uid
                    RETURNING userID
                    """,
                    uid=uid, allyCode=ally_code, clan=user_data["clan"],
                    name=user_data["name"])

                id = rows[0][0]
                return Profile.get(id)

            except Exception as e:
                print(str(e))
                return None

        return None

    @staticmethod
    def get(id):
        rows = app.db.execute(
            """
            SELECT userID, allyCode, name, clan, joinDate
            FROM Profiles
            WHERE userID = :id
            """, id=id)

        return Profile(*(rows[0])) if rows else None
