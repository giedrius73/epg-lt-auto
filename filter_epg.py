import gzip
import xml.etree.ElementTree as ET

mapping = {
    "lrt.lt": ["3279"],
    "lrtplius.lt": ["3284"],
    "tv1.lt": ["3280", "12004"],
    "tv3.lt": ["3273", "18007"],
    "tv3plus.lt": ["4808"],
    "go3films.lt": ["6292"],
    "tv6.lt": ["3274"],
    "ltv7.lv": ["3277"],
    "lnk.lt": ["3370", "6405"],
    "btv.lt": ["3268", "6398"],
    "tv8.lt": ["3278", "12005"],
    "delfi.lt": ["3365"],
    "balticum.lt": ["3364"],
    "balticumauksinis.lt": ["4809"],
    "balticumplatinum.lt": ["4807"],
    "duo3.lt": ["9152"],
    "2tv.lt": ["3287"],
    "lrytas.lt": ["3282", "12003"],
    "infotv.lt": ["3286"],
    "etaplius.lt": ["88029"],
    "sport1.lt": ["2932", "6367"],
    "go3sport1.lt": ["3380"],
    "go3sport2.lt": ["3381"],
    "viasatkinoworld.lt": ["8883", "31447", "31448", "31449"],
    "fx.lt": ["1031"]
}

with gzip.open("epg2.xml.gz", "rb") as f:
    xml_data = f.read()

root = ET.fromstring(xml_data)
new_root = ET.Element("tv")

for channel in root.findall("channel"):
    epg_id = channel.get("id")
    if epg_id in mapping:
        for playlist_id in mapping[epg_id]:
            new_channel = ET.SubElement(new_root, "channel", id=playlist_id)
            new_channel.extend(channel)

for programme in root.findall("programme"):
    epg_id = programme.get("channel")
    if epg_id in mapping:
        for playlist_id in mapping[epg_id]:
            new_prog = ET.SubElement(
                new_root,
                "programme",
                start=programme.get("start"),
                stop=programme.get("stop"),
                channel=playlist_id
            )
            new_prog.extend(programme)

xml_bytes = ET.tostring(new_root, encoding="utf-8")
with gzip.open("epg_su_filtru.xml.gz", "wb") as f:
    f.write(xml_bytes)