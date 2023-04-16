import gpxpy
import pathlib
import datetime
import srtm4
from locationsharinglib import Service
from zoneinfo import ZoneInfo

cookies_file = '/home/user/chieltracker/google.com_cookies.txt'
google_email = 'mygooglemailforbots@gmail.com'
service = Service(cookies_file=cookies_file, authenticating_account=google_email)

gpxtrackfile = '/var/www/hiruventure.nl/chieltrack.gpx'

'''Time stuff'''
JapanTZ = ZoneInfo("Asia/Tokyo")
JapanDT = datetime.datetime.now(JapanTZ)
JapanFullDateStr = JapanDT.strftime('%d-%B')


if not pathlib.Path(gpxtrackfile).is_file():
    print("file does not exist, creating file")
    gpx = gpxpy.gpx.GPX()
    with open(gpxtrackfile, "w") as f:
        f.write(gpx.to_xml())

'''Decide if you need a new track'''
def begin_new_track(m_gpx):
    if len(m_gpx.tracks) > 0:
        if m_gpx.tracks[-1].name == JapanFullDateStr:
            print("Same track date, no new track needed")
            return False
    return True


def get_last_point(m_gxp_track):
    if len(m_gxp_track.segments) > 0:
        lastsegment = m_gxp_track.segments[-1]
        if len(lastsegment.points) > 0:
            return lastsegment.points[-1]

def create_point(m_person):
    pt = gpxpy.gpx.GPXTrackPoint(m_person.latitude, m_person.longitude, time=m_person.datetime)
    pt.elevation = float(srtm4.srtm4(m_person.longitude, m_person.latitude))
    pt.comment = f'Battery level: {m_person.battery_level}'
    pt.description = m_person.address
    return pt


gpx_file = open(gpxtrackfile, 'r')
gpx = gpxpy.parse(gpx_file)
gpx_file.close()


if begin_new_track(gpx):
    print("New date, so new track added")
    today_track = gpxpy.gpx.GPXTrack()
    today_track.name = JapanFullDateStr 
    today_segment = gpxpy.gpx.GPXTrackSegment()
    gpx.tracks.append(today_track)
    today_track.segments.append(today_segment) 


for person in service.get_all_people():
    if person.nickname == 'Chiel':
        newpoint = create_point(person)
        lastpoint= get_last_point(gpx.tracks[-1])
        if lastpoint is not None and lastpoint.latitude == newpoint.latitude:
            print("New point was identical to last point, skipping")
        else:
            print(f'{datetime.datetime.now()}: {person.address}')
            gpx.tracks[-1].segments[-1].points.append(newpoint)



with open(gpxtrackfile, "w") as f:
    f.write(gpx.to_xml())
