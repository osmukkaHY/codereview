from werkzeug.security import check_password_hash

from query import query



    
def user_exists(username: str) -> bool:
    return True if query().select('1')             \
                          .from_('Users')          \
                          .where('username = ?')   \
                          .execute(username)       \
                          .fetchone()              \
    else False


def validate_user(username: str, password: str) -> bool:
    if not user_exists(username):
        return False
    password_hash = query().select('username, password_hash')  \
                           .from_('Users')                     \
                           .where('username = ?')              \
                           .execute(username)                  \
                            .fetchone()[1]

    return check_password_hash(password_hash, password)


def create_user(username: str, password_hash: str) -> bool:
    if user_exists(username):
        return False
    return True if query().insert_into('Users (username, password_hash)')  \
                          .values('(?, ?)')                                \
                          .execute(username, password_hash)                \
                          .lastrowid                                       \
    else False


def delete(username: str) -> bool:
    if not user_exists(username):
        return False
    
    return True if query().delete('')              \
                          .from_('Users')          \
                          .where('username = ?')   \
                          .execute(username)       \
                          .rowcount                \
    else False
