from app import app, db
from app.models import Contact, User, Shop, user_shop

@app.shell_context_processor
def make_context():
    return { 'db': db, 'User': User, 'Contact': Contact, 'Shop': Shop, 'user_shop': user_shop }