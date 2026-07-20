#!/usr/bin/env python3
"""Generate an accurate Bali map SVG from real GPS coordinates.

Projection: equirectangular, lng 114.35-115.80E -> x 60-940, lat 7.98-8.95S -> y 60-620.
Coastline points follow the real coast (Gilimanuk NW tip, straight-ish north coast,
east cape past Amed, south coast, Bukit peninsula, west coast back up).
"""

def P(lng, lat):
    x = 60 + (lng - 114.35) * 606.9
    y = 60 + (lat - 7.98) * 577.3
    return (round(x, 1), round(y, 1))

# --- real coastline waypoints (clockwise from NW cape) ---
BALI = [P(*c) for c in [
    (114.43, 8.12),   # Prapat Agung / NW cape
    (114.52, 8.09), (114.65, 8.13),           # NW north coast
    (114.83, 8.15), (115.02, 8.16),           # Pemuteran, Lovina
    (115.10, 8.09), (115.20, 8.06), (115.33, 8.09),  # Singaraja, Tejakula
    (115.45, 8.16), (115.59, 8.26),           # NE coast, Tulamben
    (115.66, 8.33),                           # Amed
    (115.71, 8.44),                           # east cape (Seraya)
    (115.63, 8.47), (115.57, 8.51),           # Ujung, Candidasa
    (115.51, 8.53), (115.40, 8.58),           # Padang Bai, Kusamba
    (115.31, 8.62), (115.26, 8.69),           # Sanur coast
    (115.225, 8.74),                          # Benoa / isthmus east
    (115.235, 8.79),                          # Nusa Dua
    (115.20, 8.85), (115.13, 8.85),           # Bukit south coast
    (115.07, 8.82),                           # Uluwatu cape
    (115.10, 8.78), (115.15, 8.775),          # Bukit west, Jimbaran bay
    (115.165, 8.74),                          # isthmus west (airport)
    (115.14, 8.68),                           # Kuta-Canggu coast
    (115.09, 8.62),                           # Tanah Lot
    (114.95, 8.55), (114.80, 8.47),           # SW coast, Medewi
    (114.60, 8.39), (114.47, 8.25),           # Negara coast, back to Gilimanuk
]]

PENIDA = [P(*c) for c in [
    (115.44, 8.68), (115.53, 8.665), (115.61, 8.70),
    (115.60, 8.78), (115.50, 8.77), (115.45, 8.73),
]]

def smooth_closed(pts):
    """Quadratic-through-midpoints closed path."""
    n = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f"M {mids[-1][0]:.1f} {mids[-1][1]:.1f} "
    for i in range(n):
        d += f"Q {pts[i][0]:.1f} {pts[i][1]:.1f} {mids[i][0]:.1f} {mids[i][1]:.1f} "
    return d + "Z"

# --- landmarks: (name, lng, lat, zone, label anchor, label dx, dy) ---
MARKS = [
    ("DPS Airport",  115.167, 8.744, "airport", "start",  16, -6),
    ("Canggu",       115.13,  8.65,  "south",   "end",   -11, -4),
    ("Seminyak",     115.16,  8.69,  "south",   "end",   -11,  4),
    ("Sanur",        115.26,  8.68,  "south",   "start",  12, -2),
    ("Tanah Lot",    115.087, 8.621, "south",   "end",   -11, -4),
    ("Uluwatu",      115.085, 8.829, "south",   "end",   -11,  8),
    ("Nusa Dua",     115.23,  8.80,  "south",   "start",  12,  6),
    ("Ubud",         115.263, 8.507, "center",  "start",  12,  4, True),
    ("Tegalalang",   115.28,  8.43,  "center",  "end",   -11, -2),
    ("Jatiluwih",    115.13,  8.37,  "north",   "end",   -11,  0),
    ("Ulun Danu",    115.167, 8.275, "north",   "start",  12,  2),
    ("Munduk",       115.067, 8.266, "north",   "end",   -11,  0),
    ("Sekumpul",     115.186, 8.174, "north",   "start",  12, -4),
    ("Lovina",       115.02,  8.16,  "north",   "middle",  0, -14),
    ("Sidemen",      115.43,  8.47,  "east",    "end",   -11,  8),
    ("Tirta Gangga", 115.587, 8.412, "east",    "end",   -11, 16),
    ("Lempuyang",    115.63,  8.39,  "east",    "start",  13, -4),
    ("Amed",         115.66,  8.34,  "east",    "start",  13, -4),
    ("West Bali National Park", 114.50, 8.12, "west", "middle", 0, 22),
]

