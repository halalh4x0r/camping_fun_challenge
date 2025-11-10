from server import create_app, db
from server.models import Camper, Activity, Signup

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create campers
        campers = [
            Camper(name="Caitlin", age=8),
            Camper(name="Lizzie", age=9),
            Camper(name="Nicholas Martinez", age=12),
            Camper(name="Zoe", age=11),
            Camper(name="Ashley Delgado", age=11)
        ]
        
        for camper in campers:
            db.session.add(camper)
        
        # Create activities
        activities = [
            Activity(name="Archery", difficulty=2),
            Activity(name="Swimming", difficulty=3),
            Activity(name="Swim in the lake", difficulty=3),
            Activity(name="Hiking by the stream", difficulty=2),
            Activity(name="Listening to the birds chirp", difficulty=1)
        ]
        
        for activity in activities:
            db.session.add(activity)
        
        db.session.commit()
        
        # Create signups
        signups = [
            Signup(camper_id=3, activity_id=4, time=8),
            Signup(camper_id=3, activity_id=5, time=1),
            Signup(camper_id=5, activity_id=3, time=9)
        ]
        
        for signup in signups:
            db.session.add(signup)
        
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()