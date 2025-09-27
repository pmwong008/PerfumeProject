import mongoengine as me
from django.conf import settings
import os

me.connect(
    db=os.getenv("MONGO_COLLECTION"),
    host=settings.MONGODB_URI
    )

class UserProfile(me.Document):
    user_id = me.IntField(required=True, unique=True)
    name = me.StringField(max_length=50,required=True)
    address = me.StringField(max_length=255,required=True)
    points = me.IntField(default=0)
    status = me.BooleanField(default=True)
