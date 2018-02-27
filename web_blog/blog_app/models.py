from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin

class Permission:
	FOLLOW = 0x01
	COMMIT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS =0x08
	ADMINISTER =0x08


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	default = db.Column(db.Boolean,default=False,index=True)
	permissions = db.Column(db.Integer)
	
	def __repr__(self):
		return '<Role %r>' % self.name

	@staticmethod
	def insert_roles():
		roles = {
			'User':(Permission.FOLLOW |
					Permission.COMMIT |
					Permission.WRITE_ARTICLES,True),
			'Moderator':(Permission.FOLLOW |
					Permission.COMMIT |
					Permission.WRITE_ARTICLES |
					Permission.MODERATE_COMMENTS,False),
			'Administrator':(0xff,False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()			


	users = db.relationship('User',backref='role',lazy='dynamic')

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True,index=True)
	def __repr__(self):
		return '<User %r>' % self.username
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64),unique=True,index=True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
	posts = db.relationship('Post',backref='author',lazy='dynamic')

	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
		if self.role is None:
			if self.email == '846976792@qq.com':
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default = True).first()
			
	def can(self,permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)


	@property
	def password(self):
		raise AttributeError('password is not readable attribute')	

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

class AnonymousUser(AnonymousUserMixin):
	def can(self ,permissions):
		return False		
	def is_administrator(self):
		return False

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text)
	author_id = db.Column(db.Integer,db.ForeignKey('users.id')) 


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
 
login_manager.anonymous_user = AnonymousUser
