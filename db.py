from models import TelegramGroup, GroupMember
from constants import NO_SHEET

def validate_database_group(func):
    def inner(update, context):
        group = get_db_group(update.message.chat_id)
        if group.sheet_url:
            return func(update, context)
        else:
            update.message.reply_text(NO_SHEET)
    return inner


def create_db_group(group_id):
    group = TelegramGroup(group_id=group_id)
    group.save()


def get_db_group(group_id):
    try:
        return TelegramGroup.objects.get(group_id=group_id)
    except TelegramGroup.DoesNotExist:
        return None


def update_group_sheet(group_id, sheet_url):
    group = get_db_group(group_id)
    group.update(sheet_url=sheet_url)
    group.save()


def add_group_member(group_id, member):
    group_member = GroupMember(user_id=member.id, username=member.username)
    group = get_db_group(group_id)
    group.update(push__members=group_member)
    group.save()


def remove_group_member(group_id, member):
    group_member = GroupMember(user_id=member.id, username=member.username)
    group = get_db_group(group_id)
    group.update(pull__members=group_member)
    group.save()