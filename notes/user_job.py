from .models import App_user
import json


class User_job():
    @classmethod
    def perform(self, ch, method, properties, body):
        print(" [x] %r" % body)
        data = eval(json.loads(json.dumps(body.decode('utf-8'))))
        app_user = App_user.objects.get(user_id=data['user_id'])
        app_user.last_active_time = data['timestamp']
        app_user.save()
