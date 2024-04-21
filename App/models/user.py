from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    muscle_group = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    intensity_level = db.Column(db.String(120))
    beginner_sets = db.Column(db.String(255))
    intermediate_sets = db.Column(db.String(255))
    expert_sets = db.Column(db.String(255))
    equipment = db.Column(db.String(255))
    explanation = db.Column(db.Text)
    long_explanation = db.Column(db.Text)
    video_url = db.Column(db.String(255))

    def __init__(self, muscle_group, name, intensity_level, beginner_sets, intermediate_sets, expert_sets, equipment, explanation, long_explanation, video_url):
        self.muscle_group = muscle_group
        self.name = name
        self.intensity_level = intensity_level
        self.beginner_sets = beginner_sets
        self.intermediate_sets = intermediate_sets
        self.expert_sets = expert_sets
        self.equipment = equipment
        self.explanation = explanation
        self.long_explanation = long_explanation
        self.video_url = video_url

    def get_json(self):
        return {
            'id': self.id,
            'muscle_group': self.muscle_group,
            'name': self.name,
            'intensity_level': self.intensity_level,
            'beginner_sets': self.beginner_sets,
            'intermediate_sets': self.intermediate_sets,
            'expert_sets': self.expert_sets,
            'equipment': self.equipment,
            'explanation': self.explanation,
            'long_explanation': self.long_explanation,
            'video_url': self.video_url
        }

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workouts = db.relationship('Workout', secondary='routine_workout', backref='routines')

# RoutineWorkout association table
routine_workout = db.Table('routine_workout',
    db.Column('routine_id', db.Integer, db.ForeignKey('routine.id'), primary_key=True),
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), primary_key=True),
    db.Column('order', db.Integer)  # Optional: to specify the order of workouts in a routine
)




