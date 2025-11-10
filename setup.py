from app import app, db, Camper, Activity, Signup

def setup_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if we already have data
        if not Camper.query.first():
            # Add sample data
            campers = [
                Camper(name="Caitlin", age=8),
                Camper(name="Lizzie", age=9),
                Camper(name="Nicholas Martinez", age=12),
                Camper(name="Zoe", age=11),
                Camper(name="Ashley Delgado", age=11)
            ]
            
            activities = [
                Activity(name="Archery", difficulty=2),
                Activity(name="Swimming", difficulty=3),
                Activity(name="Swim in the lake", difficulty=3),
                Activity(name="Hiking by the stream", difficulty=2),
                Activity(name="Listening to the birds chirp", difficulty=1)
            ]
            
            for camper in campers:
                db.session.add(camper)
            
            for activity in activities:
                db.session.add(activity)
            
            db.session.commit()
            
            # Add some signups
            signups = [
                Signup(camper_id=3, activity_id=4, time=8),
                Signup(camper_id=3, activity_id=5, time=1),
                Signup(camper_id=5, activity_id=3, time=9)
            ]
            
            for signup in signups:
                db.session.add(signup)
            
            db.session.commit()
            print("Sample data added successfully!")
        else:
            print("Database already has data.")

if __name__ == '__main__':
    setup_database()