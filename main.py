#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (jsonify,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   )

import re
from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug import secure_filename
from threading import Thread
#import threading
#import ast
#import time
#import subprocess




app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ENCODING'] = 'utf8'
app.config['SQLALCHEMY_CONVERT_UNICODE'] = 'TRUE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from models import User, LoginForm, RegisterForm, db, MainPrice, Competitor, SearchQuery, Result
from pars_in_db import loadAndUpdate

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#    import logging
#    logging.basicConfig()
#    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)	



EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

	
@app.route('/')
def main():

    return render_template('main.html', title="Main page")


						   
@app.route('/signin.htm', methods=['GET', 'POST'])
def signin():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=True)
                return redirect(url_for('wallet'))

        return render_template('loginfail.html')
    return render_template('signin.htm',
						   form=form
                           )						   

						   
@app.route('/signup.html', methods=['GET'])
def signup_get():
    ref = request.args.get('ref')
    form = RegisterForm()
    valid_error = False
    return render_template('signup.html', form=form, valid_error=valid_error, ref = ref)
						   
						   
						   
@app.route('/signup.html', methods=['POST'])
def signup_post():
    form = RegisterForm()
    valid_error = False
    if form.validate_on_submit():
        new_user = User(username = form.username.data, 
						email = form.email.data, 
						password = form.password.data, 
						firstname = form.firstname.data,
						secondname = form.secondname.data,
						groups = 'users',
						id_ref = form.ref.data,
						rub = '0',
						usd = '0'
						)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            valid_error = False		
            return render_template('signup.html', form=form, valid_error=valid_error)	
        return redirect(url_for('wallet'))	
    else:
        valid_error = True		
        return render_template('signup.html', form=form, valid_error=valid_error)
   

 

@app.route('/add.html')
@login_required
def add():
    return render_template('add.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/history.html')
@login_required
def history():
    payment_history = Payment_History.query.filter_by(to_user_id=current_user.id).all()
    return render_template('history.html', menu_active=5, payment_history = payment_history)

@app.route('/invest.html')
@login_required
def invest():
    return render_template('invest.html', menu_active=2)

@app.route('/myinvest.html')
@login_required
def myinvest():
    return render_template('myinvest.html', menu_active=3)

@app.route('/partners.html')
@login_required
def partners():
    return render_template('partners.html', menu_active=6)

@app.route('/send.html')
@login_required
def send():
    return render_template('send.html', menu_active=7)

@app.route('/settings.html')
@login_required
def settings():
    return render_template('settings.html', menu_active=8)

@app.route('/stat.html')
@login_required
def stat():
    return render_template('stat.html')

	
	
	
	
@app.route('/support.html')
@login_required
def support():
    tickets = Support.query.filter_by(id_user=current_user.id).all()
#    for ticket in tickets:
#        chat = Chat.query.filter_by(id_support=ticket.id).all()

#        if chat is not None:
#            for message in chat:
#                print(message.id_user)
#                if (ticket.status != 3) and (message.id_user == 1):
 #                   print("Admin in tred")
 #                   print("Admin in tred")
 #                   print("Admin in tred")
    return render_template('support.html', menu_active=9, tickets=tickets)
	

	
	


@app.route('/userfiat.html')
@login_required
def userfiat():
    return render_template('userfiat.html', menu_active=4)

	
	
