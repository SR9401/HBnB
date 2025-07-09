from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()     # si tu veux tout reset
    db.create_all()   # crée les tables en fonction de tes modèles
