from flask import Blueprint, request, redirect, render_template, url_for
from flask.ext.mongoengine.wtf import model_form
from flask.views import MethodView
from models import User

users = Blueprint('users', __name__, template_folder='templates')


class ListView(MethodView):
    
    form = model_form(User, exclude=['created_at'])
    
    def get_context(self):
        users = User.objects.all()
        form = self.form(request.form)

        context = {
            "users": users,
            "form": form
        }
        return context
    
    def get(self):
        context = self.get_context()
        return render_template('users/list.html', **context)

    def post(self):
        context = self.get_context()
        form = context.get('form')

        if form.validate():
            user = User()
            form.populate_obj(user)

            user.save()

        return render_template('users/list.html', **context)

class DetailView(MethodView):

    def get(self, name):
        user = User.objects.get_or_404(name=name)
        return render_template('users/detail.html', user=user)


# Register the urls
users.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/<name>/', view_func=DetailView.as_view('detail'))