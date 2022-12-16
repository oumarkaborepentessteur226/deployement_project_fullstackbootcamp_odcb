import codecs

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os

from application.settings import BASE_DIR
from bibi.forms import DocumentForm
from bibi.models import Document





def ajouter_document(request):
   form = DocumentForm()
   if request.method == 'POST':
      form = DocumentForm(request.POST, request.FILES)
      if form.is_valid():
         print(form.cleaned_data)
         new = Document.objects.create(**form.cleaned_data)
         new.save()



   else:
      form = DocumentForm()
   return render(request, 'authentification/index.html', {'form': form})

   # if request.method == 'POST':
   #    form = DocumentForm(request.POST, request.FILES)
   #    if form.is_valid():
   #       nom = form.cleaned_data['nom']
   #       file = form.cleaned_data['file']
   #       description = form.cleaned_data['description']
   #       envoi = 1
   #       try:
   #          doc = Document.objects.get(nom = nom)
   #       except Document.DoesNotExist:
   #          doc = Document(nom = nom, file = file, description = description)
   #          doc.save()
   #          message = "Le document {a} a bien été ajouté !".format(a = nom)
   #       else:
   #          message = "Le document {a} existe déjà !".format(a = nom)
   # return render(request, 'authentification/index.html', locals())


def verification(request):
   profile = Document.objects.all()
   return render(request, "authentification/view.html",{'profile': profile})

   #    my_file = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, "media\pdf", f.nom)

def telecharger_document(request, id):
   f = Document.objects.filter(id = id).first()
   fl_path = f.file.path
   filename = f.file.name
   if f is not None:
      fl_path = os.path.join(BASE_DIR,settings.BASE_DIR, settings.MEDIA_ROOT, filename)
      data = open(fl_path,'rb').read()
      response = HttpResponse(data, content_type='application/pdf')
      response["Content-Disposition"] = u"attachment; filename={0}.pptx".format(f.nom)
      return response
   else:
      raise Http404

# def telecharger_document(req, id):
#    project = get_object_or_404(Document, id=id)
#
#    fl_path = project.file.path
#    filename = project.file.name
#
#    fl = codecs.open(fl_path, 'r', encoding='ISO-8859-1')
#    mime_type = "application/pdf"
#    response = HttpResponse(fl, content_type=mime_type)
#    response['Content-Disposition'] = "attachment; filename=%s" % filename
#    return response