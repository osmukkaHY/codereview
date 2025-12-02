from werkzeug.security import check_password_hash

from query import query



    
def exists(username: str) -> bool:
    return True if query().select('1')             \
                          .from_('Users')          \
                          .where('username = ?')   \
                          .execute(username)       \
                          .fetchone()              \
    else False


def validate(username: str, password: str) -> bool:
    if not exists(username):
        return False
    password_hash = query().select('username, password_hash')  \
                           .from_('Users')                     \
                           .where('username = ?')              \
                           .execute(username)                  \
                           .fetchone()[1]

    return check_password_hash(password_hash, password)


def create(username: str, password_hash: str) -> bool:
    if exists(username):
        return False
    return True if query().insert_into('Users (username, password_hash)')  \
                          .values('(?, ?)')                                \
                          .execute(username, password_hash)                \
                          .lastrowid                                       \
    else False


def delete(user_id: int) -> bool:
    if not exists(user_id):
        return False
    
    return True if query().delete('')           \
                          .from_('Users')       \
                          .where('user_id = ?') \
                          .execute(user_id)     \
                          .rowcount             \
    else False
