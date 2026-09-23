"""Milestone 9 presentation, naming and localisation integration.

All generated visual/audio assets are deterministic original procedural work. No external
portrait, painting, flag, recording or game asset is embedded by this module.
A10 visual direction is implemented here: painted/canvas portrait and scene work,
engraved/cartographic focus and UI work, and restrained map-adjacent styling.
A11-A12 are implemented by later stacked passes.
"""
from __future__ import annotations
import hashlib
import math
import re
import struct
from pathlib import Path

from build_00_contracts import COUNTRIES

FOCUS_W, FOCUS_H = 95, 85
EVENT_W, EVENT_H = 474, 156
PORTRAIT_W, PORTRAIT_H = 156, 210
REGIMES = ("neutrality","democratic","communism","fascism")
FLAG_SIZES = (("",82,52),("medium/",41,26),("small/",10,7))

UNIT_DATA = {
"FRA": ("Corps d'Infanterie", ["Régiment de Picardie","Régiment de Navarre","Régiment de Champagne","Royal-Roussillon","Royal-Suédois"], ["Océan","Bretagne","Tonnant","Indomptable","Redoutable","Commerce de Marseille"]),
"ENG": ("Infantry Brigade", ["1st Foot Guards","Coldstream Guards","42nd Royal Highland Regiment","23rd Royal Welch Fusiliers","33rd Regiment of Foot"], ["Victory","Royal Sovereign","Britannia","Barfleur","Queen Charlotte","Temeraire"]),
"HAB": ("Infanteriekorps", ["Hoch- und Deutschmeister","Kaiser Regiment","De Ligne Regiment","Wallis Regiment","Grenz Infantry"], ["Theresia","Kaiser","Austria","Adler","Leopard"]),
"PRU": ("Armeekorps", ["Garde-Regiment","Regiment von Kleist","Regiment von Möllendorff","Regiment von Braunschweig","Husaren-Regiment"], ["König von Preußen","Borussia","Adler","Friedrich Wilhelm"]),
"RUS": ("Army Corps", ["Preobrazhensky Guards","Semyonovsky Guards","Izmailovsky Guards","Taurida Grenadiers","Don Cossack Host"], ["Rostislav","Saratov","Svyatoi Pavel","Evstafii","Pobedonosets"]),
"SPR": ("Cuerpo", ["Reales Guardias Españolas","Regimiento de Irlanda","Regimiento de Asturias","Regimiento de Sevilla","Regimiento de Valencia"], ["Santísima Trinidad","Santa Ana","San Ildefonso","San Juan Nepomuceno","Montañés"]),
"POR": ("Brigada", ["Regimento de Lippe","Regimento de Cascais","Regimento de Peniche","Regimento de Bragança"], ["Príncipe Real","Rainha de Portugal","Vasco da Gama","Medusa"]),
"TUR": ("Ordu", ["Kapıkulu Infantry","Janissary Orta","Rumelian Army","Anatolian Army","Sipahi Cavalry"], ["Bahr-i Zafer","Burc-u Zafer","Mesudiye","Selimiye"]),
"SWE": ("Brigad", ["Svea Livgarde","Uppland Regiment","Göta Regiment","Nylands Regiment","Livregementets Husarer"], ["Gustav III","Wasa","Dristigheten","Manligheten","Äran"]),
"DEN": ("Brigade", ["Danske Livregiment","Jyske Regiment","Norske Livregiment","Livgarden til Hest"], ["Christian VII","Danmark","Trekroner","Prindsesse Lovisa Augusta"]),
"POL": ("Dywizja", ["Gwardia Piesza Koronna","Dywizja Wielkopolska","Dywizja Małopolska","Dywizja Litewska","Brygada Kawalerii Narodowej"], []),
"NET": ("Brigade", ["Hollandse Regiment","Staatse Infanterie","Regiment Oranje","Friese Regiment"], ["Vrijheid","Staten-Generaal","De Ruyter","Brakel"]),
"SAR": ("Brigata", ["Reggimento Piemonte","Reggimento Sardegna","Reggimento Savoia","Cavalleria Savoia"], []),
"NAP": ("Brigata", ["Reggimento Reale Napoli","Reggimento Sicilia","Reggimento Calabria","Cavalleria Reale"], []),
"PAP": ("Brigata", ["Guardia Pontificia","Milizia di Roma","Milizia di Bologna"], []),
"VEN": ("Brigata", ["Fanteria Veneta","Schiavoni","Cavalleria Veneta","Milizia di Terraferma"], ["Fama","Eolo","Vittoria","Gloria Veneta"]),
"TUS": ("Brigata", ["Reggimento Toscano","Milizia Granducale","Guardia di Firenze"], []),
"BAV": ("Brigade", ["Kurfürstliches Infanterieregiment","Leibregiment","Bayerisches Kavallerieregiment"], []),
"SAX": ("Brigade", ["Kurfürstliches Infanterieregiment","Garde zu Fuß","Sächsische Kavallerie"], []),
"HAN": ("Brigade", ["Kurhannoversches Infanterieregiment","Garde-Regiment","Hannoversche Kavallerie"], []),
"WUR": ("Brigade", ["Herzogliches Infanterieregiment","Leibgarde","Württembergische Reiterei"], []),
"USA": ("Brigade", ["1st American Regiment","2nd Infantry Regiment","Legion of the United States","Virginia Militia"], ["Constitution","United States","Constellation","Chesapeake","Congress","President"]),
}

