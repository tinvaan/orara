from profiles.models import INTERESTS
from profiles.models import UserInterests


def match_percentage(user1, user2):
    if user1.username == user2.username:
        return 0.0
    else:
        match_count = 0
        for interest in user1.interests:
            if interest in user2.interest:
                match_count += 1
        return float(match_count/len(INTERESTS) * 100)