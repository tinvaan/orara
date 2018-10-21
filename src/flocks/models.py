from django.db import models

from profiles.models import OraraUser


class OraraConnections(models.Model):
    user1 = models.ForeignKey(OraraUser, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(OraraUser, related_name="user2", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Connections"
        verbose_name_plural = "Connections"

    def __str__(self):
        return "'{}' - '{}'".format(self.user1, self.user2)


class UserBookmarks(models.Model):
    user = models.ForeignKey(OraraUser, related_name='users', on_delete=models.CASCADE)
    bookmark = models.ForeignKey(OraraUser, related_name='bookmark', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return "'{}' bookmarked '{}'".format(self.user, self.bookmark)
