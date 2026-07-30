#!/usr/bin/env python3
"""Generate OpenClaw technical document matching templet.pdf layout."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfgen_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, sys

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.28 x 841.89
L_MARGIN = 85
R_MARGIN = 71
T_MARGIN = 90
B_MARGIN = 65
BODY_W = PAGE_W - L_MARGIN - R_MARGIN   # 439 pt

# ── Colours ────────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#1B3A6B')
BLUE   = colors.HexColor('#2E6DB4')
LIGHT  = colors.HexColor('#E8F0FA')
GREY   = colors.HexColor('#555555')
BLACK  = colors.black
WHITE  = colors.white

# ── Fonts ──────────────────────────────────────────────────────────────────────
# Try to register a CJK-capable font; fall back to Helvetica gracefully
def try_register_font(name, path):
    try:
        pdfmetrics.registerFont(TTFont(name, path))
        return True
    except Exception:
        return False

FONT_PATHS = [
    ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'BodyFont'),
    ('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',    'BodyFontBold'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',                 'BodyFont'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',            'BodyFontBold'),
]
registered = {}
for path, alias in FONT_PATHS:
    if alias not in registered and os.path.exists(path):
        if try_register_font(alias, path):
            registered[alias] = alias

BODY   = registered.get('BodyFont',     'Helvetica')
BOLDF  = registered.get('BodyFontBold', 'Helvetica-Bold')

# ── Styles ──────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = dict(fontName=BODY, fontSize=11, leading=18, textColor=BLACK,
                alignment=TA_JUSTIFY, spaceAfter=6)

    s['body']      = ParagraphStyle('body', **base)
    s['body_left'] = ParagraphStyle('body_left', **{**base, 'alignment': TA_LEFT})
    s['h1']        = ParagraphStyle('h1',  fontName=BOLDF, fontSize=18,
                                    leading=24, textColor=NAVY,
                                    spaceAfter=6, spaceBefore=18)
    s['h2']        = ParagraphStyle('h2',  fontName=BOLDF, fontSize=14,
                                    leading=20, textColor=BLUE,
                                    spaceAfter=4, spaceBefore=12)
    s['h3']        = ParagraphStyle('h3',  fontName=BOLDF, fontSize=12,
                                    leading=18, textColor=GREY,
                                    spaceAfter=3, spaceBefore=8)
    s['code']      = ParagraphStyle('code', fontName='Courier', fontSize=9,
                                    leading=13, textColor=BLACK,
                                    backColor=colors.HexColor('#F5F5F5'),
                                    leftIndent=12, rightIndent=12,
                                    spaceAfter=6, spaceBefore=4,
                                    borderPadding=(4,6,4,6))
    s['note']      = ParagraphStyle('note', fontName=BODY, fontSize=10,
                                    leading=15, textColor=GREY,
                                    leftIndent=16, rightIndent=8,
                                    spaceAfter=6)
    s['bullet']    = ParagraphStyle('bullet', fontName=BODY, fontSize=11,
                                    leading=18, leftIndent=20, bulletIndent=8,
                                    spaceAfter=3)
    s['cover_title'] = ParagraphStyle('cover_title', fontName=BOLDF, fontSize=28,
                                      leading=36, textColor=WHITE,
                                      alignment=TA_CENTER)
    s['cover_sub']   = ParagraphStyle('cover_sub', fontName=BODY, fontSize=14,
                                      leading=20, textColor=colors.HexColor('#D0DFF5'),
                                      alignment=TA_CENTER)
    s['cover_meta']  = ParagraphStyle('cover_meta', fontName=BODY, fontSize=11,
                                      leading=16, textColor=WHITE,
                                      alignment=TA_CENTER)
    s['toc_h1']    = ParagraphStyle('toc_h1', fontName=BOLDF, fontSize=11,
                                    leading=18, leftIndent=0)
    s['toc_h2']    = ParagraphStyle('toc_h2', fontName=BODY,  fontSize=10,
                                    leading=16, leftIndent=18)
    return s

# ── Header / Footer ─────────────────────────────────────────────────────────────
def draw_header_footer(canv, doc):
    canv.saveState()
    page_num = doc.page

    # --- Header ---
    # Double thin lines
    canv.setStrokeColor(BLUE)
    canv.setLineWidth(1.2)
    canv.line(L_MARGIN, PAGE_H - 78, PAGE_W - R_MARGIN, PAGE_H - 78)
    canv.setLineWidth(0.4)
    canv.line(L_MARGIN, PAGE_H - 81, PAGE_W - R_MARGIN, PAGE_H - 81)

    # Header text
    canv.setFont(BODY, 9)
    canv.setFillColor(GREY)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 68, "OpenClaw — Technical Overview")

    # --- Footer ---
    canv.setStrokeColor(BLUE)
    canv.setLineWidth(0.5)
    canv.line(L_MARGIN, B_MARGIN + 14, PAGE_W - R_MARGIN, B_MARGIN + 14)

    canv.setFont(BODY, 9)
    canv.setFillColor(GREY)
    canv.drawCentredString(PAGE_W / 2, B_MARGIN, str(page_num))

    canv.restoreState()


def draw_cover(canv, doc):
    """Cover page: navy top band + white logo area + bottom band."""
    canv.saveState()

    # Top band
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 240, PAGE_W, 240, fill=1, stroke=0)

    # Accent stripe
    canv.setFillColor(BLUE)
    canv.rect(0, PAGE_H - 245, PAGE_W, 5, fill=1, stroke=0)

    # Bottom band
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, 80, fill=1, stroke=0)
    canv.setFillColor(BLUE)
    canv.rect(0, 80, PAGE_W, 3, fill=1, stroke=0)

    # Footer text on cover
    canv.setFont(BODY, 10)
    canv.setFillColor(colors.HexColor('#A0B8D8'))
    canv.drawCentredString(PAGE_W / 2, 30, "March 2026  ·  https://openclaw.ai")

    canv.restoreState()


# ── Document content ────────────────────────────────────────────────────────────
CONTENT = [
    # ── Chapter 1 ────────────────────────────────────────────────────────────
    ("h1", "1  Introduction"),
    ("body", (
        "OpenClaw is an AI-powered personal assistant platform designed to run locally "
        "on any Linux, macOS, or Windows host. It combines a conversational LLM gateway "
        "with a rich extension ecosystem, giving users a single coherent interface to "
        "their files, communication channels, home automation, and cloud services."
    )),
    ("body", (
        "Unlike SaaS-hosted assistants, OpenClaw keeps all credentials and conversation "
        "history on the user's own machine. The gateway process is lightweight enough to "
        "run continuously on a Raspberry Pi while remaining capable enough to orchestrate "
        "multi-step agentic workflows on a workstation."
    )),

    ("h2", "1.1  Design Goals"),
    ("bullet", "• <b>Privacy-first</b> — no data leaves the host unless the user explicitly requests it."),
    ("bullet", "• <b>Extensible</b> — new capabilities are added via self-contained AgentSkill packages."),
    ("bullet", "• <b>Multi-channel</b> — one assistant instance serves Telegram, Discord, Signal, WhatsApp, and web chat simultaneously."),
    ("bullet", "• <b>Composable</b> — skills, cron jobs, sub-agents, and external tools can be combined freely."),

    ("h2", "1.2  Scope of This Document"),
    ("body", (
        "This document provides a technical overview of OpenClaw's architecture, core "
        "subsystems, skill system, scheduling model, and deployment considerations. "
        "It is intended for developers integrating OpenClaw into their workflow and for "
        "administrators responsible for operating an OpenClaw instance."
    )),

    # ── Chapter 2 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "2  Architecture"),
    ("body", (
        "OpenClaw is structured as a single Node.js gateway process that manages sessions, "
        "routes messages between channel adapters and model providers, and executes tool "
        "calls on behalf of the active LLM."
    )),

    ("h2", "2.1  Gateway Process"),
    ("body", (
        "The gateway is the central process that starts on boot (or on demand) and listens "
        "for incoming events from all configured channel plugins. It maintains a session "
        "registry, persists conversation history to disk, and forwards turns to the "
        "configured LLM provider."
    )),
    ("body", "Key responsibilities of the gateway:"),
    ("bullet", "• Accept and authenticate inbound messages from channel plugins."),
    ("bullet", "• Maintain per-session conversation state and tool-call history."),
    ("bullet", "• Dispatch tool calls to the host system (exec, read/write, browser, etc.)."),
    ("bullet", "• Forward completion events back to the originating channel."),
    ("bullet", "• Schedule and fire cron jobs via the built-in cron subsystem."),

    ("h2", "2.2  Channel Plugins"),
    ("body", (
        "Each messaging surface is handled by a dedicated channel plugin. Plugins are "
        "thin adapters: they authenticate with the upstream API, normalise incoming events "
        "into OpenClaw's internal message schema, and translate outbound completions back "
        "to the platform's native format."
    )),
    ("body", "Currently supported channels include:"),
    ("bullet", "• <b>Telegram</b> — via Bot API; supports inline buttons, voice, and file attachments."),
    ("bullet", "• <b>Discord</b> — supports slash commands, reactions, threads, and forum channels."),
    ("bullet", "• <b>Signal</b> — via signal-cli; supports end-to-end encrypted messaging."),
    ("bullet", "• <b>WhatsApp</b> — via WhatsApp Web.js; supports media and voice notes."),
    ("bullet", "• <b>Web Chat</b> — a built-in single-page chat UI served over HTTP/HTTPS."),

    ("h2", "2.3  Model Providers"),
    ("body", (
        "OpenClaw is model-agnostic. Any OpenAI-compatible API endpoint can be registered "
        "as a provider. The active model for a session can be changed at runtime with the "
        "<code>/model</code> command or via the session-status tool. Built-in aliases map "
        "short names to full provider/model strings, reducing configuration overhead."
    )),

    # ── Chapter 3 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "3  Skill System"),
    ("body", (
        "Skills are the primary extension mechanism. A skill is a directory containing "
        "a <code>SKILL.md</code> file with YAML front-matter (name + description) followed "
        "by instructions the model reads when that skill is selected."
    )),

    ("h2", "3.1  Skill Discovery"),
    ("body", (
        "At startup, OpenClaw scans four skill directories in order of increasing priority:"
    )),

    # Table
    ("table", {
        "headers": ["Priority", "Directory", "Notes"],
        "rows": [
            ["1 (lowest)", "openclaw/skills/",          "Built-in skills bundled with OpenClaw"],
            ["2",          "~/.openclaw/skills/",        "User-managed global skills"],
            ["3",          "<workspace>/skills/",        "Workspace-specific skills"],
            ["4 (highest)","Extra paths (config)",       "Additional paths via config"],
        ]
    }),

    ("body", (
        "When two skills share the same name, the higher-priority entry wins. "
        "Skills are injected into the system prompt as a list of <code>(name, description)</code> "
        "pairs; the full SKILL.md is only read when a task matches that skill."
    )),

    ("h2", "3.2  Skill Anatomy"),
    ("body", "A minimal skill has the following structure:"),
    ("code", (
        "my-skill/\n"
        "  SKILL.md          ← front-matter + instructions\n"
        "  scripts/          ← helper scripts (optional)\n"
        "  references/       ← additional reference docs (optional)"
    )),
    ("body", (
        "The SKILL.md front-matter must contain at minimum a <code>name</code> and a "
        "<code>description</code>. The description is surfaced to the model for skill "
        "selection and should be concise but specific."
    )),

    ("h2", "3.3  Installing Skills"),
    ("body", (
        "Skills can be installed manually by dropping a directory into the appropriate "
        "skills folder, or via the <b>ClawHub</b> registry:"
    )),
    ("code", "clawhub install <skill-name>"),
    ("body", (
        "The <code>skill-vetter</code> skill provides a security review protocol and should "
        "be run before installing any third-party skill to check for credential theft, "
        "obfuscated code, or exfiltration patterns."
    )),

    # ── Chapter 4 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "4  Scheduling & Automation"),

    ("h2", "4.1  Cron Jobs"),
    ("body", (
        "OpenClaw includes a built-in cron scheduler. Jobs are persisted to disk and "
        "survive gateway restarts. Three schedule kinds are supported:"
    )),
    ("bullet", "• <b>at</b> — one-shot execution at an absolute ISO-8601 timestamp."),
    ("bullet", "• <b>every</b> — recurring execution at a fixed millisecond interval."),
    ("bullet", "• <b>cron</b> — standard cron expression with optional timezone."),
    ("body", (
        "Each job carries a payload (<code>systemEvent</code> or <code>agentTurn</code>), "
        "an optional delivery target (announce to a channel or HTTP webhook POST), and a "
        "session target (<code>main</code> or <code>isolated</code>)."
    )),

    ("h2", "4.2  Heartbeats"),
    ("body", (
        "A configurable heartbeat prompt is injected into the main session at a regular "
        "interval. The agent reads <code>HEARTBEAT.md</code> (if present) and acts on any "
        "pending tasks, then replies <code>HEARTBEAT_OK</code> if nothing requires "
        "attention. This mechanism enables lightweight background monitoring (email, "
        "calendar, weather) without spawning isolated jobs."
    )),

    ("h2", "4.3  Sub-agents"),
    ("body", (
        "Long-running or compute-intensive tasks can be delegated to isolated sub-agent "
        "sessions. Sub-agents are spawned with <code>sessions_spawn</code> and run "
        "independently of the main session. Completion events are announced back to the "
        "originating channel automatically."
    )),

    # ── Chapter 5 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "5  Workspace & Memory"),

    ("h2", "5.1  Workspace Layout"),
    ("body", (
        "The workspace is a single directory (default <code>~/.openclaw/workspace</code>) "
        "that the agent treats as its home. Key files:"
    )),
    ("bullet", "• <b>SOUL.md</b> — defines the agent's persona, values, and communication style."),
    ("bullet", "• <b>USER.md</b> — describes the human: name, timezone, preferences, contact info."),
    ("bullet", "• <b>MEMORY.md</b> — long-term curated memory, loaded in main sessions only."),
    ("bullet", "• <b>HEARTBEAT.md</b> — task checklist for periodic heartbeat runs."),
    ("bullet", "• <b>memory/YYYY-MM-DD.md</b> — daily raw notes for short-term continuity."),

    ("h2", "5.2  Memory Model"),
    ("body", (
        "Each session starts with a fresh context window. Continuity is achieved by "
        "reading workspace files at session startup. The agent is expected to write "
        "significant events, decisions, and lessons to the daily memory file and "
        "periodically distil them into MEMORY.md."
    )),
    ("note", (
        "Note: MEMORY.md should only be loaded in direct (main) sessions with the "
        "owner. It must not be surfaced in group chats or shared sessions to prevent "
        "leaking personal context."
    )),

    # ── Chapter 6 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "6  Deployment"),

    ("h2", "6.1  Requirements"),
    ("body", "Minimum requirements for a production OpenClaw instance:"),
    ("bullet", "• Node.js 18+ (v24 recommended)"),
    ("bullet", "• 512 MB RAM (1 GB+ recommended for concurrent sub-agents)"),
    ("bullet", "• Linux, macOS, or WSL2 on Windows"),
    ("bullet", "• Outbound HTTPS access to the configured LLM provider"),

    ("h2", "6.2  Installation"),
    ("code", (
        "# Install via npm\n"
        "npm install -g openclaw\n\n"
        "# First-time setup\n"
        "openclaw setup\n\n"
        "# Start the gateway\n"
        "openclaw gateway start"
    )),

    ("h2", "6.3  Configuration"),
    ("body", (
        "All configuration lives in <code>~/.openclaw/config.json</code>. "
        "The recommended way to modify configuration is through the <code>config.patch</code> "
        "gateway action, which merges changes with the existing config and restarts the "
        "gateway automatically."
    )),
    ("body", (
        "Sensitive values (API keys, bot tokens) should be stored as environment variables "
        "and referenced via <code>${ENV_VAR}</code> syntax in the config file rather than "
        "being hardcoded."
    )),

    ("h2", "6.4  Security Considerations"),
    ("bullet", "• Run the gateway as a non-root user with minimal filesystem permissions."),
    ("bullet", "• Enable exec approval policies to require confirmation before running elevated commands."),
    ("bullet", "• Review third-party skills with the <code>skill-vetter</code> skill before installation."),
    ("bullet", "• Rotate API keys periodically and revoke unused channel bot tokens."),

    # ── Chapter 7 ────────────────────────────────────────────────────────────
    ("pagebreak", None),
    ("h1", "7  Further Resources"),
    ("body", (
        "The following resources provide additional information about OpenClaw:"
    )),
    ("bullet", "• <b>Documentation</b>: https://docs.openclaw.ai"),
    ("bullet", "• <b>Source code</b>: https://github.com/openclaw/openclaw"),
    ("bullet", "• <b>Skill registry</b>: https://clawhub.com"),
    ("bullet", "• <b>Community</b>: https://discord.com/invite/clawd"),
    ("spacer", 12),
    ("note", (
        "OpenClaw is under active development. APIs and configuration formats "
        "may change between minor versions. Always consult the local docs at "
        "<code>/root/.nvm/versions/node/.../openclaw/docs</code> for the version "
        "currently installed."
    )),
]


# ── Build PDF ──────────────────────────────────────────────────────────────────
def build(out_path):
    styles = make_styles()

    # ── Page templates ──
    body_frame = Frame(
        L_MARGIN, B_MARGIN + 20,
        BODY_W, PAGE_H - T_MARGIN - B_MARGIN - 20,
        id='body', showBoundary=0
    )

    cover_frame = Frame(
        L_MARGIN, 90, BODY_W, PAGE_H - 260 - 90,
        id='cover', showBoundary=0
    )

    doc = BaseDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=L_MARGIN, rightMargin=R_MARGIN,
        topMargin=T_MARGIN,  bottomMargin=B_MARGIN + 20,
        title="OpenClaw — Technical Overview",
        author="OpenClaw",
    )

    cover_tmpl = PageTemplate(
        id='Cover',
        frames=[cover_frame],
        onPage=draw_cover,
    )
    body_tmpl = PageTemplate(
        id='Body',
        frames=[body_frame],
        onPage=draw_header_footer,
    )
    doc.addPageTemplates([cover_tmpl, body_tmpl])

    story = []

    # ── Cover page ──
    story.append(Spacer(1, 30))
    story.append(Paragraph("OpenClaw", styles['cover_title']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Technical Overview", styles['cover_sub']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Version 1.0  ·  March 2026", styles['cover_meta']))
    story.append(Spacer(1, 60))
    story.append(Paragraph(
        "A comprehensive guide to the architecture, skill system,<br/>"
        "scheduling model, and deployment of the OpenClaw AI assistant platform.",
        styles['cover_sub']
    ))

    story.append(PageBreak())

    # Switch to body template from page 2 onward
    from reportlab.platypus import NextPageTemplate
    story.insert(len(story) - 1, NextPageTemplate('Body'))

    # ── Content ──
    def add_table(data):
        hdr   = data['headers']
        rows  = data['rows']
        col_w = [60, 180, 199]   # sum = 439
        table_data = [[Paragraph(f'<b>{h}</b>', styles['body_left']) for h in hdr]]
        for r in rows:
            table_data.append([Paragraph(str(c), styles['body_left']) for c in r])

        t = Table(table_data, colWidths=col_w, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0),  NAVY),
            ('TEXTCOLOR',  (0,0), (-1,0),  WHITE),
            ('FONTNAME',   (0,0), (-1,0),  BOLDF),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT]),
            ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#CCCCCC')),
            ('VALIGN',     (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    for kind, data in CONTENT:
        if kind == 'h1':
            story.append(Paragraph(data, styles['h1']))
            story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY,
                                    spaceAfter=6))
        elif kind == 'h2':
            story.append(Paragraph(data, styles['h2']))
        elif kind == 'h3':
            story.append(Paragraph(data, styles['h3']))
        elif kind == 'body':
            story.append(Paragraph(data, styles['body']))
        elif kind == 'bullet':
            story.append(Paragraph(data, styles['bullet']))
        elif kind == 'code':
            # Render as single paragraph with <br/> newlines
            lines = data.split('\n')
            html_lines = [line.replace(' ', '&nbsp;') if line.strip() == '' else line for line in lines]
            html = '<br/>'.join(html_lines)
            story.append(Paragraph(html, styles['code']))
            story.append(Spacer(1, 4))
        elif kind == 'note':
            story.append(Paragraph(f'<i>{data}</i>', styles['note']))
        elif kind == 'table':
            add_table(data)
        elif kind == 'pagebreak':
            story.append(PageBreak())
        elif kind == 'spacer':
            story.append(Spacer(1, data))

    doc.build(story)
    print(f"Written: {out_path}")


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/root/.openclaw/workspace/openclaw_overview.pdf'
    build(out)
