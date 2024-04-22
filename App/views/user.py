from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import db, Workout, Routine

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')



@user_views.route('/find_workout', methods=['POST'])
def find_workout():
    # Fetch user input from the form
    muscle_group = request.form.get('muscle_group')
    url = "https://work-out-api1.p.rapidapi.com/search"
    querystring = {"Muscles": muscle_group}  # Dynamic query based on user input
    headers = {
        "X-RapidAPI-Key": "e4da15d44bmshf6bc34dd6467518p191a19jsn70b01b907d7a",
        "X-RapidAPI-Host": "work-out-api1.p.rapidapi.com"
    }

    response = request.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        workouts = response.json()
        return render_template('workouts.html', workouts=workouts)
    else:
        return jsonify({"error": "Failed to fetch workouts", "status_code": response.status_code})
        
def store_workouts(workouts):
    for item in workouts:
        # Check if the workout already exists to avoid duplication
        if not Workout.query.filter_by(name=item['name']).first():
            workout = Workout(
                muscle_group=item['muscle_group'],
                name=item['name'],
                intensity_level=item.get('intensity_level', 'Moderate'),
                beginner_sets=item.get('beginner_sets', ''),
                intermediate_sets=item.get('intermediate_sets', ''),
                expert_sets=item.get('expert_sets', ''),
                equipment=item.get('equipment', 'None'),
                explanation=item.get('explanation', ''),
                long_explanation=item.get('long_explanation', ''),
                video_url=item.get('video_url', '')
            )
            db.session.add(workout)
    db.session.commit()


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

#@user_views.route('/workout-finder')
#def workout_finder():
 #   return render_template('workout_finder.html')

@user_views.route('/workout-finder')
def workout_finder():
    muscle_groups = [
        'Biceps', 'Triceps', 'Chest', 'Back', 'Legs', 
        'Abs', 'Stretching', 'Warm Up', 'Lats', 'Hamstring', 
        'Calves', 'Quadriceps', 'Trapezius', 'Shoulders', 'Glutes'
    ]
    return render_template('workout_finder.html', muscle_groups=muscle_groups)

@user_views.route('/create_routine', methods=['GET', 'POST'])
def create_routine():
    if request.method == 'POST':
        data = request.get_json()
        routine_name = data['routine_name']
        workout_ids = data['workouts']

        # Assume a function to handle the logic of creating a routine
        success = create_new_routine(routine_name, workout_ids, user_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Unable to create routine'}, 400)

    return render_template('create_routine.html')


@user_views.route('/add_workout_to_routine/<int:workout_id>', methods=['POST'])
@jwt_required()
def add_workout_to_routine(workout_id):
    current_user_id = get_jwt_identity()  # Get the identity from the JWT

    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({'status': 'error', 'message': 'Workout not found'}), 404

    # Assuming the user has a default routine
    routine = Routine.query.filter_by(user_id=current_user_id).first()
    if not routine:
        routine = Routine(user_id=current_user_id, name="Default Routine")
        db.session.add(routine)

    if workout in routine.workouts:
        return jsonify({'status': 'error', 'message': 'Workout already in routine'}), 409

    routine.workouts.append(workout)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Workout added successfully'})

















#i like pie
#apple?
#yes #g