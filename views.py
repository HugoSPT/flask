from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from models import User

users = Blueprint('users', __name__, template_folder='templates')


class ListView(MethodView):
    
    def get(self):
        users = User.objects.all()
        return render_template('users/list.html', users=users)


class DetailView(MethodView):

    def get(self, user):
        user = User.objects.get_or_404(name=user)
        print "HERE"
        return render_template('users/detail.html', user=user)


# Register the urls
users.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/<user>/', view_func=DetailView.as_view('detail'))