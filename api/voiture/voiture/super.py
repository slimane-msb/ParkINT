from django.contrib.auth import get_user_model
import os 

User = get_user_model()
user = User.objects.get(username=os.environ.get('SUPERUSER_NAME', 'admin'))
user.set_password(os.environ.get('SUPERUSER_PASSWORD', 'admin'))
user.save()
