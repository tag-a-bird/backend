from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from ...models import Record, User, Annotation, QueryConfig
from ...db import db_session, func
from tag_a_bird_backend.static.species import most_possible_birds, other_possible_birds
from tag_a_bird_backend.static.flags import flags_list

annotation_bp = Blueprint('annotation', __name__, template_folder='templates', static_folder='static')

@annotation_bp.route('/annotate', methods=["GET", "POST"])
@login_required
async def annotate():
    async def get_record(countries, with_annotation: bool=True, not_in_status: list=['draft', 'reported'], in_status: list=['questioned']):
        try:
            record = db_session.query(Record).filter(Record.country == func.any(countries)).filter(Record.species != []).order_by(func.random()).first()
            users_annotations = db_session.query(User).filter(current_user.id == User.id).first().annotations
            if users_annotations:
                related_records = [db_session.query(Record).filter(Record.id == annotation.recording_id).first() for annotation in users_annotations]
                while record in related_records:
                    record = db_session.query(Record).filter(Record.country == func.any(countries)).filter(Record.species != None).order_by(func.random()).first()
            return record
        except AttributeError as e:
            flash("No records found")
            record = str(e)
            return record

    if request.method == "GET":
        countries = db_session.query(QueryConfig).filter_by(parameter='country').first().value.split(',')
        with_annotation = db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value
        not_in_status = db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value.split(',')
        in_status = db_session.query(QueryConfig).filter_by(parameter='in_status').first().value.split(',')
        new_record = await get_record(countries, with_annotation, not_in_status, in_status)
        return render_template('annotate.html', record=new_record, most_possible_birds=most_possible_birds, other_possible_birds=other_possible_birds)

    elif request.method == "POST":
        try:
            content_type = request.headers['Content-Type']
            if content_type == 'application/json':
                data = request.get_json()
                recordId = data.pop('recordId')
                for key in data.keys():
                    labels = data[key]
                    birds = [bird for bird in labels if bird in most_possible_birds or bird in other_possible_birds]
                    flags = [flag for flag in labels if flag in flags_list]
                    new_annotation = Annotation(
                        start_time=key.split('-')[0], 
                        end_time=key.split('-')[1], 
                        label=birds, 
                        recording_id=recordId, 
                        user_id=current_user.id, 
                        status=flags
                    )
                    db_session.add(new_annotation)
            db_session.commit()
            print("Annotation added successfully")
            print(data)
            return "/annotate"
        except Exception as e:
            print(e)
            db_session.rollback()
            flash('Error: ' + str(e))
            return redirect(url_for('annotation.annotate'))