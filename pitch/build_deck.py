#!/usr/bin/env python3
"""Build the RehabLens Conrad Challenge pitch deck.

Run:  python3 build_deck.py
Output: RehabLens_Pitch_Deck.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# ---------------- Design system ----------------
NAVY   = RGBColor(0x0F, 0x17, 0x2A)
NAVY2  = RGBColor(0x1E, 0x29, 0x3B)
TEAL   = RGBColor(0x0D, 0x94, 0x88)
TEAL2  = RGBColor(0x14, 0xB8, 0xA6)
TEAL_SOFT = RGBColor(0xCC, 0xFB, 0xF1)
ORANGE = RGBColor(0xF9, 0x73, 0x16)
INK    = RGBColor(0x0F, 0x17, 0x2A)
MUTED  = RGBColor(0x64, 0x74, 0x8B)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT  = RGBColor(0xF1, 0xF5, 0xF9)
LINE   = RGBColor(0xE2, 0xE8, 0xF0)
GOLD   = RGBColor(0xF5, 0x9E, 0x0B)

FONT = "Calibri"
SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(1)
    sp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    return sp


def text(s, x, y, w, h, runs, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, line_spacing=1.0, space_after=0):
    """runs: str, or list of paragraphs; each paragraph is str or list of (txt, dict) runs."""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(runs, str):
        runs = [runs]
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if space_after:
            p.space_after = Pt(space_after)
        if isinstance(para, str):
            para = [(para, {})]
        elif isinstance(para, tuple):
            para = [para]
        for txt, style in para:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.size = Pt(style.get("size", size))
            f.bold = style.get("bold", bold)
            f.italic = style.get("italic", False)
            f.color.rgb = style.get("color", color)
            f.name = style.get("font", FONT)
    return tb


def kicker(s, label, x=Inches(0.7), y=Inches(0.42)):
    text(s, x, y, Inches(9), Inches(0.4), label.upper(), size=13, color=TEAL, bold=True)


def title(s, label, x=Inches(0.7), y=Inches(0.78), w=Inches(11.9), size=32):
    text(s, x, y, w, Inches(0.9), label, size=size, color=NAVY, bold=True)


def rule(s, y=Inches(1.62)):
    rect(s, Inches(0.72), y, Inches(1.5), Pt(3), fill=TEAL)


def footer(s, n):
    text(s, Inches(0.7), Inches(7.08), Inches(6), Inches(0.3), "RehabLens · Conrad Challenge", size=10, color=MUTED)
    text(s, Inches(12.0), Inches(7.08), Inches(0.8), Inches(0.3), str(n), size=10, color=MUTED, align=PP_ALIGN.RIGHT)


def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt


def card(s, x, y, w, h, fill=LIGHT, line=LINE, radius=0.08):
    return rect(s, x, y, w, h, fill=fill, line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)


def table(s, x, y, w, rows_data, col_widths, header_fill=NAVY, header_color=WHITE,
          row_h=0.42, header_h=0.5, size=13, header_size=13, first_col_bold=True,
          row_fills=None, aligns=None):
    rows, cols = len(rows_data), len(rows_data[0])
    gt = s.shapes.add_table(rows, cols, x, y, w, Inches(header_h + row_h * (rows - 1)))
    tbl = gt.table
    tbl.first_row = False
    tbl.horz_banding = False
    for c, cw in enumerate(col_widths):
        tbl.columns[c].width = Inches(cw)
    tbl.rows[0].height = Inches(header_h)
    for r in range(1, rows):
        tbl.rows[r].height = Inches(row_h)
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            elif row_fills:
                cell.fill.fore_color.rgb = row_fills[(r - 1) % len(row_fills)]
            else:
                cell.fill.fore_color.rgb = WHITE if r % 2 else LIGHT
            p = cell.text_frame.paragraphs[0]
            p.alignment = (aligns[c] if aligns else PP_ALIGN.LEFT)
            run = p.add_run()
            run.text = str(rows_data[r][c])
            f = run.font
            f.size = Pt(header_size if r == 0 else size)
            f.name = FONT
            f.bold = (r == 0) or (c == 0 and first_col_bold)
            f.color.rgb = header_color if r == 0 else INK
    return tbl


def chip(s, x, y, w, h, label, fill=TEAL_SOFT, color=TEAL, size=14, bold=True):
    c = rect(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tf = c.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FONT
    return c


# ================================================================
# 1 — TITLE
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, Inches(4.6), SW, Inches(0.06), fill=TEAL2)
text(s, Inches(0.9), Inches(1.5), Inches(11.5), Inches(0.6), "CONRAD CHALLENGE  ·  HEALTH & NUTRITION",
     size=16, color=TEAL2, bold=True)
text(s, Inches(0.9), Inches(2.05), Inches(11.5), Inches(1.6), "RehabLens", size=88, color=WHITE, bold=True)
text(s, Inches(0.9), Inches(3.55), Inches(11.5), Inches(0.8),
     "Your physical therapist's eyes at home.", size=30, color=RGBColor(0x99, 0xF6, 0xE4))
text(s, Inches(0.9), Inches(4.9), Inches(11.5), Inches(0.9),
     "AI form-coach that scores home exercise video against the therapist's expert reference —\n"
     "live, on any phone, with no wearables.", size=19, color=RGBColor(0xCB, 0xD5, 0xE1))
text(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.6),
     "Team: [name] · [name] · [name]     Coach: [name]     github.com/alicialiu540-oss/Conrad-project",
     size=13, color=RGBColor(0x94, 0xA3, 0xB8))
notes(s, "Open with warmth and confidence. Judges decide in the first 30 seconds whether they care. "
         "Say the tagline slowly — it is the whole product in one sentence.")

# ================================================================
# 2 — THE MOMENT
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "The moment that started it")
title(s, "Maria did everything right — and nobody saw it.")
rule(s)
text(s, Inches(0.9), Inches(2.0), Inches(7.6), Inches(2.6), [
    [("Maria is 63. Three weeks after knee-replacement surgery, she does her six home "
      "exercises every single day. ", {"size": 22, "color": INK})],
    [("But nobody can see that her knee drifts inward on every squat — and that she never "
      "quite bends it to the angle the therapist asked for.", {"size": 22, "color": INK})],
], line_spacing=1.15)
text(s, Inches(0.9), Inches(4.75), Inches(7.6), Inches(1.6), [
    [("At her follow-up visit, the therapist is puzzled: range of motion has stalled. "
      "A recovery that should take 8 weeks will now take 14.", {"size": 20, "color": MUTED})],
    [("It happened three feet from a camera lens, every day. ", {"size": 20, "color": MUTED}),
     ("The therapist was blind between visits.", {"size": 20, "bold": True, "color": TEAL})],
], line_spacing=1.15)
# right: three stat cards
card(s, Inches(9.0), Inches(2.0), Inches(3.5), Inches(1.3), fill=NAVY)
text(s, Inches(9.2), Inches(2.18), Inches(3.1), Inches(0.9),
     [("6 weeks", {"size": 30, "bold": True, "color": WHITE}),
      ("\nof unsupervised exercise between visits", {"size": 13, "color": RGBColor(0xCB, 0xD5, 0xE1)})])
card(s, Inches(9.0), Inches(3.55), Inches(3.5), Inches(1.3), fill=TEAL_SOFT)
text(s, Inches(9.2), Inches(3.73), Inches(3.1), Inches(0.9),
     [("0", {"size": 30, "bold": True, "color": TEAL}),
      ("\nways for the therapist to see her form at home", {"size": 13, "color": INK})])
card(s, Inches(9.0), Inches(5.1), Inches(3.5), Inches(1.3), fill=LIGHT)
text(s, Inches(9.2), Inches(5.28), Inches(3.1), Inches(0.9),
     [("+6 weeks", {"size": 30, "bold": True, "color": ORANGE}),
      ("\nof added recovery time, pain, and cost", {"size": 13, "color": INK})])
footer(s, 2)
notes(s, "The rubric rewards storytelling (20%). Spend the first minute on Maria — the person, not the tech. "
         "Then land the punchline: the therapist was blind between visits.")

# ================================================================
# 3 — PROBLEM
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "The problem")
title(s, "Between visits, recovery has no witness.")
rule(s)
stats = [
    ("35%", "of PT patients fully adhere to their home exercise program", TEAL),
    ("50–70%", "don't do their exercises correctly — or at all", ORANGE),
    ("$52B", "U.S. physical-therapy market, growing ~5–10% a year", NAVY),
]
x = Inches(0.9)
for big, small, col in stats:
    card(s, x, Inches(2.0), Inches(3.75), Inches(2.0), fill=LIGHT)
    text(s, x + Inches(0.25), Inches(2.25), Inches(3.25), Inches(1.5),
         [[(big, {"size": 40, "bold": True, "color": col})],
          [(small, {"size": 14, "color": MUTED})]], line_spacing=1.1)
    x += Inches(3.95)
text(s, Inches(0.9), Inches(4.5), Inches(11.5), Inches(1.9), [
    [("The blind spot. ", {"size": 19, "bold": True, "color": NAVY}),
     ("Therapists prescribe a home exercise program after nearly every injury and surgery — "
      "the most important part of recovery. But between weekly visits they see nothing: "
      "no video, no angles, no data.", {"size": 17, "color": INK})],
    [("Silent errors compound. ", {"size": 19, "bold": True, "color": NAVY}),
     ("Even motivated patients move with reduced range, knee valgus, or compensation patterns. "
      "The therapist discovers it weeks later — when recovery has already lengthened.", {"size": 17, "color": INK})],
], line_spacing=1.15, space_after=10)
chip(s, Inches(0.9), Inches(6.35), Inches(5.2), Inches(0.5),
     "Sources: Argent et al. 2018 · Physio-pedia · Grand View Research", fill=LIGHT, color=MUTED, size=11, bold=False)
footer(s, 3)
notes(s, "These are the three numbers judges will ask about. Know their sources cold: "
         "Argent 2018 (PMC5856927) for 50.8% non/low adherence; Physio-pedia for 50–65%; "
         "Grand View Research for the $52.3B market.")

# ================================================================
# 4 — SOLUTION
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "The solution")
title(s, "RehabLens: a form coach in every pocket.")
rule(s)
steps = [
    ("1", "Film", "Patient films their exercise with any phone camera. Nothing to wear, strap on, or charge."),
    ("2", "Score", "On-device AI tracks their joints and scores the motion against the therapist's expert reference — with live coaching cues."),
    ("3", "Report", "Every session becomes a progress report: range of motion, reps, scores, trends — for patient and therapist."),
]
x = Inches(0.9)
for num, head, body in steps:
    card(s, x, Inches(2.0), Inches(3.75), Inches(2.9), fill=NAVY if num != "2" else TEAL)
    text(s, x + Inches(0.3), Inches(2.3), Inches(3.15), Inches(2.3),
         [[(num, {"size": 26, "bold": True, "color": TEAL2 if num != "2" else RGBColor(0xCC, 0xFB, 0xF1)})],
          [(head, {"size": 24, "bold": True, "color": WHITE})],
          [(body, {"size": 14.5, "color": RGBColor(0xE2, 0xE8, 0xF0)})]], line_spacing=1.12)
    x += Inches(3.95)
text(s, Inches(0.9), Inches(5.35), Inches(11.5), Inches(1.4),
     [[("The result: ", {"size": 19, "bold": True, "color": NAVY}),
       ("patients get a coach at home; therapists get eyes between visits; clinics get billable "
        "monitoring. And because it runs on-device, ", {"size": 17, "color": INK}),
       ("no video ever leaves the phone.", {"size": 17, "bold": True, "color": TEAL})]],
     line_spacing=1.15)
footer(s, 4)
notes(s, "Pause on step 2 — that is the invention. The words 'on-device' answer the privacy question before it is asked.")

# ================================================================
# 5 — DEMO
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Show, don't tell")
title(s, "Judges can try it right now — on their own phones.")
rule(s)
# left: bullet features
text(s, Inches(0.9), Inches(2.0), Inches(5.6), Inches(4.4), [
    [("✔  Live pose tracking", {"size": 17, "bold": True, "color": TEAL}),
     (" — 33 landmarks, on-device, any phone camera", {"size": 16, "color": INK})],
    [("✔  Digital goniometry", {"size": 17, "bold": True, "color": TEAL}),
     (" — live knee, hip, shoulder, elbow angles", {"size": 16, "color": INK})],
    [("✔  Movement Score 0–100", {"size": 17, "bold": True, "color": TEAL}),
     (" — depth, symmetry, and tempo per rep", {"size": 16, "color": INK})],
    [("✔  Coaching cues", {"size": 17, "bold": True, "color": TEAL}),
     (" — “go deeper — target ≤ 95°, you're at 118°”", {"size": 16, "color": INK})],
    [("✔  5 exercises", {"size": 17, "bold": True, "color": TEAL}),
     (" — knee extension, sit-to-stand, bridge, shoulder, curl", {"size": 16, "color": INK})],
    [("✔  Session report", {"size": 17, "bold": True, "color": TEAL}),
     (" — what the therapist will see", {"size": 16, "color": INK})],
], line_spacing=1.35)
chip(s, Inches(0.9), Inches(6.15), Inches(4.9), Inches(0.55),
     "Try it: repo Settings → Pages → /demo", fill=NAVY, color=WHITE, size=13)
# right: mock device screen
phone = rect(s, Inches(7.2), Inches(1.95), Inches(5.3), Inches(4.9), fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
rect(s, Inches(7.45), Inches(2.2), Inches(4.8), Inches(3.0), fill=RGBColor(0x0B, 0x12, 0x20))
text(s, Inches(7.45), Inches(2.3), Inches(4.8), Inches(0.5), "🔎  LIVE  ·  Seated Knee Extension", size=13, color=TEAL2, align=PP_ALIGN.CENTER)
# skeleton-ish lines
ln = RGBColor(0x5E, 0xEA, 0xD4)
rect(s, Inches(8.6), Inches(3.1), Inches(0.05), Inches(1.3), fill=ln)   # torso
rect(s, Inches(8.6), Inches(4.35), Inches(0.05), Inches(0.55), fill=ln) # thigh
rect(s, Inches(8.6), Inches(4.85), Inches(0.55), Inches(0.05), fill=ln) # shin
text(s, Inches(7.6), Inches(5.35), Inches(4.5), Inches(1.6),
     [[("Movement Score  ", {"size": 14, "color": RGBColor(0x94, 0xA3, 0xB8)}),
       ("94", {"size": 30, "bold": True, "color": TEAL2})],
      [("Reps  8      Angle now  62°      ROM  18–96°", {"size": 14, "color": RGBColor(0xCB, 0xD5, 0xE1)})]],
     align=PP_ALIGN.CENTER, line_spacing=1.3)
footer(s, 5)
notes(s, "This is the demo slide. In the live pitch, mirror a phone to the projector and let a judge move. "
         "The demo is an explainable approximation of the research scorer — say that.")

# ================================================================
# 6 — INNOVATION
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "The innovation")
title(s, "We score the movement sequence — not a snapshot.")
rule(s)
text(s, Inches(0.9), Inches(2.0), Inches(6.6), Inches(3.3), [
    [("Today's tools count reps or measure one static angle. ", {"size": 18, "bold": True, "color": NAVY})],
    [("RehabLens encodes the ", {"size": 17, "color": INK}),
     ("entire motion sequence", {"size": 17, "bold": True, "color": TEAL}),
     (" — patient and expert reference — into the same embedding space with a "
      "Siamese bidirectional LSTM, then scores similarity.", {"size": 17, "color": INK})],
    [("The score captures depth, timing, coordination, and compensation patterns — "
      "not just “did the knee reach 90°.”", {"size": 17, "color": MUTED})],
], line_spacing=1.2)
card(s, Inches(8.0), Inches(2.0), Inches(4.4), Inches(4.4))
text(s, Inches(8.25), Inches(2.15), Inches(3.9), Inches(0.4), "Prototype validation", size=16, bold=True, color=NAVY)
rows = [
    ["Test", "Result"],
    ["Bridge vs bridge (same movement)", "99.5 / 100"],
    ["Bridge vs squat (negative control)", "0.0 / 100"],
    ["Augmented-pair accuracy (20 clips, 12 movements)", "94.2%"],
]
table(s, Inches(8.2), Inches(2.65), Inches(4.0), rows, [2.35, 1.65], row_h=0.62,
      size=12, header_size=12, first_col_bold=True)
footer(s, 6)
notes(s, "Innovation is 30% of the score — spend real time here. Emphasize 'sequence-aware': "
         "a static angle is a photo; we compare motion like a clinician's eye does.")

# ================================================================
# 7 — HOW IT WORKS
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "How it works")
title(s, "Five stages, one score.")
rule(s)
stages = [
    ("Patient video\n+ expert reference", LIGHT, INK),
    ("YOLO Pose\n17 landmarks", TEAL_SOFT, INK),
    ("Joint angles\nhip · knee · thigh · shin", TEAL_SOFT, INK),
    ("Siamese bi-LSTM\nmotion embeddings", TEAL, WHITE),
    ("Cosine similarity\n0–100 Movement Score", NAVY, WHITE),
]
x = Inches(0.9)
w = Inches(2.1)
for i, (label, fill, col) in enumerate(stages):
    shp = rect(s, x, Inches(2.2), w, Inches(1.75), fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = col
    r.font.name = FONT
    if i < len(stages) - 1:
        text(s, x + w + Inches(0.02), Inches(2.85), Inches(0.35), Inches(0.5), "➜", size=22, color=TEAL, align=PP_ALIGN.CENTER)
    x += w + Inches(0.42)
card(s, Inches(0.9), Inches(4.35), Inches(11.5), Inches(2.2), fill=LIGHT)
text(s, Inches(1.15), Inches(4.55), Inches(11.0), Inches(1.9), [
    [("Explainable by design. ", {"size": 17, "bold": True, "color": NAVY}),
     ("Alongside the score we show side-by-side skeleton video, aligned angle curves, and a "
      "plain-language report — so a therapist can see ", {"size": 15.5, "color": INK}),
     ("why", {"size": 15.5, "italic": True, "color": INK}),
     (" the score moved, not just that it moved.", {"size": 15.5, "color": INK})],
    [("Honest about 2D. ", {"size": 17, "bold": True, "color": NAVY}),
     ("Every frame carries joint-visibility confidence; occluded joints are excluded from scoring, "
      "never guessed at. The model is trained with simulated occlusions on purpose.", {"size": 15.5, "color": INK})],
], line_spacing=1.15)
footer(s, 7)
notes(s, "Walk the pipeline left to right in under 30 seconds. Emphasize visibility flags — "
         "it is our built-in answer to 'what if it can't see the joint?'")

# ================================================================
# 8 — MARKET
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "The market")
title(s, "A $52B market with a software layer still being built.")
rule(s)
# nested TAM/SAM/SOM
tam = card(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(1.15), fill=NAVY)
text(s, Inches(1.15), Inches(2.12), Inches(6.5), Inches(0.9),
     [[("TAM — U.S. physical-therapy services", {"size": 17, "bold": True, "color": WHITE}),
       ("\n$52.3B (2025) → $76.6B (2033), 4.9% CAGR · Grand View Research", {"size": 12.5, "color": RGBColor(0xCB, 0xD5, 0xE1)})]])
text(s, Inches(8.9), Inches(2.32), Inches(3.3), Inches(0.7), "$52.3B", size=30, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
sam = card(s, Inches(1.7), Inches(3.35), Inches(10.7), Inches(1.15), fill=TEAL)
text(s, Inches(1.95), Inches(3.47), Inches(6.5), Inches(0.9),
     [[("SAM — digital HEP / monitoring software for outpatient clinics", {"size": 17, "bold": True, "color": WHITE}),
       ("\n≈40,000 U.S. outpatient orthopedic clinics × ~$1,788/yr subscription", {"size": 12.5, "color": RGBColor(0xCC, 0xFB, 0xF1)})]])
text(s, Inches(8.9), Inches(3.67), Inches(3.3), Inches(0.7), "≈ $72M ARR", size=30, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
som = card(s, Inches(2.5), Inches(4.7), Inches(9.9), Inches(1.15), fill=TEAL_SOFT)
text(s, Inches(2.75), Inches(4.82), Inches(6.5), Inches(0.9),
     [[("SOM — our year-3 target", {"size": 17, "bold": True, "color": NAVY}),
       ("\n500 paying clinics ≈ 1.2% of SAM — a deliberately small, credible beachhead", {"size": 12.5, "color": MUTED})]])
text(s, Inches(8.9), Inches(5.02), Inches(3.3), Inches(0.7), "≈ $894K ARR", size=30, bold=True, color=TEAL, align=PP_ALIGN.RIGHT)
text(s, Inches(0.9), Inches(6.1), Inches(11.5), Inches(0.6),
     "Adjacent upside (not counted): white-label to telehealth platforms · insurer outcome partnerships",
     size=14, color=MUTED)
footer(s, 8)
notes(s, "Bottom-up, conservative numbers beat top-down fantasy. The SOM is under 1.5% of SAM — "
         "deliberately, and judges respect that.")

# ================================================================
# 9 — BUSINESS MODEL
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Business model")
title(s, "Clinics pay. Patients don't. Reimbursement pays for it.")
rule(s)
rows = [
    ["Tier", "Price", "Includes"],
    ["Clinic", "$149 / mo", "Unlimited patients · 3 therapist seats · dashboard + patient app"],
    ["Therapist seat", "$59 / mo", "Additional therapist on the same clinic account"],
    ["RTM Pro", "$249 / mo", "Auto-generated documentation for Medicare remote-monitoring billing"],
]
table(s, Inches(0.9), Inches(2.0), Inches(7.1), rows, [1.7, 1.2, 4.2], row_h=0.72, size=13.5, header_size=13.5)
card(s, Inches(8.3), Inches(2.0), Inches(4.2), Inches(3.1), fill=NAVY)
text(s, Inches(8.55), Inches(2.2), Inches(3.7), Inches(2.7), [
    [("Why clinics say yes", {"size": 18, "bold": True, "color": WHITE})],
    [("One monitored Medicare patient earns the clinic ", {"size": 14.5, "color": RGBColor(0xE2, 0xE8, 0xF0)}),
     ("~$19–$54/month", {"size": 15, "bold": True, "color": TEAL2}),
     (" in Remote Therapeutic Monitoring codes (98975/98977).", {"size": 14.5, "color": RGBColor(0xE2, 0xE8, 0xF0)})],
    [("The software pays for itself after 1–3 monitored patients.", {"size": 14.5, "color": RGBColor(0xE2, 0xE8, 0xF0)})],
], line_spacing=1.15)
card(s, Inches(0.9), Inches(5.15), Inches(11.6), Inches(1.4), fill=LIGHT)
text(s, Inches(1.15), Inches(5.35), Inches(11.1), Inches(1.1),
     [[("Why now: ", {"size": 17, "bold": True, "color": NAVY}),
       ("telehealth PT utilization is structurally higher post-COVID, and the 2026 CMS therapy "
        "code list expanded remote-monitoring billing. The reimbursement tailwind is our "
        "“who pays, and why today” answer.", {"size": 15.5, "color": INK})]], line_spacing=1.2)
footer(s, 9)
notes(s, "Marketing is 20% of the rubric. The RTM hook is the sharpest weapon here: "
         "the customer's ROI is arithmetic, not hope. Know 98975 ≈ $21.71 setup, 98976/98977 ≈ $22–54/mo.")

# ================================================================
# 10 — COMPETITION
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Competition")
title(s, "Everyone tracks completion. We score quality.")
rule(s)
rows = [
    ["Player", "What they do", "Where RehabLens wins"],
    ["Sword Health / Hinge Health", "Digital MSK for self-insured employers", "Hardware-free, open, priced for independent clinics"],
    ["Kaia Health", "Guided exercise video apps", "Objective movement-quality scoring from a plain camera"],
    ["Physitrack / Medbridge", "Prescribe & track exercise completion", "Track quality, not just “done”"],
    ["Wearable motion sensors", "Rep counting with extra hardware", "Zero hardware cost and friction; visual form feedback"],
]
table(s, Inches(0.9), Inches(2.0), Inches(11.5), rows, [3.1, 4.1, 4.3], row_h=0.72, size=13, header_size=13.5)
card(s, Inches(0.9), Inches(5.6), Inches(11.5), Inches(1.0), fill=TEAL_SOFT)
text(s, Inches(1.15), Inches(5.82), Inches(11.0), Inches(0.6),
     [[("Positioning: ", {"size": 16, "bold": True, "color": TEAL}),
       ("“The quality layer that existing home-exercise platforms are missing — sequence-aware, "
        "camera-based, and priced for the independent clinic.”", {"size": 16, "color": INK})]])
footer(s, 10)
notes(s, "Don't trash competitors — respect them and position against their channel choice. "
         "The enterprise players went to employers; 40k independent clinics are the gap.")

# ================================================================
# 11 — FINANCIALS
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Financials")
title(s, "Sane unit economics and an honest three years.")
rule(s)
# unit economics
rows = [
    ["Unit economics (per clinic, steady state)", "Monthly"],
    ["Revenue — clinic subscription", "$149"],
    ["Hosting + inference", "$8"],
    ["Support & onboarding", "$10"],
    ["Payments / processing", "$5"],
    ["Gross margin", "≈ 85%"],
]
table(s, Inches(0.9), Inches(2.0), Inches(4.6), rows, [3.4, 1.2], row_h=0.46, size=13, header_size=13)
# chart
text(s, Inches(6.1), Inches(2.0), Inches(6.4), Inches(0.4), "Annual recurring revenue (end of year)",
     size=14, bold=True, color=NAVY)
chart_data = CategoryChartData()
chart_data.categories = ["Year 1", "Year 2", "Year 3"]
chart_data.add_series("ARR", (36, 214, 894))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.1), Inches(2.45), Inches(6.5), Inches(3.1), chart_data)
ch = gf.chart
ch.has_legend = False
plot = ch.plots[0]
plot.has_data_labels = True
plot.data_labels.font.size = Pt(12)
plot.data_labels.font.color.rgb = NAVY
plot.data_labels.number_format = '$#,##0K'
plot.data_labels.number_format_is_linked = False
for ser in plot.series:
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = TEAL
cat_ax = ch.category_axis
cat_ax.tick_labels.font.size = Pt(12)
val_ax = ch.value_axis
val_ax.tick_labels.font.size = Pt(10)
val_ax.has_major_gridlines = True
# key assumptions
card(s, Inches(0.9), Inches(5.15), Inches(11.6), Inches(1.4), fill=LIGHT)
text(s, Inches(1.15), Inches(5.3), Inches(11.1), Inches(1.2),
     [[("Assumptions: ", {"size": 15, "bold": True, "color": NAVY}),
       ("pricing held flat; 10%/yr churn; no founder salaries in years 1–2; 20 clinics by year 1, "
        "120 by year 2, 500 by year 3. CAC ≈ $400/clinic → ~3-month payback, LTV:CAC ≈ 11. "
        "All subscription revenue — white-label and insurer channels are roadmap upside, not forecast.", {"size": 14, "color": INK})]],
     line_spacing=1.15)
footer(s, 11)
notes(s, "Financials are 10% of the rubric — be sane, not fancy. The LTV:CAC ≈ 11 line lands the "
         "efficiency story; admit the model becomes venture-scale only via the future channels.")

# ================================================================
# 12 — SAFETY & ETHICS
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Safety & ethics")
title(s, "We turn our limitations into our safety case.")
rule(s)
card(s, Inches(0.9), Inches(2.0), Inches(5.55), Inches(4.5), fill=NAVY)
text(s, Inches(1.15), Inches(2.2), Inches(5.05), Inches(4.1), [
    [("What RehabLens is NOT", {"size": 20, "bold": True, "color": WHITE})],
    [("✕  Not a medical device\n✕  Not a diagnosis or prescription\n✕  Not proof an exercise is safe\n"
      "✕  Not a substitute for a physical therapist", {"size": 17, "color": RGBColor(0xE2, 0xE8, 0xF0)})],
], line_spacing=1.3)
text(s, Inches(1.15), Inches(5.6), Inches(5.05), Inches(0.8),
     [[("Scores are “check with your therapist” flags — ", {"size": 14, "color": TEAL2}),
       ("never advice to push through pain.", {"size": 14, "bold": True, "color": WHITE})]], line_spacing=1.2)
rows = [
    ["Known limitation", "Our mitigation"],
    ["2D camera: depth ambiguity, occlusion", "Confidence-gated scoring — uncertain joints are excluded, never guessed"],
    ["Trained on one demonstrator today", "Consented multi-participant dataset, participant-split validation"],
    ["Form feedback could mislead a patient", "Fail-soft design: unclear view → “no score”, never wrong advice"],
    ["Privacy risk from video", "On-device processing; only anonymized metrics reach the clinic"],
    ["Reimbursement rules vary by payer", "RTM tier ships with billing documentation; validated by a pilot clinic"],
]
table(s, Inches(6.7), Inches(2.0), Inches(5.75), rows, [2.75, 3.0], row_h=0.66, size=11.5, header_size=12)
chip(s, Inches(6.7), Inches(5.85), Inches(5.75), Inches(0.6),
     "Validation target: Cohen's κ ≥ 0.6 vs clinician labels before pilot use", fill=TEAL_SOFT, color=TEAL, size=13)
footer(s, 12)
notes(s, "This is the anti-objection slide. Saying 'we know where it fails' reads as engineering maturity "
         "and preempts the hardest judge question. Deliver it calmly — it's a strength, not a confession.")

# ================================================================
# 13 — ROADMAP & ASK
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=WHITE)
kicker(s, "Roadmap & the ask")
title(s, "Twelve months from prototype to pilot data.")
rule(s)
phases = [
    ("M 0–3", "Evidence", "Pilot clinic partner; first consented multi-participant dataset", LIGHT, INK),
    ("M 4–8", "Validation", "Participant-split retrain; report κ vs clinician labels", TEAL_SOFT, INK),
    ("M 9–12", "Pilot", "2-clinic, 3-month pilot; measure adherence & ROM deltas", TEAL, WHITE),
    ("M 12–24", "Launch", "$149/mo commercial tier; target 120 paying clinics", NAVY, WHITE),
]
x = Inches(0.9)
for when, head, body, fill, col in phases:
    card(s, x, Inches(2.0), Inches(2.75), Inches(2.4), fill=fill)
    text(s, x + Inches(0.2), Inches(2.2), Inches(2.35), Inches(2.0),
         [[(when, {"size": 14, "bold": True, "color": TEAL2 if fill == NAVY else (WHITE if fill in (TEAL, NAVY) else TEAL)})],
          [(head, {"size": 21, "bold": True, "color": col})],
          [(body, {"size": 13, "color": RGBColor(0xE2, 0xE8, 0xF0) if fill in (NAVY, TEAL) else MUTED})]],
         line_spacing=1.1)
    x += Inches(2.95)
card(s, Inches(0.9), Inches(4.85), Inches(11.5), Inches(1.7), fill=LIGHT, line=TEAL)
text(s, Inches(1.15), Inches(5.05), Inches(11.0), Inches(1.35), [
    [("What we need from you: ", {"size": 19, "bold": True, "color": NAVY})],
    [("1) One physical therapist to critique our scoring — 30 minutes.   2) $5–10K for compute, "
      "HIPAA-capable hosting, and pilot materials.   3) Introductions to a local outpatient clinic.", {"size": 16, "color": INK})],
], line_spacing=1.2)
footer(s, 13)
notes(s, "Close the ask with specificity: a named person, a small number, one introduction. "
         "Judges are investors in spirit — a vague ask loses them.")

# ================================================================
# 14 — CLOSING
# ================================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, Inches(3.1), SW, Inches(0.06), fill=TEAL2)
text(s, Inches(0.9), Inches(1.4), Inches(11.5), Inches(1.4),
     "Every recovery deserves eyes between visits.", size=44, color=WHITE, bold=True)
text(s, Inches(0.9), Inches(2.35), Inches(11.5), Inches(0.8),
     "RehabLens gives every physical-therapy patient a coach at home — with nothing "
     "but the camera they already own.", size=20, color=RGBColor(0xCB, 0xD5, 0xE1))
text(s, Inches(0.9), Inches(3.5), Inches(11.5), Inches(1.2), [
    [("Try the live demo:  ", {"size": 18, "color": RGBColor(0x99, 0xF6, 0xE4)}),
     ("github.com/alicialiu540-oss/Conrad-project  →  demo/", {"size": 18, "bold": True, "color": WHITE})],
    [("Prototype: YOLO Pose + Siamese LSTM · 94.2% augmented-pair accuracy · MIT-licensed", {"size": 14, "color": RGBColor(0x94, 0xA3, 0xB8)})],
], line_spacing=1.4)
text(s, Inches(0.9), Inches(5.9), Inches(11.5), Inches(0.7),
     "Thank you.   — [Team names], Health & Nutrition", size=18, color=RGBColor(0xCB, 0xD5, 0xE1))
notes(s, "Land the mission line and stop. Leave time for the demo — the deck's last slide is "
         "the phone in your hand.")

OUT = "RehabLens_Pitch_Deck.pptx"
prs.save(OUT)
print(f"Saved {OUT} with {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
