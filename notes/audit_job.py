from .models import Audit
import json


class AuditJob():
    @classmethod
    def perform(self, channel, method, properties, body):
        print(" [x] %r" % body)
        # I can't use eval, look up why..!
        data = eval(json.loads(json.dumps(body.decode('utf-8'))))
        Audit.objects.create(
            model_type=data['type'], user_id=data['user_id'],  data=data)
