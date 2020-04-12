from rest_framework import routers
from blog import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'userdetail', myapp_views.UsersDetailViewset)