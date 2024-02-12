# from flask_login import UserMixin, login_required
from flask import current_app as app
# from werkzeug.security import generate_password_hash, check_password_hash

# from .. import login


class UserStats():
    """
    Interface to user database table.

    Methods use get(id) to return User object.
    """
    def __init__(self, users, admins):
        self.users = users
        self.admins = admins

    @staticmethod
    def get():
        """
        Retrieve comprehensive user statistics

        If unsuccessful return TBD.
        """
        try:
            rows = app.db.execute(
                """
                SELECT COUNT(*)
                FROM Users
                """)
            num_users = rows[0][0]
        except Exception as e:
            # improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

        try:
            rows = app.db.execute(
                """
                SELECT COUNT(*)
                FROM Users
                WHERE isAdmin = 1
                """)
            admins = rows[0][0]
        except Exception as e:
            # improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

        return UserStats(num_users, admins)
