from db.datebase import session, User

def get_user_by_telegram_id(telegram_id):
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return user