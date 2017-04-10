#!/usr/bin/env python3
"""
usage: emuparadise <system> <game>
       emuparadise --url=<url>
       emuparadise --search=<term>
       emuparadise --list-systems
       emuparadise (-h | --help)
       emuparadise --version

A tool for getting files from emuparadise
"""

import os, sys
from requests import get as rget
from ftplib import FTP, error_perm
from random import choice
from urllib.parse import urlparse
from docopt import docopt
from sys import exit

SERVER = choice(["50.7.92.186", "50.7.161.74", "50.7.136.26", "50.7.188.26", "50.7.161.234", "50.7.161.122"])
ALTSERVER = "198.16.64.50"

# Sega Saturn, Sony Playstation, Neo Geo (Arcade) not supported due to weird naming
SYSTEMS = {
    "Atari 2600": (ALTSERVER, "/Atari 2600/Games", "zip"),
    "Atari 5200": (ALTSERVER, "/Atari 5200/Roms", "zip"),
    "Atari 7800": (ALTSERVER, "/Atari 7800/Games", "zip"),
    "Atari Jaguar": (SERVER, "/Atari Jaguar", "zip"),
    "Bandai Playdia": (SERVER, "/bks/Bandai Playdia [TOSEC v2009-03-09]/Games", "zip"),
    "Neo-Geo CD": (SERVER, "/bks/101/SNK Neo-Geo CD/Games", "zip"),
    "Nintendo 64": (SERVER, "/Nintendo 64", "zip"),
    "Nintendo Entertainment System": (SERVER, "/may/120/NES Roms", "zip"),
    "Nintendo Famicom Disk System": (SERVER, "/Nintendo - Famicom Disk System", "zip"),
    "Nintendo Gamecube": (SERVER, "/Nintendo - Gamecube/USA", "zip"),
    "Nintendo Virtual Boy": (SERVER, "/Nintendo - Virtual Boy", "zip"),
    "Panasonic 3DO (3DO Interactive Multiplayer": (SERVER, "/may/120/3DO", "zip"),
    "PC Engine - TurboGrafx16": (SERVER, "/bks/101/tg16", "zip"),
    "PC Engine CD - Turbo Duo - TurboGrafx CD": (SERVER, "/pcecd/pce", "zip"),
    "PC-FX": (SERVER, "/bks/PC-FX", "zip"),
    "Philips CD-i": (SERVER, "/CD-i", "zip"),
    "Sega 32X": (SERVER, "/bks/94/245/32x", "zip"),
    "Sega CD": (SERVER, "/bks/101/SegaCD", "zip"),
    "Sega Dreamcast": (ALTSERVER, "/Dreamcast", "zip"),
    "Sega Genesis - Sega Megadrive": (ALTSERVER, "/may/120/Sega Genesis Roms", "zip"),
    "Sega Master System": (SERVER, "/may/120/Sega Master System", "zip"),
# Sega Saturn appends a tag to the filename /Saturn/Sega Saturn/Sonic R (U)(Saturn).zip
#   "Sega Saturn": (SERVER, "/Saturn/Sega Saturn", "zip"),
# Sony Playstation uses abnormal filenames, Crash Team Racing [U] >> /PSX-Redump/CTR - Crash Team Racing (USA).7z
#   "Sony Playstation": (ALTSERVER, "/PSX-Redump", "7z"),
    "Sony Playstation - Demos": (SERVER, "/may/2/Complete Sony Playstation NTSC-U Collection - Demos v0.93", "rar"),
    "Sony Playstation 2": (SERVER, "/Playstation2", "7z"),
    "Super Nintendo Entertainment System (SNES)": (SERVER, "/may/120/Super Nintendo Roms", "zip"),
# MAME uses legacy filenames /NewAdditions/MAMEnon/mslug6.zip
#   "M.A.M.E. - Multiple Arcade Machine Emulator": (ALTSERVER, "/NewAdditions/MAMEnon", "zip"),
# Neo Geo arcade roms use legacy filenames /bks/101/Neo-Geo/mslug5.zip
#   "Neo Geo": (SERVER, "/bks/101/Neo-Geo", "zip"),
    "Sega NAOMI": (SERVER, "/bks/94/Naomi", "zip"),
    "Atari Lynx": (ALTSERVER, "/Atari - Lynx", "zip"),
    "Bandai Wonderswan": (ALTSERVER, "/may/120/WonderswanMono", "ws"),
    "Bandai Wonderswan Color": (ALTSERVER, "/may/120/WonderswanColor", "wsc"),
    "Neo Geo Pocket - Neo Geo Pocket Color (NGPx)": (SERVER, "/may/120/NGPx", "7z"),
# NDS uses scene numbering /Nintendo DS/Nintendo DS 3501 - 3600/3541 - Pokemon Platinum Version (US)(XenoPhobia).7z
#   "Nintendo DS": (SERVER, "/Nintendo DS/Nintendo DS {} - {}", "7z"),
# GBA uses release filenames and scene numbering /Gameboy Advance Roms/GBA Roms 1901 - 2000/1986 - Pokemon Emerald (U)(TrashMan).zip
#   "Nintendo Game Boy Advance": (SERVER, "/Gameboy Advance Roms/GBA Roms {} - {}", "zip"),
    "Nintendo Game Boy": (SERVER, "/may/120/Gameboy Roms", "zip"),
    "Nokia N-Gage": (SERVER, "/bks/101/Nokia - N-Gage", "zip"),
    "Sega Game Gear": (SERVER, "/may/120/Sega Game Gear", "zip"),
# PSP uses release filenames /pspisos/Kanon_JPN_PROPER_PSP-iND.rar
#   "Sony Playstation Portable": (SERVER, "/pspisos", "rar"),
# PSX2PSP uses release filenames /PSX2PSP/Crash Bandicoot [U] [SCUS-94900].rar
#   "PSX on PSP": (SERVER, "/PSX2PSP", "rar"),
    "Sony PocketStation": (SERVER, "/PocketStation/Converted Roms", "bin"),
    "Abandonware": (ALTSERVER, "/may/1/DOSCollection", "zip"),
    "DOS": (ALTSERVER, "/may/1/DOSCollection", "zip"),
    "Acorn Archimedes": (ALTSERVER, "/may/Acorn/Archimedes/Games", "zip"),
# Acorn BBC Micro and Acorn Electron have a tag at the end of the filename that is included in the path
# e.g Sphinx Adventure (198x)(Acornsoft) [UEF] >> [UEF]/Sphinx Adventure (198x)(Acornsoft).zip
#   "Acorn BBC Micro": (ALTSERVER, "/may/Acorn/BBC Micro/Games/{tag}", "zip"),
#   "Acorn Electron": (SERVER, "/may/Acorn/Electron/Games/{tag}", "zip"),
# Amiga titles are downloaded from static.emuparadise.me, TODO separate handler needed
# Amiga CD titles use release filenames /bks/Amiga-CD/Civilization (1994)(Acid Software)(en-de)[!].zip
#   "Amiga CD": (ALTSERVER, "/bks/Amiga-CD", "zip"),
# Amiga CD32 titles use release filenames /bks/101/AmigaCD32/Zool - Ninja of the 'Nth' Dimension (1993)(Gremlin)[!].zip
#   "Amiga CD32": (SERVER, "/bks/101/AmigaCD32", "zip"),
    "Amstrad CPC": (ALTSERVER, "/bks/CPC", "dsk"),
    "Apple ][": (SERVER, "/bks/101/Apple2/roms", "zip"),
    "Apple II": (SERVER, "/bks/101/Apple2/roms", "zip"),
    "Apple 2": (SERVER, "/bks/101/Apple2/roms", "zip"),
    "Atari 800": (SERVER, "/may/Atari800", "zip"),
    "Atari ST": (SERVER, "/may/AtariST/Games/[STX]", "zip"),
    "Commodore 64 Preservation Project": (SERVER, "/bks/94/Commodore 64 PP", "zip"),
    "Commodore 64 (Tapes)": (SERVER, "/bks/94/Commodore 64 Tapes", "zip"),
    "ScummVM": (SERVER, "/bks/new/ScummVM/Working", "zip"),
    "Sharp X68000": (ALTSERVER, "/bks/101/Sharp X68000", "zip"),
    "ZX Spectrum (Tapes)": (SERVER, "/bks/94/Sinclair/Roms/ZX Spectrum - Games - [TAP]", "tap"),
    "ZX Spectrum (Z80)": (ALTSERVER, "/bks/94/Sinclair/Roms/ZX Spectrum - Games - [Z80]", "z80")
}

