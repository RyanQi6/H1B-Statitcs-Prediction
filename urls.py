from django.conf.urls import url
from django.contrib import admin
from H1B_DB import views
from views import index
import MySQLdb
urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^MyCase$',views.MyCase,name='MyCase'),
    url(r'^Statistics$',views.Statistics,name='Statistics'),
    url(r'^Prediction$',views.Prediction,name='Prediction'),
    url(r'^findid$',views.findid, name='findid'),
    url(r'^update$',views.update, name='update'),
    url(r'^insert$',views.insert, name='insert'),
    url(r'^deleteid$',views.deleteid, name='deleteid'),
    url(r'^statlikeme$',views.statlikeme, name='statlikeme'),
    url(r'^statcolleague$',views.statcolleague, name='statcolleague'),
    url(r'^statstate$',views.statstate, name='statstate'),
    url(r'^visual$',views.visual, name='visual'),
    url(r'^visual2$',views.visual2, name='visual2'),
    url(r'^visual3$',views.visual3, name='visual3'),
    url(r'^jobbubble$',views.jobbubble, name='jobbubble'),
    url(r'^citybubble$',views.citybubble, name='citybubble'),
    url(r'^companybubble$',views.companybubble, name='companybubble'),
    url(r'^statcompany$',views.statcompany, name='statcompany'),
    url(r'^MakePredictions$',views.MakePredictions, name='MakePredictions'),
    url(r'^about$',views.about,name='about')
]
