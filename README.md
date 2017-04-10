py-emuparadise
==============

    pip3 install git+https://github.com/blha303/py-emuparadise

    $ emuparadise --url='https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Super_Mario_Bros._(Japan,_USA)/57098'
    Downloading Super Mario Bros. (Japan, USA).zip (31515 bytes)
    
    $ emuparadise --search=banjo
    0. [N64] Banjo-Kazooie (USA)
    1. [N64] Banjo-Tooie (USA)
    <snip>
    7. Search for banjo tooie
    enter your choice: 7
    0. [N64] Banjo-Tooie (USA)
    1. [N64] Banjo-Tooie (Europe) (En,Fr,De,Es)
    2. [N64] Banjo-Tooie (Australia)
    3. Search for banjo tooie
    <snip>
    enter your choice: 1
    Downloading Banjo-Tooie (Europe) (En,Fr,De,Es).zip (32889205 bytes)
    
    $ emuparadise 'Sega Master System' 'Sonic The Hedgehog (USA, Europe)'
    Downloading Sonic The Hedgehog (USA, Europe).zip (146866 bytes)
    
    $ ls *
    Nintendo 64:
    Banjo-Tooie (Europe) (En,Fr,De,Es).zip
    
    Nintendo Entertainment System:
    Super Mario Bros. (Japan, USA).zip
    
    Sega Master System:
    Sonic The Hedgehog (USA, Europe).zip
