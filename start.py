import asyncio
from shazamio import Shazam
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
import argparse

parser = argparse.ArgumentParser(description='use: python3 start.py -p /path/to/mp3 -f file.mp3')
parser.add_argument('-f', dest='file', type=str)
parser.add_argument('-p', dest='path', type=str)
args = parser.parse_args()

async def main():
    shazam = Shazam()
    out = await shazam.recognize_song(args.path+'/'+args.file)
    #print(out)
    debug = open("debug.log", 'a')
    debug.write(str(out))
    debug.close()
    subtitle=out['track']['subtitle']
    title=out['track']['title']
    albomm=out['track']['sections'][0]['metadata'][0]['text']
    yearr=out['track']['sections'][0]['metadata'][2]['text']
    genress=out['track']['genres']['primary']
    print(f"Subtitle: {subtitle}  \nTitle: {title}  \nAlbom: {albomm}  \nYear: {yearr} \nGenress: {genress} \n")
    mp3 = MP3File(args.path+'/'+args.file)
    mp3.set_version(VERSION_2)
    mp3.artist=str(subtitle)
    mp3.song=str(title)
    mp3.albom=str(albomm)
    mp3.year=str(yearr)
    mp3.genre=str(genress)
    mp3.save()
    os.rename(args.path+'/'+args.file,subtitle+"-"+title+".mp3")
    print(f"{subtitle} - {title}.mp3 - ready!")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())