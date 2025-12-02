from werkzeug.security import check_password_hash

from query import query



    
def exists(username: str=None, user_id: int=None) -> bool:
    actual_argument = username if username else \
                      user_id  if user_id  else \
                      None
    if not actual_argument:
        return False

    cond = 'username = ?' if username else 'id = ?'
    return True if query().select('1')              \
                          .from_('Users')           \
                          .where(cond)              \
                          .execute(actual_argument) \
                          .fetchone()               \
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
