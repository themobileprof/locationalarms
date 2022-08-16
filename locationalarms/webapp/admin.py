from django.contrib import admin

# Register your models here.
from .models import Blacklist
from .models import Whitelist
from .models import EventTag
from .models import Location
from .models import SubscriptionType

admin.site.register(Blacklist)
admin.site.register(Whitelist)
admin.site.register(EventTag)
admin.site.register(Location)
admin.site.register(SubscriptionType)