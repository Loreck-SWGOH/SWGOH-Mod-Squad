from flask import current_app as app


class Profile():
    def __init__(self, uid, ally_code, clan, join_date):
        self.id = uid
        self.ally_code = ally_code
        self.clan = clan
        self.join_date = join_date

    @staticmethod
    def initialize(uid):
        try:
            rows = app.db.execute(
                """
                INSERT INTO Profiles(userID)
                VALUES(:uid)
                RETURNING id
                """,
                uid=uid)

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
        try:
            rows = app.db.execute(
                """
                UPDATE INTO Profiles(userID, allyCode, clan, joinDate)
                VALUES(:uid, :allyCode, :clan, :joinCate)
                RETURNING id
                """,
                uid=uid, allyCode=ally_code, clan=clan,
                joinDate=join_date)

            id = rows[0][0]
            return Profile.get(id)

        except Exception as e:
            # likely email already in use; improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def get(id):
        rows = app.db.execute(
            """
            SELECT userID, ally_code, clan, joinDate
            FROM Profiles
            WHERE userID = :id
            """, id=id)

        return Profile(*(rows[0])) if rows else None