FLAVOUR = [
("FRA","The Pamphlet Stalls of Paris","Printers and booksellers can barely keep pace with the appetite for political argument. Pamphlets pass from hand to hand before the ink is dry.","Public opinion has become a force of its own."),
("ENG","Coffee-House Politics","Merchants, MPs and pamphleteers crowd London's coffee houses, turning war, credit and reform into arguments that last well after midnight.","The kingdom debates in public."),
("HAB","A Court of Many Languages","Petitions reach Vienna in German, Hungarian, Czech, Italian and the languages of the southern crownlands. Reform must travel through an empire of many political traditions.","Administration is diplomacy at home."),
("PRU","The Memory of Old Fritz","Every drill field still lives in the shadow of Frederick the Great. The question is whether imitation preserves his achievement or merely preserves his habits.","Tradition can inspire or imprison."),
("RUS","Winter at the Imperial Court","Behind the brilliance of the court lies a state spanning distances that turn every order into a logistical problem.","The empire is larger than its roads."),
("SPR","The Cádiz Merchants","Atlantic merchants petition the crown for security, predictable customs and protection from disruptions that can empty warehouses in a season.","The Atlantic monarchy depends on commerce."),
("POL","The Sejm in Session","Deputies argue over sovereignty, taxation and the survival of the Commonwealth while neighbouring courts follow every speech with interest.","Reform has become a question of survival."),
("SWE","Stockholm's Political Stage","Court, officers and estates all understand that Gustavian politics is performed before an attentive public as much as decided behind palace doors.","Every gesture acquires political meaning."),
("TUR","Reports from the European Embassies","Envoys return with translated drill manuals, diplomatic memoranda and uncomfortable comparisons. The Porte must decide what can be borrowed without surrendering authority.","Knowledge itself becomes political."),
("VEN","An Evening on the Riva","Merchants and patricians watch ships enter the lagoon beneath the old symbols of the Republic, wondering how long neutrality can insulate Venice from continental upheaval.","The Serenissima measures the changing wind."),
("POR","The Lisbon Waterfront","Convoys, naval stores and colonial correspondence crowd the quays. Portugal's security remains inseparable from the Atlantic.","The sea is the kingdom's strategic depth."),
("USA","The First Cabinet Debates","The new federal government is still inventing the habits by which constitutional language becomes everyday administration.","A republic becomes a government."),
]

def _seed(label):
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8],"little")

def _slug(value):
    value=value.encode("ascii","ignore").decode().upper()
    value=re.sub(r"[^A-Z0-9]+","_",value).strip("_")
    return value[:72] or "UNKNOWN"

