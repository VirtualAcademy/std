#from django.shortcuts import render
from django.template.response import TemplateResponse
from cyph import Rot13

# Create your views here.
def cyph(request,tempname=None):
	
	if request.method == 'POST':
		txt=request.POST.get('text')
		text=Rot13(txt)
		value=text.rot13()
		context={'value':value}
		return TemplateResponse(request,tempname, context)
		
	return TemplateResponse(request,tempname)