from .models import Audit
import json


class Audit_job():
    @classmethod
    def perform(self, channel, method, properties, body):
        print(" [x] %r" % body)
        data = eval(json.loads(json.dumps(body.decode('utf-8'))))
        Audit.objects.create(
            model_type=data['type'], user_id=data['user_id'],  data=data)
