from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .forms import EventCreateForm, NoteCreateForm, PropertyCreateForm
from models import Event, Property, Note
from .forms import EventCreateForm

from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):

	#redirect to login if user isn't authenticated

	return render(request, "main/base.html")

@login_required(login_url='/accounts/login/')
def dashboard(request):
		return render(request, "main/base.html")

def properties(request):
	context = {
			"properties" : Property.objects.filter(user = request.user)
		}
	return render (request, "main/properties.html", context)

def add_property(request):
	if request.method == "POST":
		prop_form = PropertyCreateForm(request.POST)
		if prop_form.is_valid():
			prop = prop_form.save(commit=False)
			prop.user = request.user
			prop.save()
			context = {
				"properties" : Property.objects.filter(user = request.user)
			}
			print "valid form"
			return render (request, "main/properties.html", context)
		else:
			context={
				'form':prop_form
			}
			print "invalid form"
			return HttpResponseBadRequest(render (request,'main/add_property.html',context))
	else:
		context={
			'form':PropertyCreateForm()
		}
		print "GET"
		return render(request,'main/add_property.html',context)


def event(request,event_id, prop_id):
	event = Event.objects.get(pk=event_id)
	notes = event.note_set.all()

	context={
	'prop_id':prop_id,
	'event':event,
	"notes":notes
	}
	return render(request, 'main/event.html',context)

def events(request, prop_id):
	property = Property.objects.get(pk=prop_id)
	events = property.event_set.all()
	print events

	context={
	'property' : property,
	'events':events
	}
	return render(request, 'main/events.html',context)


def add_event(request, prop_id):
	if request.POST:
		event_form = EventCreateForm(request.POST)
		if event_form.is_valid():
			event = event_form.save(commit=False)
			event.property = Property.objects.get(pk=prop_id)
			event.save()
			return redirect("/property/{}/event/{}".format(prop_id, event.id))
		else:
			context={
				'form':event_form
			}
			return HttpResponseBadRequest(render (request,'main/add_event.html',context))
	else:
		context={
			'form':EventCreateForm(),
			'prop_id':prop_id,

		}
		return render(request,'main/add_event.html',context)


def note(request,event_id,prop_id,note_id):
	note = Note.objects.get(pk=note_id)
	context={
	'event_id':event_id,
	'prop_id':prop_id,
	"note":note
	}
	return render(request, 'main/note.html', context)

def notes(requst,event_id,prop_id):
		event = Event.objets.get(pk=event_id)
		notes = event.note_set.all()

		context={
		'event_id':event_id,
		'prop_id':prop_id,
		}

		return render(request, 'main/note.html', context)

def add_note(request,prop_id, event_id):
	if request.POST:
		note_form = NoteCreateForm(request.POST)
		if note_form.is_valid():
			note = note_form.save(commit=False)
			note.event = Event.objects.get(pk=event_id)
			note.save()

			
			return HttpResponse(note.id)
		else:
			context={
				'form':note_form
			}
			return HttpResponseBadRequest(render (request,'main/add_note.html',context))
	else:
		context={
			'form':NoteCreateForm(),
			'prop_id':prop_id,
			'event_id':event_id
		}
		return render(request,'main/add_note.html',context)

def add_file(request,prop_id, event_id, note_id):
    # example from fileupload project
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
		form = DocumentForm()
		context={
			'form':form
		}
		return HttpResponseBadRequest(render (request,'main/add_file.html',context))
          # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'main/note.html',{'documents': documents, 'form': form} )
