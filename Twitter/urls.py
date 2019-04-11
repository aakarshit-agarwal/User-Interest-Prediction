"""UserInterestPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getTrainingData/$', views.getTrainingData, name='getTrainingData'),
    url(r'^normalizeData/$', views.normalizeData, name='normalizeData'),
    url(r'^reduceData/$', views.reduceData, name='reduceData'),
    url(r'^trainMultinomialNBClassifier/$', views.trainMultinomialNBClassifier, name='trainMultinomialNBClassifier'),
    url(r'^trainClassifier/$', views.trainClassifier, name='trainClassifier'),
    url(r'^trainSVMClassifier/$', views.trainSVMClassifier, name='trainSVMClassifier'),
    url(r'^getTestData/$', views.getTestData, name='getTestData'),
    url(r'^getUserData/$', views.getUserData, name='getUserData'),
    url(r'^uploadDataSet/$', views.uploadDataSet, name='uploadDataSet'),
    url(r'^normalizeDataSet/$', views.normalizeDataSet, name='normalizeDataSet'),
    url(r'^trainNB/$', views.trainNB, name='trainNB'),
    url(r'^trainSVM/$', views.trainSVM, name='trainSVM'),
    url(r'^normalizeUserData/$', views.normalizeUserData, name='normalizeUserData'),
    url(r'^normalizeUserDataSet/$', views.normalizeUserDataSet, name='normalizeUserDataSet'),
    url(r'^predictInterest/$', views.predictInterest, name='predictInterest'),
    url(r'^predictNB/$', views.predictNB, name='predictNB'),
    url(r'^predictSVM/$', views.predictSVM, name='predictSVM'),
]
