
from flask_wtf import Form #导入处理表单的扩展 
from wtforms import StringField,SubmitField,TextAreaField #导入 文本字段 提交按钮
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField 





class NameForm(Form):
	"""validators指定一个由验证函数组成的列表 """
	"""require()确保字段不为空"""
	name = StringField("what is your name ?",validators = [Required()])
	sumbit = SubmitField('Submit')


class PostForm(Form):
	body = PageDownField("blog_body",validators = [Required()])
	sumbit = SubmitField('Submit')


