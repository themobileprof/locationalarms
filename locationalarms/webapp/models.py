from django.contrib.gis.db import models
# from django.contrib.gis.geos import Point


class Blacklist(models.Model):
    twitter_id = models.CharField(max_length=50)
    category = models.CharField(max_length=10)

    def __str__(self):
        return self.twitter_id


class EventTag(models.Model):
    tag = models.CharField(max_length=10)
    synonyms = models.CharField(max_length=60)
    desc = models.CharField(max_length=40)

    def __str__(self):
        return self.tag


class Liveevent(models.Model):
    event_tag = models.ForeignKey(EventTag, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    source = models.CharField(max_length=38)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    noise = models.IntegerField()
    value = models.IntegerField()
    notification_level = models.IntegerField()
    confirmed = models.CharField(max_length=10, blank=True, null=True)


class Location(models.Model):
    location = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    coord = models.PointField(srid=4326)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.location

    class Meta:
        unique_together = (('location', 'state'),)


class NotificationLog(models.Model):
    user_subscriptions = models.ForeignKey('UserSubscription', on_delete=models.CASCADE)
    date_sent = models.DateTimeField('Date sent')


class Recommendation(models.Model):
    live_event = models.ForeignKey(Liveevent, models.DO_NOTHING)
    recommendation = models.CharField(max_length=300, blank=True, null=True)


class State(models.Model):
    state = models.CharField(max_length=15)
    coord = models.PointField(srid=4326)

    def __str__(self):
        return self.state


class SubscriptionType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class TweetData(models.Model):
    tweet = models.CharField(max_length=200)
    twitter_user_id = models.CharField(max_length=50)
    tweet_date = models.CharField(max_length=10)
    tweet_time = models.CharField(max_length=10)
    status = models.CharField(max_length=33, blank=True, null=True)
    value = models.IntegerField()
    live_event = models.ForeignKey(Liveevent, models.DO_NOTHING)
    confirmed = models.CharField(max_length=10, blank=True, null=True)


class UserSubscription(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    notification_level = models.IntegerField()

    class Meta:
        unique_together = (('user_id', 'location'),)



class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField('User email')
    phone = models.CharField(max_length=20)
    twitter_id = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    subscription = models.ManyToManyField(UserSubscription)

    def __str__(self):
        return self.name


class Whitelist(models.Model):
    twitter_id = models.CharField(max_length=50)
    category = models.CharField(max_length=17)

    def __str__(self):
        return self.twitter_id



class TweetProcessor(models.Model):
    process_number = models.IntegerField()

