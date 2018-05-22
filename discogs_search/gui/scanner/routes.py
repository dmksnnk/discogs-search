from flask import render_template, request, redirect, url_for, session
from . import scanner


@scanner.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print(request.form)
        session['path'] = request.form['path']
        return redirect(url_for('.scan'))


@scanner.route('/scanning')
def scan():
    path = session.get('path')
    if not path:
        return redirect(url_for('.index'))

    return render_template('scanning.html', path=path)