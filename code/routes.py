from form import *

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@login_manager.user_loader
def load_user(user_id):
    return usr.query.get(int(user_id))

@login_required
@app.route("/to_link",methods=['GET', 'POST'])
def meet():
    try:
        link_via_hostcode(current_user.host_code)
        return redirect(link_via_hostcode(current_user.host_code))
    except:
        return ('',204)

@app.route("/meet_link_update",methods=['GET', 'POST'])
def upd_link():
    n_link=request.form['nw_link']
    try:
        if current_user.post=='EB':
                update_link(current_user.host_code,n_link)
                flash("Link Updated Successfully !!!",'success')
    except:
        flash("Unknown Error!!!",'success')
    return redirect(url_for('home1'))

@login_required
@app.route("/reply_click",methods=['GET', 'POST'])
def reply_click():
    if current_user.is_authenticated:
        chits = swit(current_user.host_code)
        eb=False
        if current_user.post=="EB":
            eb=True
        if current_user.post!='EB' and chits==False:
            return('',204)
        else:
            r_id= request.form["reply"]
            to_cont=reply_to(current_user.host_code,r_id)
            return render_template('reply.html',s_box=True,point_list=point_list,reply_to=reply_msg_via_id(r_id),r_id=r_id,to_country=to_cont,eb=eb,h_c=False,COD=True,ss_head=current_user.post,s_head=organization_via_hostcode(current_user.host_code))
    else:
        return redirect(url_for('login'))

@login_required
@app.route("/home1",methods=['GET', 'POST'])
def home1():
    if current_user.is_authenticated:
        eb=eb_fnt(current_user.post)
        com=False
        h_c=False
        chits = swit(current_user.host_code)
        country_list=sorted(country_li(current_user.host_code))
        country_list.remove(current_user.post)
        class mun(FlaskForm):
            convo_with = SelectField('Options',choices=country_list,validators=[DataRequired()])
            chit_point = SelectField('Query',choices=point_list,validators=[DataRequired()])
            viaeb = BooleanField('Via EB')
            message=TextAreaField(u'Message',validators=[DataRequired()])
            submit = SubmitField(' Send Message ')
            def validate_message(self, message):
                if len(message.data)>10000:
                    raise ValidationError('Number of character limit exceed which is 10000...'+'\nYou entered '+str(len(message.data))+' characters')
        form1=mun()
        if form1.validate_on_submit():
            if form1.viaeb.data == True and form1.convo_with.data not in eb_d:
                via_eb='Yes'
            else:
                via_eb = "No"
            if chits==True or eb_fnt(current_user.post)==True:
                message_adder_dab(current_user.host_code,form1.convo_with.data,current_user.post,via_eb,form1.message.data,'None',chit_pnt=form1.chit_point.data)
                flash("Message Sent Successfully !!!",'success')
            else:
                flash("Chits are blocked by EB !!!",'danger')
            return redirect(url_for('home1'))
        return render_template('home1.html',eb=eb,s_box=True,h_c=False,COD=True,form1=mun(),ss_head=current_user.post,s_head=organization_via_hostcode(current_user.host_code))
    else:
        return redirect(url_for('login'))

@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html',posts=posts,postup=postup,s_box=True,s_head="CHITS")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home1'))
    form = join_c()
    if form.validate_on_submit():
        if form.host_code.data in host_c_list:
            user= usr.query.filter_by(host_code=form.host_code.data,user_id=form.d_pass.data).first()
            if user and user.host_code==form.host_code.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home1'))
            else:
                return redirect(url_for('login'))
        else:
            flash("Invalid Host Code !!!",'danger')
    return render_template('login.html',posts=posts,form=form)





@app.route("/refresh_msg", methods=['GET', 'POST'])
def  refresh_msg():
    return redirect(url_for('messages'))


@login_required
@app.route("/swi", methods=['GET', 'POST'])
def switch_control():
    if eb_fnt(current_user.post)==True:
        change_switch(current_user.host_code)
        return redirect(url_for('messages'))
    else:
        return ('',204)

@login_required
@app.route("/auto_r_switch", methods=['GET', 'POST'])
def auto_refresh_change():
    change_switch_auto_r(current_user.user_id)
    return redirect(url_for('messages'))

