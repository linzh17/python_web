
from flask import render_template,session,redirect,url_for,request,current_app
from .. import db
from . import main
from . forms import NameForm,PostForm
from flask.ext.login import login_required, current_user
from ..models import Permission, Role, User, Post


@main.route('/',methods=['GET','POST'])
def index():
	form = PostForm()
			#下面的函数 会调用字段上附属的require验证函数，名字不为空 返回true"""
	if current_user.can(Permission.WRITE_ARTICLES) and \
			form.validate_on_submit():
		post = Post(body=form.body.data,author=current_user._get_current_object())
		db.session.add(post)	
		"""重定向"""
		return redirect(url_for('.index'))
		"""重定向造成post请求结束 原来的输入的数据消失，这时可以用session 来获取保存的数据"""
	page = request.args.get('page',1,type=int)
	pagination = Post.query.paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	posts = pagination.items	
	return render_template('user-form.html',form = form,posts=posts,Permission=Permission,pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
	post=Post.query.get_or_404(id)
	return render_template('user-post.html',posts=[post])

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(404)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		return redirect(url_for('.post',id=post.id))
	form.body.data = post.body
	return render_template('edit-post.html',form=form)		


@main.route('/del/<int:id>',methods=['GET','POST'])
@login_required
def delete(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(404)
	return render_template('del-post.html',posts=[post])

@main.route('/del/<int:id>/sure',methods=['GET','POST'])
@login_required
def delete_sure(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(404)
	db.session.delete(post)	
	return redirect(url_for('.index'))		