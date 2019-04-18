from profiles.models import INTERESTS
from profiles.models import OraraUser, UserInterests
from events.models import EventCustomers, EventInvites
from flocks.models import OraraConnections, UserBookmarks


def invites(user):
    all = EventInvites.objects.filter(user=user)
    return len(all)


def connections(user):
    left = OraraConnections.objects.filter(user1=user)
    right = OraraConnections.objects.filter(user2=user)
    return len(left) + len(right)


def match_percentage(user1, user2):
    if user1.username == user2.username:
        return 0.0
    else:
        match_count = 0
        for interest in user1.interests:
            if interest in user2.interest:
                match_count += 1
        return float(match_count/len(INTERESTS) * 100)


def get_customers(event):
    users = []
    for item in EventCustomers.objects.filter(event=event):
        users.append({
            'name': item.customer.name(),
            'status': item.customer.status,
            'area': item.customer.area,
            'phone': item.customer.phone
        })
    return users


def has_connection(user1, user2):
    try:
        OraraConnections.objects.get(user1=user1, user2=user2)
    except OraraConnections.DoesNotExist:
        return user1 == user2
    return True


def has_bookmark(user1, user2):
    try:
        UserBookmarks.objects.get(user=user1, bookmark=user2)
    except UserBookmarks.DoesNotExist:
        return False
    return True


def segregate(user, users):
    '''
    Divide a list of users into friends(connections) and strangers
    '''
    others = []
    connections = []

    for item in users:
        try:
            obj = OraraUser.objects.get(username=item['username'])
            if item['username'] == user.username:
                # Don't show self
                pass
            elif has_connection(user, obj):
                connections.append(item)
            else:
                others.append(item)
        except OraraUser.DoesNotExist:
            pass

    return connections, others


def nearby(user):
    users = []

    # Has the user registered any interests ?
    try:
        if UserInterests.objects.get(user=user):
            interests_known = True
    except UserInterests.DoesNotExist:
        interests_known = False

    # Filter by
    # 1) Location | TODO: Narrow down using lat/lon in next iteration
    # 2) Interests
    for user in OraraUser.objects.filter(area=user.area):
        # List all users in proximity if user's interest are not known
        if not interests_known:
            users.append({
                'username': user.username,
                'name': user.name(),
                'area': user.area,
                'bio': user.bio,
                'status': user.status,
                'college': user.college,
                'workplace': user.workplace,
                'photo': user.photo
            })
        else:
            # List users with matching interests
            try:
                interest = UserInterests.objects.get(user=user)
                if not match_percentage(interest.user, user) == 0:
                    users.append({
                        'username': user.username,
                        'name': user.name(),
                        'area': user.area,
                        'bio': user.bio,
                        'status': user.status,
                        'college': user.college,
                        'workplace': user.workplace,
                        'photo': user.photo
                    })
            except UserInterests.DoesNotExist:
                pass

    return users


def suggestions(user):
    suggested = []

    # Gather users in proximity
    users = nearby(user)

    # Filter users who are not connections
    for person in users:
        try:
            user1 = OraraUser.objects.get(username=user.username)
            user2 = OraraUser.objects.get(username=person['username'])
        except OraraUser.DoesNotExist:
            pass

        # Filter connections
        # TODO: Refactor ? There has to be a more efficient way
        try:
            OraraConnections.objects.get(user1=user1, user2=user2)
        except OraraConnections.DoesNotExist:
            try:
                OraraConnections.objects.get(user1=user2, user2=user1)
            except OraraConnections.DoesNotExist:
                suggested.append(person)

    return suggested
