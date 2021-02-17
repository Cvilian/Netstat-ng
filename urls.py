from django.conf.urls import url
from django.contrib import admin
# private import
#from fusioncharts.samples import graph
import fusioncharts.views as views

from fusioncharts import datahandler


# private import
#from fusioncharts import protocol_distribution

urlpatterns = [
    url(r'^$', views.init_chart, name='chart'),
    #url(r'^test/', views.init_chart, name='test'),
    url(r'^count/', views.update_chart, name='update_chart'),
    url(r'^admin/', admin.site.urls),
    url(r'^datahandler', datahandler.getdata),
]
