from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def get_from_login(email, password):
        """
        Get user info when attempting to login.
        Return None for incorrect email or password. Raise Exception if
        more than one user is found.
        """
        rows = app.db.execute(
            """
            SELECT password, id, email, firstname, lastname
            FROM Users
            WHERE email = :email
            """, email=email)
        if not rows:  # email not found
            return None
        if not check_password_hash(rows[0][0], password):  # incorrect password
            return None
        if len(rows) > 1:
            raise Exception("Database corrupted: " + email + " not unique")

        print(rows)
        return User(*(rows[0][1:]))  # Return everything but password

    @staticmethod
    def email_exists(email):
        """ Check for existing e-mail when registering """
        rows = app.db.execute(
            """
            SELECT email
            FROM Users
            WHERE email = :email
            """, email=email)

        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute(
                """
                INSERT INTO Users(email, password, firstname, lastname)
                VALUES(:email, :password, :firstname, :lastname)
                RETURNING id
                """,
                email=email, password=generate_password_hash(password),
                firstname=firstname, lastname=lastname)

            id = rows[0][0]
            return User.get(id)

        except Exception as e:
            # likely email already in use; improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def is_valid_password(user_id, password):
        rows = app.db.execute(
            """
            SELECT password
            FROM Users
            WHERE ID = :uid
            """,
            uid=user_id)
        return check_password_hash(rows[0][0], password)

    @staticmethod
    def update_password(user_id, cur_password, new_password):
        if User.is_valid_password(user_id, cur_password):
            try:
                rows = app.db.execute(
                    """
                    UPDATE Users SET password = :new_password
                    WHERE ID = :uid
                    RETURNING ID
                    """,
                    uid=user_id,
                    new_password=generate_password_hash(new_password))

                print(rows)
                id = rows[0][0]
                return User.get(id)
            except Exception as e:
                # improve error checking and reporting
                # the following simply prints the error to the console:
                print(str(e))
                return None
        return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute(
            """
            SELECT id, email, firstname, lastname
            FROM Users
            WHERE id = :id
            """, id=id)

        return User(*(rows[0])) if rows else None
