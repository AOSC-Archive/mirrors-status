from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, jsonify
from itsdangerous import JSONWebSignatureSerializer
import rollbar
# from flask_login import login_user, logout_user, login_required

from status.extensions import cache
from status.assets import update_mirror_status
from status.forms import MirrorUpdateForm
from status.models import *

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1)
def home():
    mirrors = Mirror.query.filter(Mirror.main!=True).order_by(Mirror.area.asc()).order_by(Mirror.name.asc()).all()
    repo = Mirror.query.filter_by(main=True).first()
    return render_template('index.html', repo=repo, mirrors=mirrors)


@main.route('/admin-token')
def token():
    data = {"type": "update"}
    serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data)


@main.route('/refresh')
def refresh():
    token = request.args.get('token')
    serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403

    if data.get('type') == 'update':
        mirrors = Mirror.query.all()
        repo = Mirror.query.filter_by(main=True).first()
        repo = update_mirror_status(repo)
        db.session.add(repo)
        db.session.commit()
        for mirror in mirrors:
            mirror = update_mirror_status(mirror)
            db.session.add(mirror)
            db.session.commit()
        return jsonify({'message': str(len(mirrors)) + " updated"}), 200
    else:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403


@main.route('/admin/add-mirror', methods=['GET', 'POST'])
def add_mirror():
    token = request.args.get('token')
    serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403

    if data.get('type') == 'update':
        form = MirrorUpdateForm()
        if form.validate_on_submit():
            mirror = Mirror()
            mirror.area = form.area.data
            mirror.last_update_url = form.last_update_url.data
            mirror.url = form.url.data
            mirror.name = form.name.data
            mirror = update_mirror_status(mirror)
            db.session.add(mirror)
            db.session.commit()

            flash('You have successfully add mirror: ' + mirror.name)
            return redirect(url_for('.add_mirror'))
        return render_template('add_mirror.html', form=form)
    else:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403



@main.route('/admin/update-mirror/<int:id>', methods=['GET', 'POST'])
def update_mirror(id):
    token = request.args.get('token')
    serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403

    if data.get('type') == 'update':
        mirror = Mirror.query.get_or_404(id)
        form = MirrorUpdateForm()
        if form.validate_on_submit():
            mirror.area = form.area.data
            mirror.last_update_url = form.last_update_url.data
            mirror.url = form.url.data
            mirror.name = form.name.data
            mirror = update_mirror_status(mirror)
            db.session.add(mirror)
            db.session.commit()

            flash('You have successfully updated mirror: ' + mirror.name)
            return redirect(url_for('.update_mirror', id=id))
        else:
            form.area.data = mirror.area
            form.last_update_url.data = mirror.last_update_url
            form.url.data = mirror.url
            form.name.data = mirror.name

            return render_template('update_mirror.html', form=form, id=id)
    else:
        rollbar.report_message("Illegal request: " + request.url, 'warning', request=request)
        return 'Forbidden', 403