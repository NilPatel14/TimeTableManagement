from django import template

register = template.Library()

@register.filter
def get_timetable(timetable_entries, time_slot, day):
    return timetable_entries.filter(time_slot=time_slot, day=day).first()