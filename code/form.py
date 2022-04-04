from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField ,RadioField ,PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from models import *



class join_c(FlaskForm):
    host_code = StringField('Host Code', validators=[DataRequired()])
    d_pass = StringField('Delegate Pass', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('  Join  ')
    def validate_host_code(self, host_code):
        global h_cd
        global hc
        hc=host_code.data
        if hc in host_c_list:
            h_cd=True
            return h_cd,hc
        else:
            h_cd=False
            raise ValidationError('Invalid Host Code !!!')
            return h_cd,hc

    def validate_d_pass(self, d_pass):
        if usr.query.filter_by(host_code=hc,user_id=d_pass.data).first() or h_cd!=True:
            pass
        else:
            raise ValidationError('Invalid Delegate Pass !!!')



class reply(FlaskForm):
    viaeb = BooleanField('Via EB')
    message=TextAreaField(u'Message',validators=[DataRequired(),Length(10000)])
    submit = SubmitField(' Reply ')

