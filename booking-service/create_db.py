from app import app, db

# Ensure that the app context is pushed
with app.app_context():
    print("Database created successfully!")
    db.create_all()
    print("Database created successfully!")
