from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
import requests

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

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        workouts = response.json()
        return render_template('workouts.html', workouts=workouts)
    else:
        return jsonify({"error": "Failed to fetch workouts", "status_code": response.status_code})


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



@user_views.route('/add_routine', methods=['POST'])
@jwt_required()
def add_routine():
    routine_name = request.form.get('routine_name')
    new_routine = Routine(name=routine_name, user_id=current_user.id)
    db.session.add(new_routine)
    db.session.commit()
    flash('Routine created successfully!')
    return redirect(url_for('user_views.manage_routines'))

@user_views.route('/manage_routines')
@jwt_required()
def manage_routines():
    routines = Routine.query.filter_by(user_id=current_user.id).all()
    return render_template('routines.html', routines=routines)

@user_views.route('/add_workout_to_routine', methods=['POST'])
@jwt_required()
def add_workout_to_routine():
    routine_id = request.form.get('routine_id')
    workout_id = request.form.get('workout_id')
    routine = Routine.query.get(routine_id)
    workout = Workout.query.get(workout_id)
    if workout not in routine.workouts:
        routine.workouts.append(workout)
        db.session.commit()
        flash('Workout added to routine successfully!')
    else:
        flash('Workout already in routine')
    return redirect(url_for('user_views.manage_routines'))

@user_views.route('/remove_workout_from_routine', methods=['GET'])
@jwt_required()
def remove_workout_from_routine():
    routine_id = request.args.get('routine_id')
    workout_id = request.args.get('workout_id')
    routine = Routine.query.get(routine_id)
    workout = Workout.query.get(workout_id)
    if workout in routine.workouts:
        routine.workouts.remove(workout)
        db.session.commit()
        flash('Workout removed from routine successfully!')
    return redirect(url_for('user_views.manage_routines'))














#i like pie
#apple?
#yes #g