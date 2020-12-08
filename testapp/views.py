from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from testapp.models import Employee
import json
from django.core.serializers import serialize
from testapp.mixins import SerializeMixin
from testapp.mixins import HttpResponseMixin

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from testapp.utils import is_json
from testapp.forms import  EmployeeForm

# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class EmployeeDetailsCBV(HttpResponseMixin, SerializeMixin ,View):

    def get_object_by_id(self, id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None
        return emp

    def get(self, request, id, *args, **kwargs):
        try:

            emp  =Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data = json.dumps({"msg":"The request resourse not available."}) 
            return self.render_to_http_response(json_data, status=400)
        else:
            json_data = self.serialize([emp,])
            return self.render_to_http_response(json_data)


    def put(self, request, id, *args, **kwargs):
        emp = self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({"msg":"No matched record found not possible to perform updation."}) 
            return self.render_to_http_response(json_data, status=404)
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"Please send a valid json only"}) 
            return self.render_to_http_response(json_data, status=404)
        provided_data = json.loads(data)
        original_data = {
            'eno': emp.eno,
            'ename':emp.ename,
            'esal' : emp.esal,
            'eaddr': emp.eaddr
        }
        original_data.update(provided_data)
        form = EmployeeForm(original_data, instance=emp)

        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"msg":'Resource Created Succesfully'})
            return self.render_to_http_response(json_data)

        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)

    def delete(self, request, id,  *args, **kwargs):
        emp = self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({"msg":"No matched record found not possible to perform updation."}) 
            return self.render_to_http_response(json_data, status=404)
        status, deleted_item = emp.delete()
        if status == 1:
            json_data=json.dumps({'msg':'Resource deleted Successfully'})
            return self.render_to_http_response(json_data)
        json_data=json.dumps({'msg':'Unable to delete...... Plz try again'})
        return self.render_to_http_response(json_data)

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeListCBV(HttpResponseMixin, SerializeMixin, View):
    def get(self, request, *args, **kwargs):
        qs  =Employee.objects.all()
        json_data = self.serialize(qs)
        return HttpResponse(json_data, content_type="application/json")
    
    def post(self, request, *args, **kwargs):

        data = request.body  ## data
        
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':'Please send valid json only'})
            return self.render_to_http_response(json_data, status=400)
            

        empdata = json.loads(data)
        form = EmployeeForm(empdata)

        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"msg":'Resource Created Succesfully'})
            return self.render_to_http_response(json_data)

        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html",{})

    
