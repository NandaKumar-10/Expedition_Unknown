from flask import render_template,url_for,redirect,request,flash,session
from controllers.forms import *
from models.model import *
from datetime import datetime,timedelta

def init_routes(app):
    @app.route('/',methods=['GET','POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    session.clear()
                    session['name'] = user.name
                    session['userid'] = user.id
                    session['email'] = form.email.data
                    session['userType'] = 'user'
                    flash(f'Success! You are logged in as {user.name}','success')
                    return redirect(url_for('dashboard'))
                else:
                    flash(f"Password is wrong! Check the password again!", 'warning')
                    return redirect(url_for('login'))
        return render_template('login.html',form=form)
    
    @app.route('/dashboard')
    def dashboard():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        user = User.query.filter_by(email=session.get("email")).first()
        task_val1 = (user.task1_stage != 6) # type: ignore
        task_val2 = (user.task2_stage != 6) # type: ignore
        task_val3 = (user.task3_stage != 6) # type: ignore
        return render_template('dashboard.html',task_val1=task_val1,task_val2=task_val2,task_val3=task_val3)

    @app.route('/dashboard/task1', methods=['GET', 'POST'])
    def task1():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=session.get("email")).first()
        expiration_time_iso = None

        if not user:
            flash("User not found. Please log in again.", "danger")
            return redirect(url_for("login"))

        if user.task1_stage in [2, 4] and user.task1_hint_start:
            expiration_time = user.task1_hint_start + timedelta(seconds=90)
        
            if datetime.utcnow() >= expiration_time:
                if user.task1_stage == 2:
                    hint = "💡 Hint 1: Boosting"
                    user.task1_stage = 3
                else: # Stage 4
                    hint = "💡 Hint 2: Extreme"
                    user.task1_stage = 5
            
                flash(hint, 'info')
                db.session.commit()
                return redirect(url_for('task1'))
            else:
                expiration_time_iso = f"{expiration_time.isoformat()}Z"

        if request.method == "POST":
            if user.task1_stage in [2, 4]:
                flash("⏳ Please wait 1m30s before trying again.", "warning")
                return redirect(url_for('task1'))
            if user.task1_stage == 6:
                flash("🚫 Task closed. No more attempts allowed.", "danger")
                return redirect(url_for('task1'))

            user_input = request.form.get("userInput", "").strip()
            user.task1_attempts += 1

            if user_input.lower() == "xg boost" or user_input.lower()=="xgboost":
                flash("✅ Correct! Well done.", "success")
                user.task1_stage = 6
                db.session.commit()
                return redirect(url_for("dashboard"))
            
            else:
                if user.task1_stage == 1 and user.task1_attempts >= 5:
                    user.task1_stage = 2
                    user.task1_hint_start = datetime.utcnow()
                    flash("⏳ You used 5 attempts. Wait 1m30s for a hint.", "warning")
                elif user.task1_stage == 3 and user.task1_attempts >= 8:
                    user.task1_stage = 4
                    user.task1_hint_start = datetime.utcnow()
                    flash("⏳ Wrong again! Wait 1m30s for another hint.", "warning")
                elif user.task1_stage == 5 and user.task1_attempts >= 9:
                    user.task1_stage = 6
                    flash("🚫 Wrong! Task closed.", "danger")
                else:
                    flash("❌ Incorrect. Try again!", "warning")
            
            db.session.commit()
            return redirect(url_for('task1'))
        return render_template("task1.html", stage=user.task1_stage,expiration_time=expiration_time_iso)

    @app.route('/dashboard/task2',methods=['GET','POST'])
    def task2():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=session.get("email")).first()
        expiration_time_iso = None

        if not user:
            flash("User not found. Please log in again.", "danger")
            return redirect(url_for("login"))

        if user.task2_stage in [2, 4] and user.task2_hint_start:
            expiration_time = user.task2_hint_start + timedelta(seconds=90)
        
            if datetime.utcnow() >= expiration_time:
                if user.task2_stage == 2:
                    hint = "💡 Hint 1: Splits"
                    user.task2_stage = 3
                else:
                    hint = "💡 Hint 2: Ensemble"
                    user.task2_stage = 5
            
                flash(hint, 'info')
                db.session.commit()
                return redirect(url_for('task2'))
            else:
                expiration_time_iso = f"{expiration_time.isoformat()}Z"

        if request.method == "POST":
            if user.task2_stage in [2, 4]:
                flash("⏳ Please wait 1m30s before trying again.", "warning")
                return redirect(url_for('task2'))
            if user.task2_stage == 6:
                flash("🚫 Task closed. No more attempts allowed.", "danger")
                return redirect(url_for('task2'))

            user_input = request.form.get("userInput", "").strip()
            user.task2_attempts += 1

            if user_input.lower() == "random forest":
                flash("✅ Correct! Well done.", "success")
                user.task2_stage = 6
                db.session.commit()
                return redirect(url_for("dashboard"))
            
            else:
                if user.task2_stage == 1 and user.task2_attempts >= 5:
                    user.task2_stage = 2
                    user.task2_hint_start = datetime.utcnow()
                    flash("⏳ You used 5 attempts. Wait 1m30s for a hint.", "warning")
                elif user.task2_stage == 3 and user.task2_attempts >= 8:
                    user.task2_stage = 4
                    user.task2_hint_start = datetime.utcnow()
                    flash("⏳ Wrong again! Wait 1m30s for another hint.", "warning")
                elif user.task2_stage == 5 and user.task2_attempts >= 9:
                    user.task2_stage = 6
                    flash("🚫 Wrong! Task closed.", "danger")
                else:
                    flash("❌ Incorrect. Try again!", "warning")
            
            db.session.commit()
            return redirect(url_for('task2'))
        return render_template('task2.html', stage=user.task2_stage,expiration_time=expiration_time_iso)

    @app.route('/dashboard/task3',methods=['GET','POST'])
    def task3():
        email=session.get('email')
        if not email:
            flash("Session Expired! Login Again!",'warning')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=session.get("email")).first()
        expiration_time_iso = None
        if not user:
            flash("User not found. Please log in again.", "danger")
            return redirect(url_for("login"))

        if user.task3_stage in [2, 4] and user.task3_hint_start:
            expiration_time = user.task3_hint_start + timedelta(seconds=90)
        
            if datetime.utcnow() >= expiration_time:
                if user.task3_stage == 2:
                    hint = "💡 Hint 1: Density"
                    user.task3_stage = 3
                else:
                    hint = "💡 Hint 2: Mixture"
                    user.task3_stage = 5
            
                flash(hint, 'info')
                db.session.commit()
                return redirect(url_for('task3'))
            else:
                expiration_time_iso = f"{expiration_time.isoformat()}Z"

        if request.method == "POST":
            if user.task3_stage in [2, 4]:
                flash("⏳ Please wait 1m30s before trying again.", "warning")
                return redirect(url_for('task3'))
            if user.task3_stage == 6:
                flash("🚫 Task closed. No more attempts allowed.", "danger")
                return redirect(url_for('task3'))

            user_input = request.form.get("userInput", "").strip()
            user.task3_attempts += 1

            if user_input.lower() == "gaussian mixture model" or user_input.lower() == "gmm":
                flash("✅ Correct! Well done.", "success")
                user.task3_stage = 6
                db.session.commit()
                return redirect(url_for("dashboard"))
            
            else:
                if user.task3_stage == 1 and user.task3_attempts >= 5:
                    user.task3_stage = 2
                    user.task3_hint_start = datetime.utcnow()
                    flash("⏳ You used 5 attempts. Wait 1m30s for a hint.", "warning")
                elif user.task3_stage == 3 and user.task3_attempts >= 8:
                    user.task3_stage = 4
                    user.task3_hint_start = datetime.utcnow()
                    flash("⏳ Wrong again! Wait 1m30s for another hint.", "warning")
                elif user.task3_stage == 5 and user.task3_attempts >= 9:
                    user.task3_stage = 6
                    flash("🚫 Wrong! Task closed.", "danger")
                else:
                    flash("❌ Incorrect. Try again!", "warning")
            
            db.session.commit()
            return redirect(url_for('task3'))
        return render_template('task3.html', stage=user.task3_stage,expiration_time=expiration_time_iso) # pyright: ignore[reportOptionalMemberAccess]
    
    @app.route('/logout')
    def logout():
        session.pop('email',None)
        session.pop('name',None)
        session.pop('userType',None)
        session.clear()
        flash("You are logged out!!!",'info')
        return redirect(url_for('login'))