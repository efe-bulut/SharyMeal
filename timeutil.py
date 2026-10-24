from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ISO = '%Y-%m-%dT%H:%M:%SZ'
LOCAL_TZ = ZoneInfo('Europe/Nicosia')

def utc_now():
    return datetime.now(timezone.utc)

def to_iso(dt):
    return dt.astimezone(timezone.utc).strftime(ISO)

def utc_now_iso():
    return to_iso(utc_now())

def local_input_to_iso(text):
    # Formdan gelen '2026-10-30T14:00' (Nicosia saati) -> UTC ISO
    naive = datetime.strptime(text, '%Y-%m-%dT%H:%M')
    return to_iso(naive.replace(tzinfo=LOCAL_TZ))

def iso_to_local_display(iso):
    dt = datetime.strptime(iso, ISO).replace(tzinfo=timezone.utc)
    return dt.astimezone(LOCAL_TZ).strftime('%d.%m.%Y %H:%M')