def _shade(rgb, delta):
    return tuple(max(0,min(255,c+delta)) for c in rgb)

def _mix(a,b,t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

def tga(width,height,pixel):
    header=struct.pack("<BBBHHBHHHHBB",0,0,2,0,0,0,0,0,width,height,24,32)
    data=bytearray()
    for y in range(height):
        for x in range(width):
            r,g,b=pixel(x,y)
            data.extend((b&255,g&255,r&255))
    return header+bytes(data)

def dds(width,height,pixel):
    flags=0x100F
    pf=struct.pack("<IIIIIIII",32,0x41,0,32,0x00FF0000,0x0000FF00,0x000000FF,0xFF000000)
    header=struct.pack("<I",124)+struct.pack("<IIIIII",flags,height,width,width*4,0,0)+b"\0"*44+pf+struct.pack("<IIIII",0x1000,0,0,0,0)
    data=bytearray()
    for y in range(height):
        for x in range(width):
            r,g,b=pixel(x,y)
            data.extend((b&255,g&255,r&255,255))
    return b"DDS "+header+bytes(data)

def art_pixel(label,kind,width,height):
    """A10 hybrid period language: painted scenes/portraits, engraved UI/focus art."""
    n=_seed(label)
    base=(((n>>8)&127)+55,((n>>24)&127)+45,((n>>40)&127)+35)
    base=tuple(min(180,max(38,int(c))) for c in base)
    canvas=(205,190,153)
    paper=(214,201,169)
    ink=(42,35,29)
    sepia=(104,75,48)
    gold=(164,126,58)
    def pixel(x,y):
        nx=x/max(1,width-1); ny=y/max(1,height-1)
        border=max(2,min(width,height)//20)

        # Portraits, event scenes and loadings use soft canvas-like tonal modelling.
        if kind in ("portrait","event","loading","bookmark"):
            wash=.20+.26*ny+.05*math.sin((x+(n&31))/max(1,width)*math.pi*3)
            bg=_mix(canvas,base,max(.08,min(.62,wash)))
            brush=((x*11+y*7+(n&255))%19)-9
            c=_shade(bg,brush//4)
        else:
            # Focuses and UI use light paper, sepia ink and engraved cross-hatching.
            grain=((x*17+y*31+(n&255))%23)-11
            c=_shade(_mix(paper,base,.13),grain//4)
            hatch=((x+2*y+(n&15))%13==0) or ((2*x-y+((n>>5)&15))%17==0)
            if hatch:
                c=_mix(c,sepia,.22)

        if x<border or x>=width-border or y<border or y>=height-border:
            return _mix(ink,gold,.22)

        if kind=="portrait":
            cx=width//2; head_y=int(height*.34); rr=int(min(width,height)*.16)
            face=(139,111,85)
            shadow=_mix(ink,base,.22)
            if (x-cx)**2+(y-head_y)**2 < rr*rr:
                light=max(0,min(1,(cx+rr-x)/(2*rr)))
                return _mix(face,(210,176,132),.28*light)
            shoulder_y=int(height*.58)
            if y>shoulder_y and abs(x-cx) < int((y-shoulder_y)*.65+width*.18):
                return shadow
            if ((n>>3)&1) and head_y-rr//2<y<head_y and abs(x-cx)<rr+8:
                return _mix(ink,gold,.12)

        elif kind=="focus":
            cx=width//2; cy=height//2
            radius=min(width,height)//4
            if abs(x-cx)<max(1,width//32) or abs(y-cy)<max(1,height//32):
                return sepia
            dist=(x-cx)**2+(y-cy)**2
            if radius*radius*.72 < dist < radius*radius:
                return ink
            if dist < radius*radius*.7 and ((x-y+n)%6)<2:
                return _mix(sepia,base,.28)

        elif kind=="event":
            horizon=int(height*.62)
            sky=_mix((189,177,151),base,.20)
            if y<horizon:
                c=_mix(c,sky,.42)
            else:
                c=_mix(c,_mix(ink,base,.30),.58)
            for k in range(5):
                px=int(width*(.15+.17*k))+((n>>(k*3))&15)-7
                roof=int(height*(.38+(.04*(k%2))))
                if abs(x-px)<width//20 and y>roof:
                    return _mix(base,ink,.38)
                if abs(x-px)<width//28 and roof-height//9<y<=roof:
                    return _mix(gold,canvas,.18)

        elif kind=="loading":
            horizon=int(height*.58)
            if y>horizon:
                c=_mix(base,ink,.46)
            ridge=int(height*(.43+.06*math.sin((x+(n&127))/max(1,width)*8)))
            if abs(y-ridge)<max(2,height//120):
                return _mix(ink,sepia,.15)
            sunx=int(width*.72); suny=int(height*.28); sr=max(8,height//14)
            if (x-sunx)**2+(y-suny)**2<sr*sr:
                return _mix(gold,(236,215,166),.48)

        elif kind=="bookmark":
            if x>width*.58 and y<height*.72:
                return _mix(base,gold,.15)
            if abs(y-height*.64)<3:
                return sepia

        elif kind in ("ui","cartography"):
            # Fine cartographic grid/engraving, intentionally understated.
            major=max(12,min(width,height)//4)
            minor=max(6,major//3)
            if x%major==0 or y%major==0:
                return _mix(sepia,ink,.22)
            if x%minor==0 or y%minor==0:
                return _mix(c,sepia,.34)
            if kind=="ui" and (x-width/2)**2+(y-height/2)**2 < (min(width,height)*.31)**2:
                return _mix(c,gold,.18)
        return c
    return pixel
def flag_pixel(tag,base,variant,width,height):
    n=_seed(tag+"|"+variant)
    accent={"neutrality":(177,139,63),"democratic":(223,218,192),"communism":(158,45,45),"fascism":(42,57,89),"default":_shade(base,45)}[variant]
    dark=_mix(base,(20,20,20),.45)
    pattern=n%4
    def pixel(x,y):
        nx=x/max(1,width-1); ny=y/max(1,height-1)
        if pattern==0:
            c=base if nx<.5 else accent
        elif pattern==1:
            c=accent if .34<ny<.66 else base
        elif pattern==2:
            c=accent if abs(nx-.5)<.12 or abs(ny-.5)<.15 else base
        else:
            c=accent if nx+ny<.9 else base
        if x<max(1,width//30) or y<max(1,height//30):
            c=dark
        return c
    return pixel

def wav_float(label,duration=1.2,rate=44100):
    n=_seed(label); frames=bytearray()
    for i in range(int(duration*rate)):
        t=i/rate
        if "cannon" in label:
            value=.55*math.sin(2*math.pi*55*t)*math.exp(-4.5*t)+.14*math.sin(2*math.pi*113*t)*math.exp(-7*t)
        elif "crowd" in label:
            value=.10*math.sin(2*math.pi*(170+(n%90))*t)+.07*math.sin(2*math.pi*263*t)+.05*math.sin(2*math.pi*337*t)
            value*=min(1,t/.15)*min(1,(duration-t)/.25)
        else:
            value=.24*math.sin(2*math.pi*660*t)*math.exp(-2.4*t)+.16*math.sin(2*math.pi*880*t)*math.exp(-3*t)
        value=max(-.9,min(.9,value))
        frames.extend(struct.pack("<ff",value,value))
    block=8; byte_rate=rate*block
    fmt=struct.pack("<HHIIHH",3,2,rate,byte_rate,block,32)
    return b"RIFF"+struct.pack("<I",4+(8+len(fmt))+(8+len(frames)))+b"WAVEfmt "+struct.pack("<I",len(fmt))+fmt+b"data"+struct.pack("<I",len(frames))+bytes(frames)

def _country_rows():
    rows=[]
    for row in COUNTRIES.splitlines():
        tag,filename,name,colour=row.split("|")
        rows.append((tag,filename,name,tuple(map(int,colour.split()))))
    return rows

def _division_names():
    parts=[]
    for tag,(fallback,names,ships) in UNIT_DATA.items():
        safe=[n.replace('"',"'") for n in names]
        ordered=" ".join(f'{i+1} = {{ "{name}" }}' for i,name in enumerate(safe))
        parts.append(f'{tag}_NAP_INF = {{ name = "{fallback}s" for_countries = {{ {tag} }} can_use = {{ always = yes }} division_types = {{ "line_infantry" "light_infantry" "grenadier" "guard_infantry" "militia" }} fallback_name = "%d {fallback}" ordered = {{ {ordered} }} }}')
        parts.append(f'{tag}_NAP_CAV = {{ name = "Mounted Formations" for_countries = {{ {tag} }} can_use = {{ always = yes }} division_types = {{ "light_cavalry" "dragoon" "heavy_cavalry" "lancer" "irregular_cavalry" }} fallback_name = "%d Cavalry Brigade" }}')
    return "\n".join(parts)+"\n"

def _ship_names():
    parts=[]
    for tag,(_,_,ships) in UNIT_DATA.items():
        if not ships: continue
        unique=" ".join('"'+s.replace('"',"'")+'"' for s in ships)
        parts.append(f'{tag}_NAP_SAIL = {{ name = "Historical Sailing Warships" for_countries = {{ {tag} }} type = ship ship_types = {{ ship_of_the_line_hull frigate_hull sloop_hull bomb_ketch_hull fireship_hull }} fallback_name = "Warship %d" unique = {{ {unique} }} }}')
    return "\n".join(parts)+"\n"

def _flavour_events():
    events=["add_namespace = nap_flavour"]
    loc=["\ufeffl_english:"]
    for i,(tag,title,desc,option) in enumerate(FLAVOUR,1):
        events.append(f'''country_event = {{
 id = nap_flavour.{i}
 title = nap_flavour.{i}.t
 desc = nap_flavour.{i}.d
 picture = GFX_NAP_EVENT_01
 fire_only_once = yes
 trigger = {{ tag = {tag} }}
 mean_time_to_happen = {{ months = 8 }}
 option = {{ name = nap_flavour.{i}.a add_political_power = 15 scoped_sound_effect = "nap_dispatch_effect" }}
}}''')
        loc += [f' nap_flavour.{i}.t:0 "{title}"',f' nap_flavour.{i}.d:0 "{desc}"',f' nap_flavour.{i}.a:0 "{option}"']
    return "\n".join(events)+"\n","\n".join(loc)+"\n"

def build(root):
    out={}
    # Period-styled event pictures and loading screens.
    for i in range(1,13):
        out[f"gfx/event_pictures/nap_event_{i:02d}.tga"]=tga(EVENT_W,EVENT_H,art_pixel(f"event-{i}","event",EVENT_W,EVENT_H))
    for i in range(1,4):
        out[f"gfx/loadingscreens/load_napoleonic_{i}.dds"]=dds(960,540,art_pixel(f"loading-{i}","loading",960,540))
    out["gfx/interface/nap_ui_seal.tga"]=tga(96,96,art_pixel("ui-seal","ui",96,96))
    out["gfx/interface/nap_ui_divider.tga"]=tga(512,24,art_pixel("ui-divider","ui",512,24))
    out["gfx/interface/nap_map_legend.tga"]=tga(320,96,art_pixel("map-legend","cartography",320,96))
    out["gfx/interface/nap_cartographic_frame.tga"]=tga(512,64,art_pixel("cartographic-frame","cartography",512,64))
    out["sound/nap_dispatch.wav"]=wav_float("dispatch")
    out["sound/nap_crowd.wav"]=wav_float("crowd",1.6)
    out["sound/nap_cannon.wav"]=wav_float("cannon",1.8)
    out["sound/napoleonic.asset"]='''sound = { name = "nap_dispatch" file = "nap_dispatch.wav" always_load = yes volume = 0.55 }
sound = { name = "nap_crowd" file = "nap_crowd.wav" always_load = yes volume = 0.45 }
sound = { name = "nap_cannon" file = "nap_cannon.wav" always_load = yes volume = 0.60 }
soundeffect = { name = "nap_dispatch_effect" sounds = { sound = "nap_dispatch" } loop = no is3d = no max_audible = 1 max_audible_behaviour = fail volume = 0.65 }
soundeffect = { name = "nap_crowd_effect" sounds = { sound = "nap_crowd" } loop = no is3d = no max_audible = 1 max_audible_behaviour = fail volume = 0.55 }
soundeffect = { name = "nap_cannon_effect" sounds = { sound = "nap_cannon" } loop = no is3d = no max_audible = 1 max_audible_behaviour = fail volume = 0.60 }
'''
    out["common/units/names_divisions/napoleonic_names_divisions.txt"]=_division_names()
    out["common/units/names_ships/napoleonic_ship_names.txt"]=_ship_names()
    ev,loc=_flavour_events()
    out["events/10_flavour.txt"]=ev
    out["localisation/english/nap_flavour_l_english.yml"]=loc
    out["docs/asset-provenance.md"]="""# Asset provenance

All assets generated by \`content/build_70_presentation.py\` are original procedural output created for this repository.

- focus icons: deterministic engraved/cartographic compositions derived from internal focus IDs
- leader/commander portraits: original warm canvas-style portrait cards, not copies of historical paintings or photographs
- event pictures and loading screens: original painted/canvas-style period scenes
- bookmark art, map legend and UI pieces: restrained engraved/cartographic compositions
- default/regime flags: original heraldic placeholders derived from each country's palette
- event stingers: mathematically synthesised WAV files with no sampled recording

No external painting, photograph, commercial recording, font file or game asset is redistributed by this pass. A10's visual direction is implemented without copying historical artworks. Any future replacement asset must be recorded here with source and licence before merge.
"""
    out["docs/presentation.md"]="""# Milestone 9 presentation layer

The presentation pipeline gives every current focus a custom icon, every current scripted event a custom period-styled picture, and every inline political/military leader an original portrait card. It also supplies regime flags, three loading screens, 1789 bookmark art, UI ornaments, event stingers, historical division/corps naming groups, sailing-warship names and additional flavour events.

A10 is implemented as a hybrid period presentation: portraits, event scenes and loading screens use a warmer painted/canvas treatment; focus art and UI use engraved/cartographic linework; map-adjacent art stays understated rather than recolouring the strategic map. The treatment avoids modern gritty-WWII visual language while retaining stable gameplay IDs.

The event sound layer remains functional. The A11 stacked pass supplies the approved soundtrack policy.

English remains the authoritative localisation. The A12 stacked pass makes that a build invariant.
"""
    return out

def _paths(outputs,root,prefix,suffix):
    names={p for p in outputs if p.startswith(prefix) and p.endswith(suffix)}
    base=root/prefix
    if base.exists():
        for p in base.rglob("*"+suffix):
            names.add(p.relative_to(root).as_posix())
    return sorted(names)

def _text(outputs,root,path):
    value=outputs.get(path)
    if isinstance(value,str): return value
    p=root/path
    return p.read_text(encoding="utf-8-sig") if p.exists() else ""

def _blocks(text,pattern):
    spans=[]
    for m in re.finditer(pattern,text,re.M):
        start=m.start(); brace=text.find("{",m.start())
        if brace<0: continue
        depth=0; quote=False; esc=False
        for i in range(brace,len(text)):
            ch=text[i]
            if quote:
                if esc: esc=False
                elif ch=="\\": esc=True
                elif ch=='"': quote=False
                continue
            if ch=='"': quote=True
            elif ch=="{": depth+=1
            elif ch=="}":
                depth-=1
                if depth==0:
                    spans.append((start,i+1))
                    break
    return spans

def _patch_focuses(text,updates,interface):
    spans=_blocks(text,r"^\s*(?:focus|shared_focus)\s*=\s*\{")
    for start,end in reversed(spans):
        block=text[start:end]
        m=re.search(r"\bid\s*=\s*([A-Za-z0-9_]+)",block)
        if not m: continue
        fid=m.group(1); gfx="GFX_NAP_FOCUS_"+_slug(fid)
        if re.search(r"\bicon\s*=",block):
            block=re.sub(r"\bicon\s*=\s*[^\s}]+",f"icon = {gfx}",block,count=1)
        else:
            block=block[:m.end()]+f"\n icon = {gfx}"+block[m.end():]
        text=text[:start]+block+text[end:]
        path=f"gfx/interface/goals/{_slug(fid).lower()}.tga"
        if path not in updates:
            updates[path]=tga(FOCUS_W,FOCUS_H,art_pixel(fid,"focus",FOCUS_W,FOCUS_H))
            interface += [f'spriteType = {{ name = "{gfx}" texturefile = "{path}" }}',f'spriteType = {{ name = "{gfx}_shine" texturefile = "{path}" }}']
    return text

def _patch_events(text):
    spans=_blocks(text,r"^\s*(?:country_event|news_event)\s*=\s*\{")
    for start,end in reversed(spans):
        block=text[start:end]
        m=re.search(r"\bid\s*=\s*([A-Za-z0-9_.]+)",block)
        if not m: continue
        index=(_seed(m.group(1))%12)+1; gfx=f"GFX_NAP_EVENT_{index:02d}"
        if re.search(r"\bpicture\s*=",block):
            block=re.sub(r"\bpicture\s*=\s*[^\s}]+",f"picture = {gfx}",block,count=1)
        else:
            d=re.search(r"\bdesc\s*=\s*[^\n}]+",block)
            pos=d.end() if d else m.end()
            block=block[:pos]+f"\n picture = {gfx}"+block[pos:]
        text=text[:start]+block+text[end:]
    return text

def _patch_people(text,tag,updates,interface,people):
    spans=_blocks(text,r"\bcreate_(?:country_leader|field_marshal|corps_commander|navy_leader)\s*=\s*\{")
    for start,end in reversed(spans):
        block=text[start:end]
        m=re.search(r'\bname\s*=\s*"([^"]+)"',block)
        if not m: continue
        name=m.group(1); key=_slug(name)
        gfx="GFX_NAP_PORTRAIT_"+key
        if key not in people:
            people.add(key)
            path=f"gfx/leaders/NAP/{key.lower()}.tga"
            updates[path]=tga(PORTRAIT_W,PORTRAIT_H,art_pixel(name,"portrait",PORTRAIT_W,PORTRAIT_H))
            interface.append(f'spriteType = {{ name = "{gfx}" texturefile = "{path}" }}')
        active=re.search(r"(?m)^\s*picture\s*=",block)
        if active:
            block=re.sub(r'(?m)^\s*picture\s*=\s*[^\n]+',f'\tpicture = {gfx}',block,count=1)
        else:
            block=block[:m.end()]+f"\n\tpicture = {gfx}"+block[m.end():]
        text=text[:start]+block+text[end:]
    return text

def _patch_oob(text,tag):
    spans=_blocks(text,r"^\s*division_template\s*=\s*\{")
    for start,end in reversed(spans):
        block=text[start:end]
        if "division_names_group" in block: continue
        cavalry=any(tok in block for tok in ("light_cavalry","dragoon","heavy_cavalry","lancer","irregular_cavalry"))
        group=f"{tag}_NAP_CAV" if cavalry else f"{tag}_NAP_INF"
        m=re.search(r'\bname\s*=\s*"[^"]+"',block)
        if m: block=block[:m.end()]+f"\n\tdivision_names_group = {group}"+block[m.end():]
        text=text[:start]+block+text[end:]
    return text

def _polish_loc(text):
    text=text.replace("the the ","the ")
    text=text.replace("These balance values remain provisional.","")
    text=text.replace("Numeric balance remains provisional.","")
    text=text.replace("These balance values are provisional.","")
    text=text.replace("while preserving the bounded territorial rules of the mod.","while strengthening the institutions needed to sustain the chosen policy.")
    text=text.replace("This branch builds on the existing national path rather than overriding its government or territorial settlement.","The programme develops alongside the country's existing constitutional and diplomatic commitments.")
    text=re.sub(r'Advance the ([^.]+) programme\.',lambda m:"Develop the "+m.group(1)+" programme.",text)
    text=text.replace("placeholder","temporary")
    text=text.replace("Placeholder","Temporary")
    return text

def postprocess(outputs,root):
    updates={}; interface=['spriteTypes = {']
    # Shared event/UI sprites.
    for i in range(1,13):
        interface.append(f'spriteType = {{ name = "GFX_NAP_EVENT_{i:02d}" texturefile = "gfx/event_pictures/nap_event_{i:02d}.tga" }}')
    interface += [
        'spriteType = { name = "GFX_nap_ui_seal" texturefile = "gfx/interface/nap_ui_seal.tga" }',
        'spriteType = { name = "GFX_nap_ui_divider" texturefile = "gfx/interface/nap_ui_divider.tga" }',
        'spriteType = { name = "GFX_nap_map_legend" texturefile = "gfx/interface/nap_map_legend.tga" }',
        'spriteType = { name = "GFX_nap_cartographic_frame" texturefile = "gfx/interface/nap_cartographic_frame.tga" }',
    ]
    # Replace solid development flags with deterministic heraldic variants.
    for tag,filename,name,colour in _country_rows():
        for variant in ("default",)+REGIMES:
            suffix="" if variant=="default" else "_"+variant
            for folder,w,h in FLAG_SIZES:
                updates[f"gfx/flags/{folder}{tag}{suffix}.tga"]=tga(w,h,flag_pixel(tag,colour,variant,w,h))
    # Focus icons.
    for path in _paths(outputs,root,"common/national_focus",".txt"):
        text=_patch_focuses(_text(outputs,root,path),updates,interface)
        updates[path]=text
    # Events and people created by events.
    people=set()
    for path in _paths(outputs,root,"events",".txt"):
        text=_patch_events(_text(outputs,root,path))
        text=_patch_people(text,"NAP",updates,interface,people)
        updates[path]=text
    # Starting political and military portraits.
    for path in _paths(outputs,root,"history/countries",".txt"):
        tag=Path(path).name[:3]
        updates[path]=_patch_people(_text(outputs,root,path),tag,updates,interface,people)
    # Commanders sometimes get created by focus rewards.
    for path in _paths(outputs,root,"common/national_focus",".txt"):
        updates[path]=_patch_people(updates.get(path,_text(outputs,root,path)),"NAP",updates,interface,people)
    # Historical corps/division naming groups for current OOBs.
    for path in _paths(outputs,root,"history/units",".txt"):
        tag=Path(path).name[:3]
        if tag in UNIT_DATA:
            updates[path]=_patch_oob(_text(outputs,root,path),tag)
    # Better bookmark artwork.
    updates["gfx/interface/select_date_napoleonic.tga"]=tga(384,152,art_pixel("1789-bookmark","bookmark",384,152))
    # English cleanup, including retained localisation not previously generator-owned.
    loc_paths={p for p in outputs if p.startswith("localisation/english/") and p.endswith(".yml")}
    loc_root=root/"localisation/english"
    if loc_root.exists():
        for p in loc_root.rglob("*.yml"): loc_paths.add(p.relative_to(root).as_posix())
    for path in sorted(loc_paths):
        updates[path]=_polish_loc(_text(outputs,root,path))
    interface.append("}")
    updates["interface/nap_presentation.gfx"]="\n".join(interface)+"\n"
    suggestions=outputs.get("suggestions.md","")
    note='''

## Presentation follow-up

- A10 is implemented as the approved painted/engraved/cartographic hybrid without invasive strategic-map recolouring.
- Any historical-art replacement must be redistribution-safe and added to the provenance ledger.
- A11 and A12 are implemented in their own stacked passes.
'''
    if "## Presentation follow-up" not in suggestions: suggestions+=note
    updates["suggestions.md"]=suggestions
    return updates
