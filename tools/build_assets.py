"""Builds the profile banner and the project cards (SVG) used in README.md.

Edit PROJECTS below and run:  python3 tools/build_assets.py
Everything is plain SVG, so GitHub shows it without any external service.
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

COLORS = {"ai": "#a78bfa", "auto": "#2dd4bf", "edu": "#60a5fa"}

PROJECTS = [
    # slug, category key, label, badge, title, description, tags
    ("sar-super-resolution", "ai", "DEEP LEARNING · REMOTE SENSING", "IEEE-style report",
     "SAR Super-Resolution (SRGAN)",
     "Upscales satellite radar (SAR) images with a custom SRGAN: SSIM + L1 loss, TTUR and a STAC data pipeline.",
     ["TensorFlow", "Keras", "GANs", "Computer vision"]),
    ("machine-vision", "ai", "MACHINE VISION · CNN", "Group project",
     "Galactic Credit Scanner",
     "Real-time conveyor scanner that detects, classifies and sums credit chips: OpenCV + a CNN trained on 2,800 images.",
     ["OpenCV", "TensorFlow", "CNN", "Python"]),
    ("multi-agent-llm", "ai", "AGENTIC AI · MANUFACTURING", "Grade A",
     "Multi-Agent Factory + LLM",
     "Agents negotiate, re-route around failures and accept plain-language orders through a local Llama 3 model.",
     ["CMAS", "Python", "Ollama", "Modbus TCP"]),
    ("ml-lesson", "ai", "MACHINE LEARNING · AI ETHICS", "Lesson design",
     "ML Lesson: Social Anxiety Data",
     "Linear regression on a real social-anxiety dataset (MSE, MAE, R²) and a classroom discussion of AI ethics.",
     ["scikit-learn", "pandas", "Seaborn", "Jupyter"]),
    ("agv-hmi", "auto", "PLC · INDUSTRIAL HMI", "Live demo",
     "AGV Operator HMI",
     "Operator HMI that mirrors a TwinCAT IEC 61131-3 PLC state machine: dispatch, emergency stop and reset-to-home.",
     ["TwinCAT", "Structured Text", "IEC 61131-3", "State machine"]),
    ("tbot-control", "auto", "CONTROL SYSTEMS · ROBOTICS", "Live demo",
     "T-Bot Modelling & Control",
     "Lagrangian model of a CoreXY robot: 19-state state-space model, RGA decoupling and P/PI/PID tuning.",
     ["MATLAB", "Simulink", "Control theory", "Robotics"]),
    ("rtd-daq", "auto", "MECHATRONICS · SENSORS", "Grade A",
     "RTD Data Acquisition System",
     "Temperature DAQ for surgical robotics: Wheatstone bridge, amplifier and ADC in Simulink with live Arduino input.",
     ["Simulink", "Arduino", "MATLAB", "PID"]),
    ("crane-modbus", "auto", "INDUSTRIAL AUTOMATION · PYTHON", "Modbus TCP",
     "Crane Pick-and-Place Controller",
     "Python controller that executes a JSON pick-and-place plan on a simulated industrial crane over Modbus TCP.",
     ["Python", "pymodbus", "Modbus TCP", "JSON"]),
    ("physics-labs", "edu", "AI IN EDUCATION · PHYSICS", "Örebro University",
     "Physics Labs × Machine Learning",
     "Colab labs where students model their own measurements, plus labs from an Örebro University collaboration.",
     ["Python", "Colab", "NumPy", "Physics"]),
    ("gy25-labs", "edu", "AI IN EDUCATION · GY25", "Swedish curriculum",
     "Gy25 Physics & Math AI Labs",
     "Jupyter/Colab labs that bring machine learning into Physics 1–2 and Mathematics 4 under Sweden's Gy25 curriculum.",
     ["Python", "Colab", "Regression", "Gy25"]),
]


def text_w(s, size, k=0.56):
    """Rough rendered width of a string (px) for wrapping and pill sizing."""
    narrow = sum(1 for c in s if c in "ilI.,:;'|!() ·-")
    wide = sum(1 for c in s if c in "mwMW@%")
    return size * (k * (len(s) - narrow - wide) + 0.3 * narrow + 0.85 * wide)


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(trial, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def card(slug, cat, label, badge, title, desc, tags):
    c = COLORS[cat]
    W, H, P = 600, 226, 30
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">',
           f'<title>{escape(title)}</title>',
           '<defs>',
           f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f1c30"/><stop offset="1" stop-color="#0b1424"/></linearGradient>',
           f'<radialGradient id="glow" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{c}" stop-opacity="0.22"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>',
           f'<clipPath id="r"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
           '</defs>',
           '<g clip-path="url(#r)">',
           f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
           f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
           f'<rect width="5" height="{H}" fill="{c}"/>',
           '</g>',
           f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="15.5" fill="none" stroke="#24364f" stroke-width="1.5"/>',
           f'<text x="{P}" y="40" font-family="{MONO}" font-size="13" letter-spacing="1.6" fill="{c}" font-weight="600">{escape(label)}</text>']
    if badge:
        bw = text_w(badge, 12.5, 0.6) + 22
        bx = W - P - bw
        out += [f'<rect x="{bx:.1f}" y="23" width="{bw:.1f}" height="24" rx="12" fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-opacity="0.55"/>',
                f'<text x="{bx + bw/2:.1f}" y="39.5" text-anchor="middle" font-family="{FONT}" font-size="12.5" font-weight="600" fill="{c}">{escape(badge)}</text>']
    out.append(f'<text x="{P}" y="82" font-family="{FONT}" font-size="27" font-weight="700" fill="#f3f7fc">{escape(title)}</text>')
    assert text_w(title, 27, 0.62) <= W - 2 * P, f"title too long: {title}"
    lines = wrap(desc, 18, W - 2 * P)
    assert len(lines) <= 2, f"description too long ({len(lines)} lines): {desc}"
    for i, line in enumerate(lines):
        out.append(f'<text x="{P}" y="{116 + i*25}" font-family="{FONT}" font-size="18" fill="#b4c3d6">{escape(line)}</text>')
    x = P
    for t in tags:
        tw = text_w(t, 14, 0.6) + 22
        assert x + tw <= W - P - 30, f"tags do not fit: {tags}"
        out += [f'<rect x="{x:.1f}" y="{H-58}" width="{tw:.1f}" height="28" rx="7" fill="#15243a" stroke="#2b405e"/>',
                f'<text x="{x + tw/2:.1f}" y="{H-39}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="#d3e2f4">{escape(t)}</text>']
        x += tw + 8
    out.append(f'<text x="{W-P}" y="{H-38}" text-anchor="end" font-family="{FONT}" font-size="22" fill="{c}">↗</text>')
    out.append('</svg>')
    (ASSETS / "cards").mkdir(parents=True, exist_ok=True)
    (ASSETS / "cards" / f"{slug}.svg").write_text("\n".join(out), encoding="utf-8")


def gear_path(cx, cy, r_out, r_in, teeth):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r = r_out if (i % 4) in (1, 2) else r_in
        pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def banner():
    W, H = 1280, 320
    # physics: a sine wave
    wave = " ".join(f"{'M' if i == 0 else 'L'}{730 + i*3:.1f},{170 - 34*math.sin(i*3/22):.1f}" for i in range(0, 61))
    layers = [(960, [118, 170, 222]), (1045, [96, 142, 198, 244]), (1130, [146, 196])]
    gear_c = (1205, 170)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Gabriel Danho — AI and Automation Engineer">',
         '<title>Gabriel Danho — AI &amp; Automation Engineer</title>',
         '<defs>',
         '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#091322"/><stop offset="0.55" stop-color="#10223d"/><stop offset="1" stop-color="#0b3243"/></linearGradient>',
         '<radialGradient id="glow" cx="0.78" cy="0.5" r="0.45"><stop offset="0" stop-color="#2a74b8" stop-opacity="0.35"/><stop offset="1" stop-color="#2a74b8" stop-opacity="0"/></radialGradient>',
         '<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#2a74b8"/><stop offset="0.5" stop-color="#a78bfa"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient>',
         '<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#ffffff" fill-opacity="0.07"/></pattern>',
         f'<clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>',
         '</defs>',
         '<g clip-path="url(#r)">',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
         f'<rect y="{H-6}" width="{W}" height="6" fill="url(#bar)"/>',
         '</g>',
         # text
         f'<text x="72" y="96" font-family="{MONO}" font-size="17" letter-spacing="3" fill="#7cc4ff">HELLO, I’M</text>',
         f'<text x="70" y="166" font-family="{FONT}" font-size="66" font-weight="800" fill="#ffffff" letter-spacing="-1">Gabriel Danho</text>',
         f'<text x="72" y="214" font-family="{FONT}" font-size="31" font-weight="600" fill="#8fd3ff">AI &amp; Automation Engineer</text>',
         f'<text x="72" y="256" font-family="{FONT}" font-size="19" fill="#b4c4d8">Physicist · Licensed teacher · M.Sc. AI &amp; Automation</text>',
         # physics wave (flowing)
         f'<path d="{wave}" fill="none" stroke="#7cc4ff" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 7">',
         '<animate attributeName="stroke-dashoffset" from="0" to="-34" dur="1.6s" repeatCount="indefinite"/></path>']
    # network edges
    first = layers[0]
    for y in first[1]:
        o.append(f'<line x1="910" y1="170" x2="{first[0]}" y2="{y}" stroke="#4d6a92" stroke-opacity="0.55" stroke-width="1.5"/>')
    for (x1, ys1), (x2, ys2) in zip(layers, layers[1:]):
        for a in ys1:
            for b in ys2:
                o.append(f'<line x1="{x1}" y1="{a}" x2="{x2}" y2="{b}" stroke="#4d6a92" stroke-opacity="0.5" stroke-width="1.3"/>')
    for y in layers[-1][1]:
        o.append(f'<line x1="{layers[-1][0]}" y1="{y}" x2="{gear_c[0]-30}" y2="170" stroke="#4d6a92" stroke-opacity="0.55" stroke-width="1.5"/>')
    o.append('<line x1="907" y1="170" x2="912" y2="170" stroke="#7cc4ff" stroke-width="3"/>')
    # nodes (pulsing)
    k = 0
    for x, ys in layers:
        for y in ys:
            o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#0b1526" stroke="#a78bfa" stroke-width="2.6">'
                     f'<animate attributeName="stroke-opacity" values="1;0.35;1" dur="2.4s" begin="{k*0.25:.2f}s" repeatCount="indefinite"/></circle>')
            k += 1
    # automation gear (rotating)
    gx, gy = gear_c
    o += [f'<g><path d="{gear_path(gx, gy, 30, 23, 9)}" fill="#0b1526" stroke="#2dd4bf" stroke-width="2.6" stroke-linejoin="round"/>',
          f'<circle cx="{gx}" cy="{gy}" r="8" fill="none" stroke="#2dd4bf" stroke-width="2.6"/>',
          f'<animateTransform attributeName="transform" type="rotate" from="0 {gx} {gy}" to="360 {gx} {gy}" dur="9s" repeatCount="indefinite"/></g>']
    # a signal travelling physics -> AI -> automation
    o.append('<circle r="4.5" fill="#ffffff"><animateMotion dur="3.2s" repeatCount="indefinite" '
             'path="M730,170 L910,170 L960,118 L1045,142 L1130,196 L1175,170"/>'
             '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="3.2s" repeatCount="indefinite"/></circle>')
    for x, lab, col in [(820, "physics", "#7cc4ff"), (1045, "AI", "#a78bfa"), (1205, "automation", "#2dd4bf")]:
        o.append(f'<text x="{x}" y="290" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{col}" fill-opacity="0.85">{lab}</text>')
    o.append('</svg>')
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "banner.svg").write_text("\n".join(o), encoding="utf-8")


if __name__ == "__main__":
    banner()
    for p in PROJECTS:
        card(*p)
    print("built", len(PROJECTS), "cards + banner in", ASSETS)
