from flask import Blueprint, request, redirect, render_template, url_for,Flask, flash, session
from flask.views import MethodView

from flask_mongoengine.wtf import model_form
from tumblelog.models import Post, Comment, Login, Aacargo, CaptureQueue
from tumblelog import mailComm, app
import uuid
from tumblelog.session import requires_auth
from tumblelog import db


posts = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):

    decorators = [requires_auth]

    form = model_form(Aacargo)

    def get_context(self,waybillNumber=None):
        posts = ''
        if waybillNumber != None and waybillNumber != ''.strip():
            posts = Aacargo.objects(airWaybillNumber=waybillNumber)

        form = self.form(request.form)
        context = {
            'posts': posts
            ,'form': form
        }
        return context

    def get(self):
        context = self.get_context()
        print context
        return render_template('posts/list.html', **context)

    def post(self):
        airWaybillNumber = request.form['airWaybillNumber']
        context = self.get_context(airWaybillNumber)

        posts = context.get('posts')

        if len(posts) == 0:
            exists = CaptureQueue.objects(captureNo=airWaybillNumber)
            if len(exists) == 0:
                """
                d:DONE
                w:WAIT
                c:CAPTURING
                """
                CaptureQueue(captureNo=airWaybillNumber,captureStatus='w').save()

            flash('sorry your data now have not capture,but already add to capture queue. please wait few minute!')
            return render_template('posts/success.html')

        return render_template('posts/list.html', **context)

class DetailView(MethodView):

    decorators = [requires_auth]

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)
        context = {
            'post': post
            ,'form': form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))
        return render_template('posts/detail.html', **context)

class RegisterView(MethodView):


    form = model_form(Login,exclude=['identity']
        ,field_args={'password': {'password': True},'confirm': {'password': True}})

    def get_context(self,email=None):
        form = self.form(request.form)
        post = None

        if (email != None):
            post = Login.objects(email=email).first()

        context = {
            'post': post
            ,"form": form
        }
        return context

    def get(self):
        context = self.get_context()
        return render_template('posts/register.html', **context)

    def post(self):
        context = self.get_context(request.form['email'])
        posts = context.get('post')
        form = context.get('form')

        if (posts != None):
            flash('This email address already exists!')
            return render_template('posts/success.html')
        else:
            recipient = form.email.data
            if form.validate():
                form.save()

                context = self.get_context(request.form['email'])
                posts = context.get('post')
                form = context.get('form')
                
                identity = str(posts.identity)
                message = mailComm.get('message')
                mail = mailComm.get('mail')
                mail.send(message('This is Flask-Email Test'
                    , body= 'click this url to verify yourID\r\nhttp://127.0.0.1:5000/success/?identity=%s' % identity
                    , sender = 'thassange@163.com'
                    , recipients = [recipient]))

                return redirect('success')

        return render_template('posts/register.html', **context)

class SuccessView(MethodView):

    def get(self,identity):
        identity = str(request.args.get('identity', 'get')).replace('get','')
        if str(identity) == '':
            flash('you have a email, check it.')
            return render_template('posts/success.html')

        user = Login.objects(identity=identity).first()

        if user == None and str(identity) != '' :
            flash('This check code is invalid.')
            return render_template('posts/success.html')
        else:
            Login.objects(identity=identity).update(**{'identity': 'succeed'})
            flash('Gratulation your account verify succeed!')
            return render_template('posts/success.html')

class LoginView(MethodView):

    form = model_form(Login,exclude=['identity','email','confirm']
,field_args={'password': {'password': True}})

    def get_context(self):
        form = self.form(request.form)
        post = None

        context = {
           'post': post
           ,'form': form
        }
        return context

    def get(self,type=None):
        type = str(request.args.get('type', 'get')).replace('get','')
        print type
        if type == 'out':
            session['token_user'] = ''
            return redirect('/login')
        context = self.get_context()
        return render_template('posts/login.html', **context)

    def post(selft,type=None):
        req_user_name = request.form['username']
        req_pass_word = request.form['password']
        user_info = Login.objects(username=req_user_name,password=req_pass_word).first()
        

        if user_info != None:
            identity = user_info['identity']
            if identity == 'succeed':
                session['token_user'] = req_user_name
                return redirect('/')
            else:
                flash('Please verify this account.')
                return render_template('posts/success.html') 
        else:
            flash('This account is invalid.')
            return render_template('posts/success.html')

# Register the urls
posts.add_url_rule('/', view_func = ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
#posts.add_url_rule('/success/', view_func=SuccessView.as_view('success'))
posts.add_url_rule('/success/', defaults={'identity': None}, view_func=SuccessView.as_view('success'))
posts.add_url_rule('/login/',defaults={'type': None}, view_func=LoginView.as_view('login'))