"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, PropertyForm
from app.models import UserProfile, PropertyProfile
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from os import getcwd, listdir
from os.path import join
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


def get_uploaded_images(rootdir,uploaddir):
    images = []
    try:
        images = listdir(join(rootdir,uploaddir))
    except Exception as e:
        print(e)
    else:
        print("complete")

    return images





@app.route('/properties/<propertyid>')
#@login_required
def get_images(propertyid):   
    return send_from_directory( join( getcwd(),app.config['UPLOAD_FOLDER']),propertyid )




@app.route('/property/<propertyid>')
#@login_required
def property(propertyid): 
    apt = PropertyProfile.query.filter_by(title=propertyid).first()  
    return render_template('property.html',data=apt) 
    

@app.route('/properties/create', methods=["GET","POST"])
#@login_required
def new_property():
    """Render a secure page on our website that only logged in users can access."""
    form = PropertyForm()
    if request.method == 'GET':
        return render_template('new_property.html',form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            # process form data
            title       = form.title.data
            bathrooms   = form.bathrooms.data
            rooms       = form.rooms.data
            location    = form.location.data
            price       = form.price.data
            housingtype = form.housingtype.data
            description = form.description.data
            photo       = form.photo.data
            filename    = secure_filename(photo.filename)
            photo.save( join( getcwd(),app.config['UPLOAD_FOLDER'] , filename))

            user = PropertyProfile.query.filter_by(title=title).first()
             


            if user is not None  :
                
                flash(f'Property already exists   {user.price}', 'danger')
                return render_template('new_property.html',form=form)

            else:
                # Insert to database
                newproperty = PropertyProfile(title,bathrooms,rooms,location,price,housingtype,description,filename)
                db.session.add(newproperty)
                db.session.commit()
                flash('Successfully added a new property', 'success')
                return redirect(url_for("properties")) 
            
        else:
            flash_errors(form)
            return render_template('new_property.html',form=form)




@app.route('/properties')
#@login_required
def properties():
    #if not session.get('logged_in'):
    #    abort(401)
    found = PropertyProfile.query.all()
    rootdir             = getcwd()
    uploaddir           = "app/uploads/photos"
    #found               = get_uploaded_images(rootdir,uploaddir)
    return render_template('properties.html',data=found) 




@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template("login.html", form=form)


    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate_on_submit():
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data

            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.
            user = UserProfile.query.filter_by(username=username).first()


            if user is not None and check_password_hash(user.password, password):
                remember_me = False

                # get user id, load into session
                login_user(user)

                # remember to flash a message to the user
                flash('Logged in successfully.', 'success')
                return redirect(url_for("home"))  # they should be redirected to a secure-page route instead

            else:
                flash('Username or Password is incorrect.', 'danger')
                return render_template("login.html", form=form)
            
        else :
            flash_errors(form)
            return render_template("login.html", form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully.', 'danger')
    return redirect(url_for("home"))




###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
