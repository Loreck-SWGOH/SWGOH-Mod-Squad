from flask_login import UserMixin, login_required
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    """
    Interface to user database table.

    Methods use get(id) to return User object.
    """
    def __init__(self, id, email, first_name, last_name, is_admin):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    @staticmethod
    @login.user_loader
    def get(id):
        """
        Retrieve user info based on database id
        """
        rows = app.db.execute(
            """
            SELECT id, email, firstName, lastName, isAdmin
            FROM Users
            WHERE id = :id
            """, id=id)

        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute(
            """
            SELECT id, email, firstName, lastName, isAdmin
            FROM Users
            """)
        return [User(*row) for row in rows]

    @staticmethod
    def get_from_login(email, password):
        """
        Get user info when attempting to login.

        Return None for incorrect email or password. Raise Exception if
        more than one user is found.
        """
        rows = app.db.execute(
            """
            SELECT password, id
            FROM Users
            WHERE email = :email
            """, email=email)
        if not rows:  # email not found
            return None
        if not check_password_hash(rows[0][0], password):  # incorrect password
            return None
        if len(rows) > 1:
            raise Exception("Database corrupted: " + email + " not unique")

        id = rows[0][1]
        return User.get(id)

    @staticmethod
    def email_exists(email):
        """
        Check for existing e-mail when registering
        """
        rows = app.db.execute(
            """
            SELECT email
            FROM Users
            WHERE email = :email
            """, email=email)

        return len(rows) > 0

    @staticmethod
    def register(email, password, first_name, last_name, is_admin):
        """
        Register a user by adding them to database.

        If unsuccessful, TBD.
        """
        try:
            rows = app.db.execute(
                """
                INSERT INTO Users(email, password,
                                  firstname, lastname, isAdmin)
                VALUES(:email, :password, :firstname, :lastname, :isadmin)
                RETURNING id
                """,
                email=email, password=generate_password_hash(password),
                firstname=first_name, lastname=last_name,
                isadmin=int(is_admin))

            id = rows[0][0]
            return User.get(id)

        except Exception as e:
            # likely email already in use; improve error checking and reporting
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def is_valid_password(user_id, plain_password):
        """
        Check whether the password is valid.
        """
        rows = app.db.execute(
            """
            SELECT password
            FROM Users
            WHERE ID = :uid
            """,
            uid=user_id)

        return check_password_hash(rows[0][0], plain_password)

    @staticmethod
    @login_required
    def update_password(user_id, cur_password, new_hashed_password):
        """
        Change stored password.

        If unsuccessful return TBD.
        """
        if User.is_valid_password(user_id, cur_password):
            try:
                rows = app.db.execute(
                    """
                    UPDATE Users SET password = :new_password
                    WHERE ID = :uid
                    RETURNING ID
                    """,
                    uid=user_id,
                    new_password=new_hashed_password)

                print(rows)
                id = rows[0][0]
                return User.get(id)
            except Exception as e:
                # improve error checking and reporting
                # the following simply prints the error to the console:
                print(str(e))
                return None
        return None