ZCOL = {"south": "#e8c98a", "center": "#a5e8b0", "north": "#8ed6c8",
        "east": "#e8a54b", "west": "#c9b8e8", "airport": "#25d366"}

AIRPORT = P(115.167, 8.744)
UBUD = P(115.263, 8.507)
ULUWATU = P(115.085, 8.829)
ULUN = P(115.167, 8.275)
TG = P(115.587, 8.412)
SANUR = P(115.26, 8.68)
KELINGKING = P(115.47, 8.75)
BATUR = P(115.375, 8.242)
AGUNG = P(115.507, 8.343)

def volcano(cx, cy, s):
    return f'<path d="M{cx-s} {cy+s*0.7} L{cx} {cy-s} L{cx+s} {cy+s*0.7} Z" fill="#123c2c"/>'

svg = []
svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" font-family="\'Plus Jakarta Sans\',\'Segoe UI\',sans-serif">')
svg.append('''<defs>
  <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#12555c"/><stop offset="1" stop-color="#0b3a46"/>
  </linearGradient>
  <linearGradient id="land" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4d9d68"/><stop offset="0.55" stop-color="#2f7d4f"/><stop offset="1" stop-color="#1f6244"/>
  </linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#04211a" flood-opacity="0.45"/>
  </filter>
</defs>''')
svg.append('<rect width="1000" height="640" fill="url(#sea)"/>')
svg.append('''<g stroke="#7fc9c0" stroke-width="1.5" opacity="0.28" stroke-linecap="round">
  <path d="M60 560 H100"/><path d="M905 560 H945"/><path d="M120 500 H150"/><path d="M900 470 H935"/>
</g>''')

svg.append(f'<g filter="url(#soft)">')
svg.append(f'<path d="{smooth_closed(BALI)}" fill="url(#land)" stroke="#e8c98a" stroke-width="3.5"/>')
svg.append(f'<path d="{smooth_closed(PENIDA)}" fill="url(#land)" stroke="#e8c98a" stroke-width="3"/>')
svg.append('</g>')

# volcanoes
svg.append(volcano(*BATUR, 26))
svg.append(volcano(*AGUNG, 34))
svg.append(f'<text x="{BATUR[0]}" y="{BATUR[1]-34}" font-size="14" fill="#cfe8d8" text-anchor="middle" font-style="italic">Mt Batur</text>')
svg.append(f'<text x="{AGUNG[0]}" y="{AGUNG[1]-44}" font-size="14" fill="#cfe8d8" text-anchor="middle" font-style="italic">Mt Agung</text>')

# routes from airport
ax, ay = AIRPORT
svg.append(f'''<g fill="none" stroke="#f2d795" stroke-width="3" stroke-dasharray="9 8" stroke-linecap="round" opacity="0.85">
  <path d="M{ax} {ay} Q {ax+22} {(ay+UBUD[1])/2} {UBUD[0]} {UBUD[1]}"/>
  <path d="M{ax} {ay} Q {ax-2} {ay+34} {ULUWATU[0]+10} {ULUWATU[1]-4}"/>
  <path d="M{ax} {ay} Q {SANUR[0]+40} {SANUR[1]-10} {(SANUR[0]+TG[0])/2} {(SANUR[1]+TG[1])/2-30} T {TG[0]} {TG[1]}"/>
  <path d="M{ax} {ay-14} Q {ULUN[0]-40} {(ay+ULUN[1])/2} {ULUN[0]} {ULUN[1]}"/>
  <path d="M{SANUR[0]} {SANUR[1]} Q {(SANUR[0]+KELINGKING[0])/2} {(SANUR[1]+KELINGKING[1])/2+16} {KELINGKING[0]} {KELINGKING[1]}"/>
</g>''')

