import email
from app import app, db
from flask import redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, ContactForm
from app.models import Admin, User

@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html',  title=title)

@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html',  title=title)


@app.route('/favorite')
def favorite():
    title = 'Favorite'

    #VIEWING FAVORITES IN PROFILE 
    favorite = current_user.favorites
    subtotal = 0
    for f in favorite:
        subtotal+=int(f.quantity)
    

    return render_template('userprofile.html', favorite=favorite, subtotal=subtotal, title=title)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    
    if form.validate_on_submit():
        
        email = form.email.data
        username = form.username.data
        password = form.password.data
        
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all() 
        if users_with_that_info:
            flash(f"There is already a user with that username and/or email. Please try again", "danger")
            return render_template('signup.html', title=title, form=form)

        
        new_user = User(email=email, username=username, password=password)
        
        flash(f"{new_user.username} has succesfully signed up.", "success")
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            
            login_user(user)
            
            flash(f'{user} has successfully logged in', 'success')
            
            return redirect(url_for('index'))
        else:
            flash('Username and/or password is incorrect', 'danger')
            
    return render_template('login.html', title=title, form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))

##ADD TO FAVORITES 
@app.route("/add_to_favorites/<shop_owner_id>")
@login_required
def addToFavorites(shop_owner_id):
    title= 'Add to Favorites'

    item_to_add = Favorite(shop_owner_id=shop_owner_id, user_id=current_user.id)
    db.session.add(item_to_add)
    db.session.commit()
    
    repeat_favorite = Favorite.query.filter_by(shop_owner_id=shop_owner_id, favoritor=current_user).first()
    if repeat_favorite:
        
        flash('This shop owner has already been favorited!')
        

    return render_template('index.html', title=title)

##REMOVE FROM FAVORITES
@app.route("/removeFromfavorite/<shop_owner_id>")
@login_required
def removeFromFavorite(shop_owner_id):

    favorite_to_remove = favorite.query.filter_by(shop_owner_id=shop_owner_id, favoritor=current_user).first()
    db.session.delete(favorite_to_remove)
    db.session.commit()

    flash('Shop owner has been removed from your favorites!', 'success')
    return redirect(url_for('index.html'))


@app.route("/shop_owner_profile")
def shop_owner_profile(shop_owner_id):
    title = 'Shop Owner'
    shop_owner = Admin.query.get_or_404(shop_owner_id)

    return render_template('shop_owner_profile.html', shop_ownert=shop_owner, title=title)



@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    title = 'Contact me'
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data   
        subject = form.subject.data 
        message = form.message.data

        new_message = User(name=name, email=email, subject=subject, message=message)
        
        flash(f"Thank you for you {new_message.name}, I will return your message shortly", "success")
        return redirect(url_for('index'))

    return render_template('contact.html', title=title, form=form)
