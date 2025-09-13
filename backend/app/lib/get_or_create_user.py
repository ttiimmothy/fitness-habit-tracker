from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User


def get_or_create_user(db: Session, user_id: str, user_name: str, user_email: str, user_picture: str):
  user = db.query(User).filter(User.google_sub == user_id).first()
  print("user")
  print(user)
  if user:
    return user
  user = db.query(User).filter(User.email == user_email).first()
  if user:
    user.avatar_url = user_picture
    user.google_sub = user_id
    db.commit()
    db.refresh(user)
    return user
  new_user = User(name=user_name, email=user_email, google_sub=user_id, avatar_url=user_picture)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