# markers + labels
for m in MARKS:
    name, lng, lat, zone, anchor, dx, dy = m[:7]
    big = len(m) > 7
    x, y = P(lng, lat)
    col = ZCOL[zone]
    if zone == "airport":
        svg.append(f'<g transform="translate({x} {y})"><circle r="13" fill="{col}" stroke="#0e3b2e" stroke-width="3"/>'
                   f'<text y="5" font-size="13" text-anchor="middle" fill="#0e3b2e" font-weight="800">✈</text></g>')
        svg.append(f'<text x="{x+dx}" y="{y+dy}" font-size="16" fill="#fff" font-weight="800">{name}</text>')
    else:
        r = 8 if big else 7
        fs = 17 if big else 15
        fw = 800 if big else 700
        svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#0e3b2e" stroke-width="2"/>')
        svg.append(f'<text x="{x+dx}" y="{y+dy+5}" font-size="{fs}" fill="#fff" font-weight="{fw}" text-anchor="{anchor}"'
                   f' style="paint-order:stroke" stroke="#0b3a3a" stroke-width="3" stroke-opacity="0.45">{name}</text>')

# Nusa Penida
kx, ky = KELINGKING
svg.append(f'<circle cx="{kx}" cy="{ky}" r="7" fill="#e8c98a" stroke="#0e3b2e" stroke-width="2"/>')
pc = P(115.525, 8.73)
svg.append(f'<text x="{pc[0]}" y="{pc[1]+48}" font-size="15" fill="#fff" font-weight="700" text-anchor="middle">Nusa Penida</text>')
mid = ((SANUR[0]+kx)/2, (SANUR[1]+ky)/2)
svg.append(f'<text x="{mid[0]-14}" y="{mid[1]+34}" font-size="13" fill="#cfe8d8" font-style="italic">⛵ boat day trip</text>')

# title, compass, legend
svg.append('<text x="64" y="88" font-size="34" fill="#fff" font-weight="800" font-family="Georgia,serif">BALI</text>')
svg.append('<text x="64" y="114" font-size="15" fill="#e8c98a" font-weight="700" letter-spacing="2">PRIVATE DRIVER COVERAGE</text>')
svg.append('''<g transform="translate(930 92)" stroke="#e8c98a" fill="none" stroke-width="2.6">
  <circle r="24"/><path d="M0 -16 L7 9 L0 4 L-7 9 Z" fill="#e8c98a" stroke="none"/>
  <text x="0" y="-32" font-size="14" fill="#e8c98a" text-anchor="middle" stroke="none" font-weight="700">N</text>
</g>''')
svg.append('''<g transform="translate(64 478)">
  <rect width="296" height="132" rx="16" fill="#0e3b2e" opacity="0.9" stroke="#e8c98a" stroke-width="1.5"/>
  <text x="20" y="31" font-size="15" fill="#e8c98a" font-weight="800">⏱ FROM DPS AIRPORT (approx.)</text>
  <text x="20" y="58" font-size="14.5" fill="#faf7f0">Seminyak 30 min · Uluwatu 45 min</text>
  <text x="20" y="82" font-size="14.5" fill="#faf7f0">Ubud 1 h 15 · Ulun Danu 2 h</text>
  <text x="20" y="106" font-size="14.5" fill="#faf7f0">Amed 2 h 30 · Lovina 3 h</text>
</g>''')
svg.append('</svg>')

open('/home/user/personal-driver-bali/assets/img/bali-map.svg', 'w').write('\n'.join(svg) + '\n')
print('map written,', len('\n'.join(svg)), 'bytes')
