from profiles.models import INTERESTS
from profiles.models import OraraUser, UserInterests
from events.models import EventCustomers
from flocks.models import OraraConnections, UserBookmarks


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
        return False
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
            if has_connection(user, obj):
                connections.append(item)
            elif item['username'] == user.username:
                # Don't show self
                pass
            else:
                others.append(item)
        except OraraUser.DoesNotExist:
            pass

    return connections, others
