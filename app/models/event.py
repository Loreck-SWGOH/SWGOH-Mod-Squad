from flask import current_app as app


class Event():
    def __init__(self, eid, name):
        self.id = eid
        self.name = name

    @staticmethod
    def get(id):
        rows = app.db.execute(
            """
            SELECT ID, name
            FROM Events
            WHERE ID = :id
            """, id=id)

        return Event(*(rows[0])) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute(
            """
            SELECT ID, name
            FROM Events
            """)

        return [Event(*row) for row in rows]
