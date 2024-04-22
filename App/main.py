import os

from flask import Flask, render_template, request
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from .models import Workout

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)



from App.views import views

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    app.app_context().push()
    return app

def fetch_workouts_from_api():
    url = "https://work-out-api1.p.rapidapi.com/workouts"
    headers = {
        'X-RapidAPI-Key': 'e4da15d44bmshf6bc34dd6467518p191a19jsn70b01b907d7a',  # Replace with your actual API key
        'X-RapidAPI-Host': 'work-out-api1.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        workouts = response.json()
        return workouts
    else:
        return None

def store_workouts(data):
    if data and 'results' in data:  # Check the correct key based on the API response
        for item in data['results']:
            # Check if workout already exists to prevent duplicates
            if not Workout.query.filter_by(name=item['name']).first():
                workout = Workout(
                    name=item['name'],
                    description=item.get('description'),
                    muscle_group=item.get('muscle_group', 'General'),
                    intensity_level=item.get('intensity_level', 'Moderate'),
                    equipment=item.get('equipment', 'None')
                )
                db.session.add(workout)
        db.session.commit()