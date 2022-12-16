from django.urls import path
from authentification import views
from django.conf import settings


from django.conf.urls.static import static
from django.urls import path

from bibi.views import ajouter_document,telecharger_document,verification

urlpatterns = [
    path('add', ajouter_document, name='ajouter_document'),
    path('signup', views.signup, name='signup'),
path('v', verification, name='verification'),
path('signin', views.signin, name='signin'),
path('vu', views.signin, name='signin'),
path('', views.home, name='home'),
    path('signout', views.signout, name='signout'),
path('<id>', telecharger_document, name="telecharger_document"),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)