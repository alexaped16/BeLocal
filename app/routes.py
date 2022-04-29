
from contextlib import redirect_stderr
from app import app, db
from flask import redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, ContactForm
from app.models import Shop, User

@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html',  title=title)

@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html',  title=title)



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
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))





# ADD AND DELETE FAVORITES

@app.route('/my_favorites')
@login_required
def my_favorites():
    title = 'My Favorites'
    favorites = current_user.favorites

    #VIEWING FAVORITES IN PROFILE 

    return render_template('my_favorites.html', title=title, favorites=favorites)


@app.route('/add-to-favorites/<shop_id>')
@login_required
def addToFavorites(shop_id):

    shop_to_add = Shop.query.get_or_404(shop_id)
    current_user.add_favorite(shop_to_add)
        

    return redirect(url_for('my_favorites'))


##REMOVE FROM FAVORITES
@app.route('/remove-from-favorites/<shop_id>')
@login_required
def removeFromFavorites(shop_id):

    shop_to_remove = Shop.query.get_or_404(shop_id)
    current_user.remove_favorite(shop_to_remove)




    flash(f'{shop_to_remove.shop_title} has been removed from your favorites.', 'success')
    return redirect(url_for('my_favorites'))


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    title = 'Contact me'
    if form.validate_on_submit():
        email = form.email.data   
        message = form.message.data

        new_message = User(email=email, message=message)
        
        flash(f"Thank you for your message, {new_message.name}. I will get back to you soon!", "success")
        return redirect(url_for('index'))

    return render_template('contact.html', title=title, form=form)









# SHOP PROFILES 

@app.route('/goth_angel')
def goth_angel():
    title = 'Goth Angel'
    return render_template('/shop-profile/goth_angel.html',  title=title)

@app.route('/the_letter_head')
def the_letter_head():
    title = 'The Letter Head'
    return render_template('/shop-profile/the_letter_head.html',  title=title)

@app.route('/loops_by_linds')
def loops_by_linds():
    title = 'Loops by Linds'
    return render_template('/shop-profile/loops_by_linds.html',  title=title)

@app.route('/mela_project')
def mela_projects():
    return render_template('/shop-profile/mela_projects.html')

@app.route('/jukias_closet')
def jukias_closet():
    return render_template('/shop-profile/jukias_closet.html')



@app.route('/get_shop/<shop>')
def get_shop(shop):
    # url == f"url_for {{ Shop.url_for }}" 
        
    return redirect(url_for(f'{shop}'))
    # return render_template('/shop-profile/jukias_closet.html')

@app.route('/my_favorites')
def get_favorites():
    # url == f"url_for {{ Shop.url_for }}" 
        
    return redirect(url_for('my_favorites'))

