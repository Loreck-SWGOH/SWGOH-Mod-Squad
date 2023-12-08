from flask import current_app as app


class Campaign():
    def __init__(self, cid, name):
        self.id = cid
        self.name = name

    # @staticmethod
    # def update(uid, ally_code):
    #     """ Retrieve data from SWGOH, update local DB """
    #     swgoh = SWGOH(ally_code)
    #     user_data = swgoh.get(["name", "clan"])
    #     if json is not None:
    #         try:
    #             rows = app.db.execute(
    #                 """
    #                 UPDATE Profiles
    #                 SET allyCode = :allyCode, clan = :clan, name = :name
    #                 WHERE userID = :uid
    #                 RETURNING userID
    #                 """,
    #                 uid=uid, allyCode=ally_code, clan=user_data["clan"],
    #                 name=user_data["name"])

    #             id = rows[0][0]
    #             return Profile.get(id)

    #         except Exception as e:
    #             print(str(e))
    #             return None

    #     return None

    @staticmethod
    def get(id):
        rows = app.db.execute(
            """
            SELECT ID, name
            FROM Campaigns
            WHERE ID = :id
            """, id=id)

        return Campaign(*(rows[0])) if rows else None
