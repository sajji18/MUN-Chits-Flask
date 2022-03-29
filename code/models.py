from mun_details import *
import pandas as pd
from setup import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



def r(lst):
    lst.reverse()
    return lst


class usr(dab.Model, UserMixin):
    id = dab.Column(dab.Integer, primary_key=True)
    host_code=dab.Column(dab.String, nullable=False)
    user_id = dab.Column(dab.String(20), unique=True, nullable=False)
    post = dab.Column(dab.String(50), nullable=False)
    auto_reply_switch=dab.Column(dab.Boolean,nullable=False,default=True)
    attendance=dab.Column(dab.Boolean,nullable=False,default=False)
    
    def get_reset_token(self, expires_sec=600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return usr.query.get(user_id)
    def __repr__(self):
        return f"user('{self.host_code}','{self.user_id}', '{self.post}')"

class sw(dab.Model):
    host_code=dab.Column(dab.String, primary_key=True)
    switch = dab.Column(dab.Boolean,nullable=False,default=True)
    link = dab.Column(dab.Text,nullable=False)
    orgn=dab.Column(dab.String, nullable=False)
    def __repr__(self):
        return f"user('{self.host_code}','{self.link}','{self.orgn}')"


class message(dab.Model):
    id = dab.Column(dab.Integer, primary_key=True)
    host_code = dab.Column(dab.String, nullable=False)
    to=dab.Column(dab.String(50), nullable=False)
    from_c = dab.Column(dab.String(50), nullable=False)
    viaeb = dab.Column(dab.String(10), nullable=False)
    message = dab.Column(dab.Text, nullable=False)
    timestamp=dab.Column(dab.String, nullable=False)
    point=dab.Column(dab.String, nullable=False,default='General')
    replyid = dab.Column(dab.String, nullable=False)


    def __repr__(self):
        return f"user('{self.host_code}','{self.timestamp}','{self.to}', '{self.from_c}', '{self.viaeb}', '{self.message}', '{self.replyid}')"




'''
def message_adder_dab(host_code,to,from_c,viaeb,message,replyid):
    msg= message(host_code=host_code,to=to,from_c=from_c,viaeb=viaeb,message=message,replyid=replyid)
    dab.session.add(msg)
    dab.session.commit()
'''
def message_adder_dab(host_id,to_c,from_country,viaeb_c,message_c,replyid_c,chit_pnt='General'):
    msg=message(host_code=host_id,to=to_c,timestamp=current_time(),from_c=from_country,viaeb=viaeb_c,message=message_c,point=chit_pnt,replyid=replyid_c)
    dab.session.add(msg)
    dab.session.commit()
'''
message_adder_dab(host_id='qw',to_c='china',from_country='england',viaeb_c='Yes',message_c='koooooooo',replyid_c=2)
'''
def eb_fnt(pst):
    try:
        if pst in eb_d:
            return True
        else:
            return False
    except:
        return False

def swit(host_id):
    try:
        return sw.query.filter_by(host_code=host_id).first().switch
    except:
        return False

def change_switch(host_id):
    try:
        if current_user.post=='EB':
            if sw.query.filter_by(host_code=host_id).first().switch==True:
                sw.query.filter_by(host_code=host_id).first().switch=False
                dab.session.commit()
            else:
                sw.query.filter_by(host_code=host_id).first().switch=True
                dab.session.commit()
    except:
        pass

def change_switch_auto_r(user_idq):
    try:
        if usr.query.filter_by(user_id=user_idq).first().auto_reply_switch==True:
            usr.query.filter_by(user_id=user_idq).first().auto_reply_switch=False
            dab.session.commit()
        else:
            usr.query.filter_by(user_id=user_idq).first().auto_reply_switch=True
            dab.session.commit()
    except:
        pass


def message_to_list(query_result):
    msg_lst=[]
    for i in query_result:
        try:
            t_m=[]
            t_m.append(i.id)
            t_m.append(i.to)
            t_m.append(i.from_c)
            t_m.append(i.viaeb)
            t_m.append(i.message)
            t_m.append(i.timestamp)
            t_m.append(i.point)
            t_m.append(i.replyid)
            msg_lst.append(t_m)
        except:
            pass
    return msg_lst


def msg_sent(host_id,admin_country):
    temp_msg=message_to_list(message.query.filter_by(host_code=host_id , from_c=admin_country).all())
    fnl=[]
    for p in temp_msg:
        try:
            if p[-1].isnumeric():
                reply = message.query.filter_by(id=int(p[-1])).first().message
                p.pop()
                p.append(reply)
                fnl.append(p)
            else:
                fnl.append(p)
        except:
            pass
    return fnl



def msg_rec(host_id,admin_country):
    temp_msg=message_to_list(message.query.filter_by(host_code=host_id , to=admin_country).all())
    fnl=[]
    for p in temp_msg:
        try:
            if p[-1].isnumeric():
                reply = message.query.filter_by(id=int(p[-1])).first().message
                p.pop()
                p.append(reply)
                fnl.append(p)
            else:
                fnl.append(p)
        except:
            pass
    return fnl



def msg_sort_r(host_id,admin_country,sort_country,sort_query):
    msg_r=msg_rec(host_id,admin_country)
    df= pd.DataFrame(msg_r,columns=column_for_messages)
    if sort_country==all_opt and sort_query!=all_opt:
            filt = (df['point'])==sort_query
            return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query==all_opt:
        filt = (df['from'])==sort_country
        return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query!=all_opt:
        filt = ((df['from'])==sort_country) & ((df['point'])==sort_query)
        return (df[filt].values.tolist())

def organization_via_hostcode(host_id):
    return (sw.query.filter_by(host_code=host_id).first().orgn)

def country_li(host_id):
    user=usr.query.filter_by(host_code=host_id).all()
    c_l=[]
    for i in user:
        if i.post in c_l:
            pass
        else:
            c_l.append(i.post)
    return c_l



def msg_sort_s(host_id,admin_country,sort_country,sort_query):
    msg_s=msg_sent(host_id,admin_country)
    df= pd.DataFrame(msg_s,columns=column_for_messages)
    if sort_country==all_opt and sort_query!=all_opt:
        filt = (df['point'])==sort_query
        return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query==all_opt:
        filt = (df['to'])==sort_country
        return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query!=all_opt:
        filt = ((df['to'])==sort_country) & ((df['point'])==sort_query)
        return (df[filt].values.tolist())


def msg_for_eb(host_id):
    temp_msg=message_to_list(message.query.filter_by(host_code=host_id , viaeb='Yes').all())
    fnl=[]
    for p in temp_msg:
        try:
            if p[-1].isnumeric():
                reply = message.query.filter_by(id=int(p[-1])).first().message
                p.pop()
                p.append(reply)
                fnl.append(p)
            else:
                fnl.append(p)
        except:
            pass
    return fnl

def refresh_status_switch_via_userid(user_idq):
    try:
        return usr.query.filter_by(user_id=user_idq).first().auto_reply_switch
    except:
        return False

def reply_to(host_id,mssg_id):
    return message.query.filter_by(id=int(mssg_id)).first().from_c

def reply_msg_via_id(msg_id):
    try:
        if msg_id.isnumeric():
            reply = message.query.filter_by(id=int(msg_id)).first().message
            return reply
    except:
        return None

'''
print(msg_for_eb('qw'))
'''
def via_eb_sort(host_id,sort_country,sort_query):
    msg_eb= msg_for_eb(host_id)
    df= pd.DataFrame(msg_eb,columns=column_for_messages)
    if sort_country==all_opt and sort_query!=all_opt:
        filt = ((df['point'])==sort_query)
        return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query==all_opt:
        filt = ((df['to']==sort_country) | (df['from']==sort_country))
        return (df[filt].values.tolist())
    elif sort_country!=all_opt and sort_query!=all_opt:
        filt = (((df['point'])==sort_query) & ((df['to']==sort_country)) | (((df['point'])==sort_query) & (df['from']==sort_country)))
        return (df[filt].values.tolist())

'''
print(via_eb_sort('qw','china'))
'''
def link_via_hostcode(host_id):
    return (sw.query.filter_by(host_code=host_id).first().link)

def update_link(host_id,linkf):
    sw.query.filter_by(host_code=host_id).first().link=linkf
    dab.session.commit()


