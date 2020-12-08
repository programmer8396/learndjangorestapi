from django.http import HttpResponse

from django.core.serializers import serialize

import json 

class SerializeMixin(object):
    def serialize(self, qs):
        json_data = serialize('json', qs)
        pdict  =json.loads(json_data)
        finallist= []
        for obj in pdict:
            emp_data = obj["fields"]
            finallist.append(emp_data)
        json_data = json.dumps(finallist)
        return json_data

class HttpResponseMixin(object):
    def render_to_http_response(self,json_data,status=200):
        return HttpResponse(json_data, content_type="application/json",status=status)