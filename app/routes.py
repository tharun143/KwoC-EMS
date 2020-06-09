from flask import render_template, flash, redirect, url_for,  request
from app import app, db
from app.get_returns import tax
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddTransactionForm, AddCommentForm, EditTransactionForm, UpdateStatusForm
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User, Transaction, Comment, Document
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime


@app.route('/index')
@login_required
def index():
    if current_user.job != 'Acc':
        transaction = Transaction.query.filter_by(user_id=current_user.id)  
        return render_template("index.html", title='HomePage',transaction=transaction)
    else:
        return redirect(url_for('acc_index'))    

@app.route('/acc_index')
@login_required
def acc_index():
    #should link 
    link = 11
    transaction = Transaction.query.filter_by(user_id=link)
    document = Document.query.all()  
    return render_template("acc_index.html", title='HomePage',transaction=transaction,document=document)            

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.job == 'Acc':
            return redirect(url_for('acc_index'))
        else:    
            return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        r = form.remember_me.data
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            if user.job == 'Acc':
                return redirect(url_for('acc_index'))
            else:    
                return redirect(url_for('index',r=r))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.job == 'Acc':
                next_page = url_for('acc_index')
            else:
                next_page = url_for('index',r=r)    
        return redirect(next_page) 
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        if current_user.job == 'Acc':
            return redirect(url_for('acc_index'))
        else:    
            return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,job=form.job.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{'author': user, 'body': 'Test post #1'},{'author': user,'body': 'Test post #2'}]
    return render_template('user.html',user=user,posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/get_returns')
@login_required
def get_returns():
    transactions = Transaction.query.filter_by(user_id=current_user.id,valid=True)
    cr_tr = Transaction.query.filter_by(user_id=current_user.id,valid=True,tr_type='credited')
    inc_tax, income = tax(cr_tr)
    return render_template('returns.html',title='Returns',transaction=transactions,tax=inc_tax,income=income)

@app.route('/add_transaction',methods=['GET','POST'])
@login_required
def add_transaction():
    form = AddTransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(tr_id=form.tr_id.data, date=form.date.data, description=form.description.data, tr_type=form.tr_type.data, amount=form.amount.data)
        transaction.user_id = current_user.id
        filename = secure_filename(form.file.data.filename)
        db.session.add(transaction)
        db.session.commit()   
        if filename != '':
            form.file.data.save('uploads/'+filename)
            document = Document(filename=filename,transaction_id=transaction.id)
            db.session.add(document)
            db.session.commit()
        flash('You have sucessfully added the transaction!')
        return redirect(url_for('index'))
    return render_template('transaction.html',title='New Transaction',form=form)    

@app.route('/edit_transaction/<trans_id>',methods=['GET','POST'])
@login_required
def edit_transaction(trans_id):
    form = EditTransactionForm()
    transaction = Transaction.query.filter_by(id=trans_id).first_or_404()
    if form.validate_on_submit():
        transaction.tr_id = form.tr_id.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        transaction.tr_type = form.tr_type.data
        transaction.amount = form.amount.data
        filename = secure_filename(form.file.data.filename)
        db.session.commit()
        if filename != '':
            form.file.data.save('uploads/'+filename)
            document = Document(filename=filename,transaction_id=transaction.id)
            db.session.add(document)
            db.session.commit()
        flash('You have sucessfully edited the transaction!')    
        return redirect(url_for('edit_transaction',trans_id=transaction.id))
    elif request.method == 'GET':
        form.tr_id.data = transaction.tr_id
        form.date.data = transaction.date
        form.description.data = transaction.description
        form.tr_type.data = transaction.tr_type
        form.amount.data = transaction.amount   
    return render_template('edit_transaction.html',title='Edit Transaction',form=form)   

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.company = form.company.data
        current_user.designation = form.designation.data 
        current_user.facebook = form.facebook.data
        current_user.twitter = form.twitter.data
        current_user.linkedin = form.linkedin.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.company.data = current_user.company
        form.designation.data = current_user.designation
        form.facebook.data = current_user.facebook
        form.linkedin.data = current_user.linkedin
        form.twitter.data = current_user.twitter
    return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/add_comment/<trans_id>',methods=['GET','POST'])    
@login_required
def add_comment(trans_id):
    form = AddCommentForm()
    comm = Comment.query.filter_by(trans_id=trans_id)
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data)
        comment.trans_id = trans_id
        comment.user_id = current_user.id
        db.session.add(comment)
        db.session.commit()
        flash('You have commented this transaction!')
        return redirect(url_for('add_comment', trans_id = trans_id))
    return render_template('add_comment.html',title='New Comment',form=form,comm=comm)     

@app.route('/update_status/<trans_id>',methods=['GET','POST'])
@login_required
def update_status(trans_id):
    form = UpdateStatusForm()
    transaction = Transaction.query.filter_by(id=trans_id).first_or_404()
    if form.validate_on_submit():
        if form.status.data == 'True':
            transaction.valid = bool(form.status.data)
        else:
            x = None
            transaction.valid = bool(x)
        db.session.commit()
        flash('You have successfully updated the status of the transaction!')
        return redirect(url_for('update_status', trans_id=trans_id))
    return render_template('status.html',title='Update Status',form=form,tr=transaction)        


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/')
@app.route('/explore')
def explore():
    return render_template("explore.html")

@app.route('/jquery_min')
def jquery_min():
    return render_template('jquery.min.js')

@app.route('/browser_min')
def browser_min():
    return render_template('browser.min.js')

@app.route('/breakpoints_min')
def breakpoints_min():
    return render_template('breakpoints.min.js')

@app.route('/util')
def util():
    return render_template('util.js')

@app.route('/main')
def main():
    return render_template('main.js')

@app.route('/myscirpt')
def myscript():
    return render_template('myscript.js')

@app.route('/myscript2')
def myscript2():
    return render_template('myscript2.js')

@app.route('/brd')
def brd():
    return render_template('brd.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return redirect('https://www.termsandconditionsgenerator.com/live.php?token=ajGs0Y1cg4yVzPMm5tNPj5t8KCaHS7Oi')

@app.route('/policy')
def policy():
    return redirect('https://www.privacypolicygenerator.info/live.php?token=EDXwCfzKcR5D6LCyEyrCCtDzT6ySApKT')

@app.route('/disclaimer')
def disclaimer():
    return redirect('https://www.disclaimergenerator.net/live.php?token=KGTl18cFWm6Sze9ZKolR8n4HRIxv4lLs')