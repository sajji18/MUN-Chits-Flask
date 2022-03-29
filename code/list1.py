from app import *
import pandas as pd

'''sw1=usr(host_code='qw',user_id='b1',post='china')
dab.session.add(sw1)
dab.session.commit()
'''

def swit(host_id):
    try:
        return sw.query.filter_by(host_code=host_id).first().switch
    except:
        return False

def refresh_status_switch_via_userid(user_idq):
    try:
        return usr.query.filter_by(user_id=user_idq).first().auto_reply_switch
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

"""
print(swit('qw'))
change_switch('qw')
print(swit('qw'))
"""
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

'''
print(refresh_switch_via_userid('a1'))
change_switch_auto_r('a1')
print(refresh_switch_via_userid('a1'))
'''

def delete_by_host_code(host_id):
    try:
        x=usr.query.filter_by(host_code=host_id).all()
        for i in x:
            dab.session.delete(i)
        dab.session.commit()
    except:
        pass
    try:
        x= sw.query.filter_by(host_code=host_id).all()
        for i in x:
            dab.session.delete(i)
        dab.session.commit()
    except:
        pass
    try:
        x= message.query.filter_by(host_code=host_id).all()
        for i in x:
            dab.session.delete(i)
        dab.session.commit()
    except:
        pass


'''host_id='qw'
x=usr.query.filter_by(host_code=host_id).all()
for i in x:
    dab.session.delete(i)
dab.session.commit()

'''


def add_user(host_id,user_idd,country):
    dab.session.add(usr(host_code=host_id,user_id=user_idd,post=country))
    dab.session.commit()


def link_via_hostcode(host_id):
    return (sw.query.filter_by(host_code=host_id).first().link)


def chits_adder(host_id, link_q,organization):
    dab.session.add(sw(host_code=host_id,link=link_q,orgn=organization))
    dab.session.commit()

def organization_via_hostcode(host_id):
    return (sw.query.filter_by(host_code=host_id).first().orgn)


'''chits_adder('qw','www.sarveshd444.pythonanywhere.com',"MEMUN")
add_user('qw','d1', 'UK')
add_user('qw','e1', "China")
add_user('qw','f1', "DPRK")'''

'''print(link_via_hostcode('qw'))'''

'''add_user('LMUN-ECEJR', 'P9dg86HA','Victoria Newton')'''
def update(userid,npost):
    usr.query.filter_by(user_id=userid).first().post=npost
    dab.session.commit()


def update_link(host_id,linkf):
    sw.query.filter_by(host_code=host_id).first().link=linkf
    dab.session.commit()
def message_to_list(query_result):
    msg_lst=[]
    for i in query_result:
        try:
            t_m=[]
            t_m.append(i.id)
            t_m.append(i.host_code)
            t_m.append(i.to)
            t_m.append(i.from_c)
            t_m.append(i.viaeb)
            t_m.append(i.message)
            t_m.append(i.timestamp)
            t_m.append(i.replyid)
            msg_lst.append(t_m)
        except:
            pass
    return msg_lst

def sw_to_list(query_result):
    sw_lst=[]
    for i in query_result:
        try:
            t_m=[]
            t_m.append(i.host_code)
            t_m.append(i.link)
            t_m.append(i.orgn)
            sw_lst.append(t_m)
        except:
            pass
    return sw_lst

def usr_to_list(query_result):
    usr_lst=[]
    for i in query_result:
        try:
            t_m=[]
            t_m.append(i.host_code)
            t_m.append(i.user_id)
            t_m.append(i.post)
            usr_lst.append(t_m)
        except:
            pass
    return usr_lst


def message_adder_for_shifting(id_f,host_id,to_c,from_country,viaeb_c,message_c,replyid_c):
    msg=message(id=id_f,host_code=host_id,to=to_c,timestamp=current_time(),from_c=from_country,viaeb=viaeb_c,message=message_c,replyid=replyid_c)
    dab.session.add(msg)
    dab.session.commit()

def shift_database(file_name_message,file_name_sw,file_name_usr):
    df=pd.read_csv((file_name_message))
    msg_list=df.values.tolist()
    df=pd.read_csv((file_name_usr))
    usr_list=df.values.tolist()
    df=pd.read_csv((file_name_sw))
    sw_list=df.values.tolist()
    for i in sw_list:
        chits_adder(i[0],'',i[2])
    for i in usr_list:
        add_user(i[0],i[1],i[2])
    for i in msg_list:
        message_adder_for_shifting(i[0],i[1],i[2],i[3],i[4],i[5],i[6])

column_for_messages=["msg_id",'host_code',"to","from","viaeb","message","datetime","replyid"]
column_for_sw=["host_code","link","organization"]
column_for_usr=["host_code","user_id","post"]

def create_shifting(file_name_message='messages.csv',file_name_sw='sw.csv',file_name_usr='usr.csv'):
    df=pd.DataFrame(message_to_list(message.query.all()),columns=column_for_messages)
    df.to_csv((file_name_message),index=False)
    df=pd.DataFrame(sw_to_list(sw.query.all()),columns=column_for_sw)
    df.to_csv((file_name_sw),index=False)
    df=pd.DataFrame(usr_to_list(usr.query.all()),columns=column_for_usr)
    df.to_csv((file_name_usr),index=False)
'''
lkl=['Chairperson','Secretariat','Vice Chairperson','Rapporteur']
for o in lkl:
    x=usr.query.filter_by(post=o).all()
    for i in x:
        dab.session.delete(i)
    dab.session.commit()
 '''




dfg=message.query.all()

print(len(dfg))