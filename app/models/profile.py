from flask import current_app as app
import json
from datetime import datetime

from app.utils.swgoh import SWGOH


class Profile():
    def __init__(self, uid, ally_code, swgoh_info, swgoh_name,
                 clan_id, join_date):
        self.id = uid
        self.ally_code = ally_code
        self.swgoh_info = swgoh_info
        self.swgoh_name = swgoh_name
        self.clan_id = clan_id
        self.join_date = join_date

    @staticmethod
    def get(id):
        rows = app.db.execute(
            """
            SELECT userID, allyCode, swgohInfo, swgohName, clanID, joinDate
            FROM Profiles
            WHERE userID = :id
            """, id=id)

        return Profile(*(rows[0])) if rows else None

    @staticmethod
    def initialize(uid):
        """
        Add initial profile.

        Called when users are created. If unsuccessful, TBD.
        """
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
            # improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def update(uid, ally_code, use_swgoh_gg, alt_swgoh_gg):
        """
        Retrieve data from SWGOH, update local DB

        If retrieval from SWGOH or database unsuccessful, then TBD.
        """
        swgoh_info = SWGOH.get_swgoh_site(use_swgoh_gg, alt_swgoh_gg)
        swgoh = SWGOH(swgoh_info, ally_code)
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