@login_required
@app.route("/confi", methods=['GET', 'POST'])
def messages():
    if current_user.is_authenticated:
        confi_srt= False
        chits = swit(current_user.host_code)
        auto_r=refresh_status_switch_via_userid(current_user.user_id)
        country_name=sorted(country_li(current_user.host_code))
        country_name.remove(current_user.post)
        eb=eb_fnt(current_user.post)
        msg_data_eb=''
        msg_data_rec=r(msg_rec(current_user.host_code,current_user.post))
        msg_data_sent=r(msg_sent(current_user.host_code,current_user.post))
        if eb_fnt(current_user.post)==True:
            eb=True
            msg_data_eb=r(msg_for_eb(current_user.host_code))
        return render_template('confi.html',point_list=point_list,all_opt=all_opt,confi_srt=confi_srt,auto_r=True,chits=swit(current_user.host_code),h_c=False,usr_country=current_user.post,country_list=country_name,msg_data_eb=msg_data_eb,eb=eb_fnt(current_user.post),msg_data_sent=msg_data_sent,msg_data_rec=msg_data_rec ,title='Committee')
    else:
        return redirect(url_for('login'))

@login_required
@app.route("/confi_sort", methods=['GET', 'POST'])
def sort_msg():
    if current_user.is_authenticated:
        confi_srt= True
        chits = swit(current_user.host_code)
        auto_r=refresh_status_switch_via_userid(current_user.user_id)
        sort_country_q=request.form['sort_country']
        sort_query_q=request.form['sort_query']
        if sort_country_q==all_opt and sort_query_q==all_opt:
            return redirect(url_for('messages'))
            return redirect(url_for('messages'))
        country_lst_sort=sorted(country_li(current_user.host_code))
        country_lst_sort.remove(current_user.post)
        eb=eb_fnt(current_user.post)
        msg_data_eb=''
        msg_data_rec=r(msg_sort_r(current_user.host_code,current_user.post,sort_country_q,sort_query_q))
        msg_data_sent=r(msg_sort_s(current_user.host_code,current_user.post,sort_country_q,sort_query_q))
        if eb_fnt(current_user.post) == True:
            eb=True
            msg_data_eb=r(via_eb_sort(current_user.host_code,sort_country_q,sort_query_q))

        return render_template('confi.html',confi_srt=confi_srt,point_list=point_list,all_opt=all_opt,auto_r=False,chits=swit(current_user.host_code),h_c=False,usr_country=current_user.post,country_list=country_lst_sort,msg_data_eb=msg_data_eb,eb=eb_fnt(current_user.post),msg_data_sent=msg_data_sent,msg_data_rec=msg_data_rec ,title='Committee')
    else:
        return redirect(url_for('login'))







@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@login_required
@app.route("/reply",methods=["POST","GET"])
def reply_msg():
    chits=swit(current_user.host_code)
    d_id= request.form["reply"]
    to_cont=reply_to(current_user.host_code,d_id)
    from_c=current_user.post
    msg=request.form["reply_msg"]
    try:
        via_eb=request.form["Via_EB"]
        if str(via_eb) == 'Yes' and to_cont!="EB":
            via_eb="Yes"
        else:
            via_eb="No"
    except:
        via_eb="No"
    if chits==True or current_user.post=="EB":
        message_adder_dab(current_user.host_code,to_cont,from_c,via_eb,msg,d_id,request.form["chits_point"])
        flash('Reply Sent !!!','success1')
    else:
        return ('',204)

    return redirect(url_for('messages'))




@app.route("/host_committee",methods= ["POST","GET"])
def host_committee():
    return render_template('host_committee.html', title= 'Committee Builder',s_head='Host Committee')

@app.route("/help_desk",methods= ["POST","GET"])
def help_desk():
    return render_template('help_desk.html', title= 'Help Desk',s_head='Help Desk')

@app.route("/about",methods= ["POST","GET"])
def about():
    return render_template('about.html', title= 'About',s_head='About')


@app.route("/faq",methods= ["POST","GET"])
def faq():
    return render_template('faq.html', title= 'CHITS | FAQ',s_head='FAQ')