@app.route('/wallet.html')
@login_required
def wallet():
    if current_user.groups == 'users':
        if current_user.id_ref == 0:
            ref = "/"
        else:
    	    ref = "{}signup.html?ref={}".format(request.host_url, current_user.id_ref)
    else:
        ref = "{}signup.html?ref={}".format(request.host_url, current_user.id)		
    return render_template('wallet.html', name=current_user.username, menu_active=1, ref = ref)	
	
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.htm')
	
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('main.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return signin()



@app.route('/ajax/settings/', methods=['POST'])
@login_required
def ajax_settings():
    request_type=0
    user_email=0
    user_password=0
    user_new_password=0
	
    request_type = request.form['type']
    user_password = request.form['password']
    if request.form['type'] == 'change_email':
        user_email = request.form['email']
        user = User.query.filter_by(email=current_user.email).first() 
        if user_password == user.password:
            if not EMAIL_REGEX.match(user_email):
                return jsonify({'s': 0, 'd' : "Почта ошибка"})
            user.email = user_email
            db.session.commit()
            return jsonify({'s': 1, 'd' : "Новая почта {} внесена.".format(user_email)})	
        return jsonify({'s':0, 'd' : "Ошибка данных"})	
    else:		
        if request.form['type'] == 'change_password':
            user_new_password = request.form['new_password']
            user = User.query.filter_by(email=current_user.email).first()   
            if user_password == user.password:
                if len(user_new_password) < 4:
                    return jsonify({'s': 0, 'd' : "Пароль должен быть больше 4 символов"})
                user.password = user_new_password
                db.session.commit()			
                return jsonify({'s': 1, 'd' : "Новый пароль внесён"})	
            return jsonify({'s':0, 'd' : "Ошибка данных"})	
    success = 0
    text = "0"
    return jsonify({'s':success, 'd' : text})	



	
@app.route('/ajax/support/', methods=['POST'])
@login_required
def ajax_support():
    type = request.form['type']		# 'new'
    if type == 'new':
        type_ticket = request.form['type_ticket']		
        topic = request.form['topic']		
        message = request.form['message']		
        if len(message) < 25:
            return jsonify({'s':0, 'd' : "Сообщение короткое. Минимум 25 символов."})	        
        if len(topic) < 5:
            return jsonify({'s':0, 'd' : "Тема короткая. Минимум 5 символов."})
        if int(type_ticket) < 1 or int(type_ticket) > 5:
            return jsonify({'s':0, 'd' : "Неверный тип проблемы."})
    
        support = Support(	id_user=current_user.id, 
							type_ticket = type_ticket,
							topic = topic,
							status = 1,
							date_time = datetime.now()
							)
        db.session.add(support)
        db.session.commit()

        support = Support.query.filter_by(id_user=current_user.id).order_by(Support.id.desc()).first()
	
        chat = Chat(id_support=support.id,
					id_user = current_user.id,
					message = message,
					date_time = support.date_time
					)
        db.session.add(chat)
        db.session.commit()		
	
        return jsonify({'s':1, 'd' : ' '})	
    if type == 'new_message_ticket':	
        id = request.form['id']		
        message = request.form['message']	       	
        if len(message) < 25:
            return jsonify({'s':0, 'd' : "Сообщение короткое. Минимум 25 символов."})	

        chat = Chat(id_support=id,
					id_user = current_user.id,
					message = message,
					date_time = datetime.now()
					)
        db.session.add(chat)
        db.session.commit()	
        return jsonify({'s':1, 'd' : ' '})	

    if type == 'close':	
        id = request.form['id']		       	
        support = Support.query.filter_by(id=id).first() 
        support.status = 3
        db.session.commit()	
        return jsonify({'s':1, 'd' : ' '})	
    return jsonify({'s':0, 'd' : ' '})	



@app.route('/ajax/admin/', methods=['POST'])
@login_required
def ajax_admin():
    if current_user.groups == 'admins':
        type = request.form['type']		# 'new'
        if type == 'new':
            type_ticket = request.form['type_ticket']		
            topic = request.form['topic']		
            message = request.form['message']		
            if len(message) < 25:
                return jsonify({'s':0, 'd' : "Сообщение короткое. Минимум 25 символов."})	        
            if len(topic) < 5:
                return jsonify({'s':0, 'd' : "Тема короткая. Минимум 5 символов."})
            if int(type_ticket) < 1 or int(type_ticket) > 5:
                return jsonify({'s':0, 'd' : "Неверный тип проблемы."})
    
            support = Support(	id_user=current_user.id, 
	    						type_ticket = type_ticket,
	    						topic = topic,
	    						status = 1,
	    						date_time = datetime.now()
	    						)
            db.session.add(support)
            db.session.commit()

            support = Support.query.filter_by(id_user=current_user.id).order_by(Support.id.desc()).first()
	
            chat = Chat(id_support=support.id,
	    				id_user = current_user.id,
	    				message = message,
	    				date_time = support.date_time
	    				)
            db.session.add(chat)
            db.session.commit()		
	
            return jsonify({'s':1, 'd' : ' '})	
        if type == 'new_message_ticket':	
            id = request.form['id']		
            message = request.form['message']	       	
            if len(message) < 25:
                return jsonify({'s':0, 'd' : "Сообщение короткое. Минимум 25 символов."})	

            chat = Chat(id_support=id,
    					id_user = current_user.id,
    					message = message,
    					date_time = datetime.now()
    					)
            db.session.add(chat)
            db.session.commit()
			
            support = Support.query.filter_by(id=id).first()
            support.status = 2
            db.session.commit()	
			
            return jsonify({'s':1, 'd' : ' '})	

        if type == 'close':	
            id = request.form['id']		       	
            support = Support.query.filter_by(id=id).first() 
            support.status = 3
            db.session.commit()	
            return jsonify({'s':1, 'd' : ' '})	
        return jsonify({'s':0, 'd' : ' '})	
    else:
        return jsonify({'s':0, 'd' : "Вы не администратор."})    

	
@app.route('/support/<id>/')
@login_required
def answer(id):
    ticket = Support.query.filter_by(id=id).first()     
    if ticket.id_user == current_user.id:
		
        chat = (db.session.query(Chat,User)		
			.filter(Chat.id_support==ticket.id)
			.filter( User.id == Chat.id_user)
			.order_by(Chat.date_time.desc())
			.all())

        return render_template('answer.html', menu_active=9, ticket=ticket, chat=chat)
    else:
        return redirect(url_for('support'))	



@app.route('/admin/<id>/')
@login_required
def administration(id):
    ticket = Support.query.filter_by(id=id).first()     
#    if current_user.id == 1:
    if current_user.groups == 'admins':
        chat = (db.session.query(Chat,User)		
			.filter(Chat.id_support==id)
			.filter( User.id == Chat.id_user)
			.order_by(Chat.date_time.desc())
			.all())
 
        return render_template('answer.html', menu_active=9, ticket=ticket, chat=chat)
    else:
        return redirect(url_for('support'))		


@app.route('/userinfo/<id>/')
@login_required
def userinfo(id):
    if id == '1':
        return redirect(url_for('support'))	
    if current_user.groups == 'admins':
        payment_history = Payment_History.query.filter_by(to_user_id=id).all()
        user = User.query.filter_by(id=id).first() 
        tickets = Support.query.filter_by(id_user=id).all()
        refers = User.query.filter_by(groups="admins").all()		
        return render_template('userinfo.html', tickets=tickets, user=user, refers=refers, menu_active=10, 
								payment_history = payment_history)
    else:
        return redirect(url_for('support'))		

		
		
@app.route('/ajax/userinfo/', methods=['POST'])
@login_required
def ajax_userinfo():
    if current_user.groups == 'admins':
        type = request.form['type']		# 'new'
        if type == 'change_username':
            id = request.form['id']		
            username = request.form['username']		
            user = User.query.filter_by(id=id).first()
            check_username = User.query.filter_by(username=username).first()
            if check_username is None:
                user.username = username
                db.session.commit()
                return jsonify({'s':1, 'd' : "Логин изменён."})	
            else:
                return jsonify({'s':0, 'd' : "Такой логин уже существует."})			
        if type == 'change_firstname':
            id = request.form['id']		
            firstname = request.form['firstname']		
            user = User.query.filter_by(id=id).first()
            user.firstname = firstname
            db.session.commit()
            return jsonify({'s':1, 'd' : "Имя изменено."})	
        if type == 'change_secondname':
            id = request.form['id']		
            secondname = request.form['secondname']		
            user = User.query.filter_by(id=id).first()
            user.secondname = secondname
            db.session.commit()
            return jsonify({'s':1, 'd' : "Фамилия изменена."})
        if type == 'change_email':
            id = request.form['id']		
            email = request.form['email']		
            user = User.query.filter_by(id=id).first()
            check_email = User.query.filter_by(email=email).first()
            if check_email is None:
                user.email = email
                db.session.commit()
                return jsonify({'s':1, 'd' : "Почта изменена."})	
            else:
                return jsonify({'s':0, 'd' : "Такая почта уже существует."})				
        if type == 'change_password':
            id = request.form['id']		
            password = request.form['password']		
            user = User.query.filter_by(id=id).first()
            user.password = password
            db.session.commit()
            return jsonify({'s':1, 'd' : "Пароль изменён."})	
        if type == 'change_groups':
            id = request.form['id']
            if id == '1':
                return jsonify({'s':0, 'd' : "Ты чё, хакер дохуя?"})
            else:
                user = User.query.filter_by(id=id).first()
                if user.groups == 'users':
                    group = 'admins'
                else:
                    group = 'users'
                user.groups = group
                db.session.commit()
                return jsonify({'s':1, 'd' : "Права изменены.", 't' : group})	
        if type == 'addRUB':
            from_user = request.form['from_user']		
            to_user = request.form['to_user']		
            rub_sum = request.form['rub_sum']		
            message = request.form['message']		
			
            to_user = User.query.filter_by(username=to_user).first()
            from_user = User.query.filter_by(username=from_user).first()
			
            if (to_user is None) or (from_user is None):
                return jsonify({'s':1, 'd' : "Такого пользователя не существует."})	
			
            to_user.rub = int(to_user.rub) + int(rub_sum)
            db.session.commit()

            add_payment_history = Payment_History(from_user_id=from_user.id,
													to_user_id = to_user.id,
													message = message,
													rub = rub_sum,
													usd = '0',
													date_time = datetime.now()
												)			
            db.session.add(add_payment_history)
            db.session.commit()			
            return jsonify({'s':1, 'd' : "Деньги занесены."})	        

        if type == 'addUSD':
            from_user = request.form['from_user']		
            to_user = request.form['to_user']		
            usd_sum = request.form['usd_sum']		
            message = request.form['message']		
			
            to_user = User.query.filter_by(username=to_user).first()
            from_user = User.query.filter_by(username=from_user).first()
			
            if (to_user is None) or (from_user is None):
                return jsonify({'s':1, 'd' : "Такого пользователя не существует."})	
			
            to_user.usd = int(to_user.usd) + int(usd_sum)
            db.session.commit()

            add_payment_history = Payment_History(from_user_id=from_user.id,
													to_user_id = to_user.id,
													message = message,
													rub = '0',
													usd = usd_sum,
													date_time = datetime.now()
												)			
            db.session.add(add_payment_history)
            db.session.commit()			
            return jsonify({'s':1, 'd' : "Деньги занесены."})
			
        if type == 'change_idref':
            id = request.form['id']		
            idref = request.form['idref']		
            user = User.query.filter_by(id=id).first()
            user.id_ref = idref
            db.session.commit()
            return jsonify({'s':1, 'd' : "ID рефера изменён."})				

			
			
        return jsonify({'s':0, 'd' : 'как ты сюда попал?'})	
    else:
        return jsonify({'s':0, 'd' : "Вы не администратор."})  
		
		
@app.route('/admin.html')
@login_required
def admin():
    if current_user.groups == 'admins':

        if current_user.id != 1:
            tickets = (db.session.query(Support,User)		
    			.filter(Support.status!=3)
    			.filter(User.id == Support.id_user)
    			.filter(User.id_ref == current_user.id)
    			.all())
        else:
            tickets = (db.session.query(Support,User)		
    			.filter(Support.status!=3)
	    		.filter(User.id == Support.id_user)
    			.all())	
		
	
        return render_template('admin.html', menu_active=9, tickets=tickets)
    else:
        return redirect(url_for('support'))	
		


@app.route('/adminpanel.html')
@login_required
def adminpanel():
    if current_user.groups == 'admins':

        users_list = (db.session.query(User)
						.filter(User.groups=='users')
						.all())	

	
        return render_template('adminpanel.html', menu_active=10, users_list=users_list)
    else:
        return redirect(url_for('support'))	


		
from flask import json
from sqlalchemy import and_, any_, or_

@app.route('/api/1.0/get_main_table')
def get_main_table():
    query = request.args.get('query').split()
    
    query = [q.replace('_', ' ') for q in query]
    data = MainPrice.query.filter(and_(*[MainPrice.name.ilike('%'+name+'%') for name in query]))
    items = []
    for dat in data:
        items.append({"id": dat.id, "name": dat.name, "price": dat.low_price})

    return jsonify(items)		
		
	
@app.route('/api/1.0/get_comp_table')
def get_comp_table():
    query = request.args.get('query').split()
    query = [q.replace('_', ' ') for q in query]
    data = Competitor.query.filter(and_(*[Competitor.name.ilike('%'+name+'%') for name in query]))
    items = []
    for dat in data:
        items.append({"id": dat.id, "comp_name": dat.comp_name, "name": dat.name, "price": dat.low_price})

    return jsonify(items)		
	
@app.route('/api/1.0/get_comp_table_all')
def get_comp_table_all():
    query = request.args.get('query').split()
    query = [q.replace('_', ' ') for q in query]
    second = request.args.get('second').split()
    second = [q.replace('_', ' ') for q in second]
    data = Competitor.query.filter(and_(*[Competitor.name.ilike('%'+name+'%') for name in query], or_(*[Competitor.name.ilike('%'+word+'%') for word in second]))).order_by(Competitor.low_price)
    all = {}
    for dat in data:
        if dat.comp_name not in all:
            all[dat.comp_name] = [{"id": dat.id, "name": dat.name, "price": dat.low_price, "diff" : ''}]
        else:
            all[dat.comp_name].append({"id": dat.id, "name": dat.name, "price": dat.low_price, "diff" : ''})
    return jsonify(all)		



# C R U D

@app.route('/api/1.0/create_searchquery', methods=['POST'])
def create_searchquery():
    searchquery = request.args.get('query')
	
    new_search_query = SearchQuery(query = searchquery)
    try:
        db.session.add(new_search_query)
        db.session.commit()
    except:
        db.session.rollback()	
    return ''


@app.route('/api/1.0/read_searchquery')
def read_searchquery():
    all = []
    searchquery_list = db.session.query(SearchQuery).all()	
    for el in searchquery_list:
        all.append({'query' : el.query})
    return jsonify(all)
	
@app.route('/api/1.0/delete_searchquery')
def delete_searchquery():
		
    return ''	

	
@app.route('/api/1.0/create_result', methods=['POST'])
def create_result():
    selected = request.args.get('selected')
    main = request.args.get('mainrecord')
    comp = request.args.get('comprecord')
    new_record = Result(selected_record=selected, main_records=main, competitor_records=comp)
    try:
        db.session.add(new_record)
        db.session.commit()
    except:
        db.session.rollback()
    return ''


"""	
    new_search_query = SearchQuery(query = searchquery)
    try:
        db.session.add(new_search_query)
        db.session.commit()
    except:
        db.session.rollback()	
"""
    
	

from sqlalchemy import union_all

@app.route('/api/1.0/read_result')
def read_result():
    all = []

    data = db.session.query(Result).all()	
    for dat in data:
        if dat.selected_record is not '':
            result = {}
            selected_price = MainPrice.query.filter_by(id=int(dat.selected_record)).first()
            result['selected'] = [{"sel_id": selected_price.id, "sel_price" : selected_price.low_price}]
            result['res_id'] = [dat.id]
			
			

			
            comp_records_list = dat.competitor_records
            comp_records_list = list(map(int, comp_records_list.split(',')))
            record_a = db.session.query(Competitor).filter(Competitor.id.in_(comp_records_list)).order_by(Competitor.low_price).all()
 
            for rec in record_a:
                if rec.comp_name not in result:
                    result[rec.comp_name] = [{"id": rec.id, "name": rec.name, "price": rec.low_price, "diff" : ''}]
                else:
                    result[rec.comp_name].append({"id": rec.id, "name": rec.name, "price": rec.low_price, "diff" : ''})

            main_records_list = dat.main_records
            main_records_list = list(map(int, main_records_list.split(',')))
			
            record_b = db.session.query(MainPrice).filter(MainPrice.id.in_(main_records_list)).order_by(MainPrice.low_price).all()
            

			
            for rec in record_b:
                if '1main_price' not in result:
                    result['1main_price'] = [{"id": rec.id, "name": rec.name, "price": rec.low_price}]
                else:
                    result['1main_price'].append({"id": rec.id, "name": rec.name, "price": rec.low_price})				
            all.append(result)
    	
	
    return jsonify(all)
	
	
	
	
@app.route('/api/1.0/delete_result')
def delete_result():
    id = request.args.get('id')		
    try:
        user = Result.query.get(id)
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.rollback()	
    return ''	
	
@app.route('/result.html')
def result():
    return render_template('result.html', title="Result page")	
	
	
		


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
			
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
			
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = app.config['UPLOAD_FOLDER'] 
            file.save(os.path.join(path, filename))
			
            thread1 = Thread(target=loadAndUpdate, args=(path, filename,))
            thread1.start()			

            return 'Файл загружен и обрабатывается'
    return ''

@app.route('/api/1.0/get_price_names')
def get_price_names():



    records = []
    if db.session.query(MainPrice).first() is not None:
        records.append('AppleHelp.ru')

    recs = db.session.query(Competitor).group_by(Competitor.comp_name).all()

    for rec in recs:
        records.append(rec.comp_name)


    return jsonify(records)


@app.route('/api/1.0/del_price_by_name')
def del_price_names():
    comp_name = request.args.get('comp_name')

    if comp_name == 'AppleHelp.ru':
        num_rows_deleted = db.session.query(MainPrice).delete()
        db.session.commit()
    else:
        delete_q = Competitor.__table__.delete().where(Competitor.comp_name == comp_name)
        db.session.execute(delete_q)
        db.session.commit()
    return ''	
	