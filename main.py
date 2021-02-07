#!/usr/bin/env python3
# coding=utf-8
import os
import io
from pygti.gti import GTI, Auth
import asyncio
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import datetime
import requests
import subprocess
from pytz import timezone
global font_station; font_station = ImageFont.truetype(font = 'fonts/Arial Bold.ttf', size = 55)
global font_station_direction; font_station_direction = ImageFont.truetype(font = 'fonts/Arial.ttf', size = 30)
global icon_cache; icon_cache = {}


global font_text; font_text = ImageFont.truetype(font = 'fonts/Arial.ttf', size = 45)
#global font_text; font_text = ImageFont.load_default()


GTI_USER = None
GTI_PASS = None

LINE_OFFSET = 100
PADDING_LEFT = 150

DISPLAY_WIDTH = 1872
DISPLAY_HEIGT = 1404

try:
    from dotenv import load_dotenv

    load_dotenv()

    GTI_USER = os.getenv("GTI_USER")
    GTI_PASS = os.getenv("GTI_PASS")
except ImportError:
    pass

PRIO_1_JARRESTRASSE = {
    "station": {
        "name":"Jarrestraße (Kampnagel)",
        "id":"Master:70031",
        "city":"Hamburg",
        "type":"STATION"
    },
    "filter":[
        {"serviceID":"HHA-B:17_HHA-B","stationIDs":["Master:70030"]},
        {"serviceID":"HHA-B:172_HHA-B","stationIDs":["Master:70030"]},
        {"serviceID":"HHA-B:173_HHA-B","stationIDs":["Master:70030"]}
    ],
    "time": {"date": "heute", "time": "jetzt"},
    "maxList": 5,
    "maxTimeOffset": 360,
    "useRealtime": True,
}

PRIO_1_GERTIGSTRASSE = {
    "station": {
        "name":"Gertigstraße",
        "id":"Master:70005",
        "city":"Hamburg",
        "type":"STATION"
    },
    "filter":[
        {"serviceID":"HHA-B:6_HHA-B","stationIDs":["Master:70004"]},
        {"serviceID":"HHA-B:17_HHA-B","stationIDs":["Master:70004"]},
        {"serviceID":"HHA-B:606_HHA-B","stationIDs":["Master:70004"]}
    ],
    "time": {"date": "heute", "time": "jetzt"},
    "maxList": 5,
    "maxTimeOffset": 360,
    "useRealtime": True,
}


async def main():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, GTI_USER, GTI_PASS)

        gti = GTI(auth)
        while True:
            print(datetime.datetime.now())
            print("Request PRIO_1 (Jarrestraße --> Barmbek, Gertigstraße --> HBF)")
            dl_jarrestrasse = await gti.departureList(PRIO_1_JARRESTRASSE)
            dl_gertigstrasse = await gti.departureList(PRIO_1_GERTIGSTRASSE)
            #dl = {'returnCode': 'OK', 'time': {'date': '18.01.2021', 'time': '15:38'}, 'departures': [
            # {'line': {'name': '6', 'direction': 'Auf dem Sande (Speicherstadt)', 'origin': 'U Borgweg', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Großraumgelenkbus'},
            #  'id': 'HHA-B:6_HHA-B'}, 'timeOffset': 1, 'serviceId': 66385, 'station': {'combinedName': 'Gertigstraße', 'id': 'Master:70005'}}, {'line': {'name': '173', 'direction': 'Am Stühm-Süd', 'origin': 'Mundsburger Brücke', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Stadtbus', 'model': 'Solobus'}, 'id': 'HHA-B:173_HHA-B'}, 'timeOffset': 4, 'serviceId': 52119, 'station': {'combinedName': 'Jarrestraße (Kampnagel)', 'id': 'Master:70031'}}, {'line': {'name': '17', 'direction': 'U Feldstraße', 'origin': 'Karlshöhe', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Gelenkbus'}, 'id': 'HHA-B:17_HHA-B'}, 'timeOffset': 5, 'serviceId': 106172, 'station': {'combinedName': 'Gertigstraße', 'id': 'Master:70005'}}, {'line': {'name': '17', 'direction': 'U Berne (Berner Heerweg)', 'origin': 'U Feldstraße', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Niederflur Metrobus'}, 'id': 'HHA-B:17_HHA-B'}, 'timeOffset': 8, 'serviceId': 106272, 'station': {'combinedName': 'Jarrestraße (Kampnagel)', 'id': 'Master:70031'}}, {'line': {'name': '173', 'direction': 'Am Stühm-Süd', 'origin': 'Mundsburger Brücke', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Stadtbus', 'model': 'Solobus'}, 'id': 'HHA-B:173_HHA-B'}, 'timeOffset': 11, 'serviceId': 52120, 'station': {'combinedName': 'Jarrestraße (Kampnagel)', 'id': 'Master:70031'}}, {'line': {'name': '6', 'direction': 'Auf dem Sande (Speicherstadt)', 'origin': 'U Borgweg', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Großraumgelenkbus'}, 'id': 'HHA-B:6_HHA-B'}, 'timeOffset': 11, 'serviceId': 66388, 'station': {'combinedName': 'Gertigstraße', 'id': 'Master:70005'}}, {'line': {'name': '17', 'direction': 'U Feldstraße', 'origin': 'U Berne (Berner Heerweg)', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Gelenkbus'}, 'id': 'HHA-B:17_HHA-B'}, 'timeOffset': 15, 'serviceId': 106444, 'station': {'combinedName': 'Gertigstraße', 'id': 'Master:70005'}}, {'line': {'name': '172', 'direction': 'Lentersweg', 'origin': 'Mundsburger Brücke', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Stadtbus', 'model': 'Schnellbus'}, 'id': 'HHA-B:172_HHA-B'}, 'timeOffset': 18, 'delay': 0, 'serviceId': 52558, 'station': {'combinedName': 'Jarrestraße (Kampnagel)', 'id': 'Master:70031'}}, {'line': {'name': '17', 'direction': 'U Berne (Berner Heerweg)', 'origin': 'U Feldstraße', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Gelenkbus'}, 'id': 'HHA-B:17_HHA-B'}, 'timeOffset': 18, 'delay': 0, 'serviceId': 106273, 'station': {'combinedName': 'Jarrestraße (Kampnagel)', 'id': 'Master:70031'}}, {'line': {'name': '6', 'direction': 'Auf dem Sande (Speicherstadt)', 'origin': 'U Borgweg', 'type': {'simpleType': 'BUS', 'shortInfo': 'Bus', 'longInfo': 'Niederflur Metrobus', 'model': 'Großraumgelenkbus'}, 'id': 'HHA-B:6_HHA-B'}, 'timeOffset': 21, 'serviceId': 66391, 'station': {'combinedName': 'Gertigstraße', 'id': 'Master:70005'}}]}
            #print(dl)
            drawResult(dl_jarrestrasse, dl_gertigstrasse)
            print(f"finished at: {datetime.datetime.now()}")
            await asyncio.sleep(60 - datetime.datetime.now().second)

        

