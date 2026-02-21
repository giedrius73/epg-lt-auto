import gzip
import xml.etree.ElementTree as ET

# Mapping: epg.one channel ID → your playlist IDs
mapping = {
    "3279": ["lrt.lt"],
    "3284": ["lrtplius.lt"],
    "3280": ["tv1.lt", "12004"],
    "3273": ["tv3.lt", "18007"],
    "4808": ["tv3plus.lt"],
    "6292": ["go3films.lt"],
    "3274": ["tv6.lt"],
    "3277": ["ltv7.lv"],
    "3370": ["lnk.lt", "6405"],
    "3268": ["btv.lt", "6398"],
    "3278": ["tv8.lt", "12005"],
    "3365": ["delfi.lt"],
    "3364": ["balticum.lt"],
    "4809": ["balticumauksinis.lt"],
    "4807": ["balticumplatinum.lt"],
    "9152": ["duo3.lt"],
    "3287": ["2tv.lt"],
    "3282": ["lrytas.lt", "12003"],
    "3286": ["infotv.lt"],
    "88029": ["etaplius.lt"],
    "2932": ["sport1.lt", "6367"],
    "3380": ["go3sport1.lt"],
    "3381": ["go3sport2.lt"],
    "8883": ["viasatkinoworld.lt"],
    "31447": ["viasatkinoworld.lt"],
    "31448": ["viasatkinoworld.lt"],
    "31449": ["viasatkinoworld.lt"],
    "1031": ["fx.lt"]
}

# Read original EPG
with gzip.open("epg2.xml.gz", "rb") as f:
    xml_data = f.read()

# Safety check: if file is empty or not XML
if len(xml_data) < 1000:
    print("ERROR: epg2.xml.gz is too small or invalid. Aborting.")
    with gzip.open("epg_su_filtru.xml.gz", "wb") as out:
        out.write(b"<tv></tv>")
    exit()

try:
    root = ET.fromstring(xml_data)
except ET.ParseError:
    print("ERROR: epg2.xml.gz is not valid XML. Aborting.")
    with gzip.open("epg_su_filtru.xml.gz", "wb") as out:
        out.write(b"<tv></tv>")
    exit()

new_root = ET.Element("tv")

# Filter channels
found_channels = 0
for channel in root.findall("channel"):
    epg_id = channel.get("id")
    if epg_id in mapping:
        found_channels += 1
        for playlist_id in mapping[epg_id]:
            new_channel = ET.SubElement(new_root, "channel", id=playlist_id)
            for child in channel:
                new_channel.append(child)

# Filter programmes
found_programmes = 0
for programme in root.findall("programme"):
    epg_id = programme.get("channel")
    if epg_id in mapping:
        found_programmes += 1
        for playlist_id in mapping[epg_id]:
            new_prog = ET.SubElement(
                new_root,
                "programme",
                start=programme.get("start"),
                stop=programme.get("stop"),
                channel=playlist_id
            )
            for child in programme:
                new_prog.append(child)

print(f"Filtered channels: {found_channels}")
print(f"Filtered programmes: {found_programmes}")

# Safety: if nothing found, do NOT produce empty EPG
if found_channels == 0:
    print("WARNING: No channels matched. Writing empty EPG safely.")
    with gzip.open("epg_su_filtru.xml.gz", "wb") as out:
        out.write(b"<tv></tv>")
    exit()

# Save filtered EPG
xml_bytes = ET.tostring(new_root, encoding="utf-8")
with gzip.open("epg_su_filtru.xml.gz", "wb") as f:
    f.write(xml_bytes)