class NotFound(Exception):
    pass

class AlreadyExists(Exception):
    pass

def get(system, game):
    if not system in SYSTEMS:
        raise NotFound
    server, dir, ext = SYSTEMS[system]
    filename = "{}.{}".format(game, ext)
    if os.path.exists(os.path.join(system, filename)):
        raise AlreadyExists
    ftp = FTP(server)
    _loginresp = ftp.login("Anonymous", "chrome@example.com")
    _cwdresp = ftp.cwd(dir)
    try:
        size = ftp.size(filename)
    except error_perm:
        return 1
    print("Downloading {} ({} bytes)".format(filename, size))
    try:
        os.mkdir(system)
    except FileExistsError:
        pass
    with open(os.path.join(system, filename), "wb") as f:
        ftp.retrbinary("RETR {}".format(filename), f.write)
    return 0

def search(term, p=False):
    results = rget("https://www.emuparadise.me/roms/autocomplete.php", params={"term": term}).json()
    if p and results:
        for n, result in enumerate(results):
            if result["category"] == "Search for":
                print("{n}. {category} {label}".format(n=n, **result))
            elif result["category"] == "ROMs, ISOs, Games":
                print("{n}. [{system}] {label}".format(n=n, **result))
    return results

def resolve(gid):
    return rget("https://www.emuparadise.me/roms/roms.php", params={"gid": gid}, allow_redirects=False).headers["Location"]

def parse_url(emup_url):
    path = urlparse(emup_url).path.replace("_", " ")[1:]
    system, game, _ = path.split("/")
    system = " ".join(system.split()[:-1])
    return system, game

def main():
    args = docopt(__doc__, version="emuparadise 0.0.1")
    if args["--list-systems"]:
        print("\n".join(sorted(SYSTEMS.keys())))
    elif args["--url"]:
        return get(*parse_url(args["--url"]))
    elif args["--search"]:
        results = search(args["--search"], p=True)
        result = None
        while result is None:
            try:
                index = int(input('enter your choice: '))
                result = results[index]
            except ValueError:
                print("Try again. Has to be a number.")
            except IndexError:
                print("Check your input. Ctrl-C to back out")
            if result["category"] == "Search for":
                results = search(result["label"], p=True)
                result = None
        return get(*parse_url(resolve(result["gid"])))
    elif args["<system>"] and args["<game>"]:
        return get(args["<system>"], args["<game>"])
    else:
        return 99

if __name__ == "__main__":
    exit(main())