def drawResult(result_jarrestrasse, result_gertigstrasse):
    # create draw with background base
    image = Image.open('HVV Basescreen.bmp')
    draw = ImageDraw.Draw(image)

    offset = 100
    draw.text((PADDING_LEFT - 50,offset), 'Jarrestraße (Kampnagel)', font = font_station, anchor='lb')
    head_length = draw.textlength('Jarrestraße (Kampnagel)', font = font_station)
    draw.text((PADDING_LEFT - 30 + head_length,offset), 'in Richtung Barmbek', font = font_station_direction, anchor='lb')

    draw.text((DISPLAY_WIDTH - 100,offset), datetime.datetime.now(timezone("Europe/Berlin")).strftime("%H:%M"), anchor='rb', font = font_station, fill=0)


    offset += 50
    drawDepartures(draw, result_jarrestrasse["departures"], offset, image)

    offset = (DISPLAY_HEIGT / 2) + 75
    draw.text((PADDING_LEFT - 50,offset), 'Gertigstraße', font = font_station, anchor='lb')
    head_length = draw.textlength('Gertigstraße', font = font_station)
    draw.text((PADDING_LEFT - 30 + head_length,offset), 'in Richtung Hauptbahnhof', font = font_station_direction, anchor='lb')

    offset += 50
    drawDepartures(draw, result_gertigstrasse["departures"], offset, image)

    image.save("Output.bmp")
    #to draw the image call subprocess
    #subprocess.run(["sudo","./IT8951/IT8951", "0", "0", "Output.bmp"])
    return

def drawDepartures(draw, departures, offset, image):
    for departure in departures:
        line = departure["line"]
        image.paste(getIcon(line["id"]), (PADDING_LEFT, int(offset  )))
        draw.bitmap
        #draw.text((PADDING_LEFT,offset), line["name"], font = font_text, fill=0)
        draw.text((PADDING_LEFT+200,offset), line["direction"], font = font_text, fill=0)
        timeOffset = departure["timeOffset"]
        if "delay" in departure:
            timeOffset += int(departure["delay"] / 60)
        draw.text((DISPLAY_WIDTH - 100,offset), createTimeOffsetText(timeOffset, "delay" in departure), anchor='rt', font = font_text, fill=0)
        draw.line([(0,offset + 80),(DISPLAY_WIDTH, offset + 80)], width=2, fill=200)
        offset += 110

def createTimeOffsetText(timeOffset, hasDelay):        
    if timeOffset == 0:
        return f"{'(verspätet) ' if hasDelay else ''} sofort"
    elif timeOffset > 0:
        return f"{'(verspätet) ' if hasDelay else ''} in {str(timeOffset)} min"
    else:
        return f"{'(verspätet) ' if hasDelay else ''} vor {str(timeOffset * -1)} min"
def getIcon(busId):
    if busId not in icon_cache:
        response = requests.get("https://www.geofox.de/icon_service/line?height=50&lineKey=" + busId, stream= True)
        icon_with_transparency = Image.open(io.BytesIO(response.content))
        white_bg = Image.new('RGBA', icon_with_transparency.size, (255,255,255))
        icon_white_background = Image.alpha_composite(white_bg, icon_with_transparency)
        icon_cache[busId] = icon_white_background

    return icon_cache[busId]



asyncio.run(main())
