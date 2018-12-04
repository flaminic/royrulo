from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask_basicauth import BasicAuth
from database import Database
import io
import csv

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
database = Database()

basic_auth = BasicAuth(app)


# Templates
@app.route("/")
def home():
    return render_template('index.html', page_name="home")


@app.route("/cerimonia")
def cerimonia():
    return render_template('cerimonia.html', page_name="cerimonia")


@app.route("/ricevimento")
def ricevimento():
    return render_template('ricevimento.html', page_name="ricevimento")


@app.route("/rsvp")
def rsvp():
    return render_template('rsvp.html', page_name="rsvp")


@app.route("/rsvp/<person_id>")
def edit_rsvp(person_id):
    person_details_info = database.get_person_details(person_id)
    if person_details_info:
        return render_template('editRsvp.html', person_details_info=person_details_info)
    else:
        return redirect(url_for('home'))


@app.route("/grazie/<person_id>")
def thanks(person_id):
    return render_template('thanks.html', person_id=person_id)


@app.route("/all-rsvp")
@basic_auth.required
def get_all_rsvp():
    rows = database.get_all_people();
    return render_template("allRsvp.html", rows=rows)


@app.route('/download-rsvp')
@basic_auth.required
def download():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'guestName', 'email', 'howMany', 'diet', ])

    rows = database.get_all_people();
    for row in rows:
        cw.writerow([row['id'], row['guestName'], row['email'], row['howMany'], row['diet'], ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=rsvp.csv"
    output.headers["Content-type"] = "text/csv"
    return output




# rsvp api end point
@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        guest_name = request.form['guestName']
        email = request.form['email']
        how_many = request.form['people']
        diet = request.form['diet'] or ""
        person_id = database.insert_person(
            guest_name=guest_name,
            email=email,
            how_many=how_many,
            diet=diet,
        )
        return redirect(url_for('thanks', person_id=person_id))


@app.route("/register/<person_id>", methods=['POST'])
def modify_person(person_id):
    if request.method == 'POST':
        guest_name = request.form['guestName']
        email = request.form['email']
        how_many = request.form['people']
        diet = request.form['diet'] or ""
        database.edit_person(
            person_id,
            guest_name=guest_name,
            email=email,
            how_many=how_many,
            diet=diet,
        )
        return redirect(url_for('thanks', person_id=person_id))


@app.route("/rsvp-delete/<person_id>", methods=['POST'])
@basic_auth.required
def delete_person(person_id):
    if request.method == 'POST':
        database.remove_person(person_id)
        return redirect(url_for('get_all_rsvp'))

if __name__ == "__main__":
    app.run()
