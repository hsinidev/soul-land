import os
import re
import glob
import json
import urllib.parse

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
ROOT_DIR   = r"c:\Users\hsini\Desktop\website manga projects\Soul Land - Legend of The Gods' Realm"
MANGA_DIR  = os.path.join(ROOT_DIR, "manga", "Soul Land")
MANGA_NAME = "Soul Land: Legend of The Gods' Realm"
SITE_URL   = "https://readsoulland.com"

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def extract_chapter_number(folder_name):
    """Extract numeric chapter number from Ch.NNN style names."""
    match = re.search(r'Ch\.(\d+)', folder_name)
    return int(match.group(1)) if match else 0

def extract_chapter_title(folder_name):
    """Extract the descriptive title after the chapter number."""
    match = re.match(r'Ch\.\d+\s*-?\s*(.*)', folder_name)
    if match and match.group(1).strip():
        return match.group(1).strip()
    return ""

def get_images(folder_path):
    """Return naturally sorted list of image basenames in a chapter folder (no dupes)."""
    extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    seen = set()
    images = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)):
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions:
                key = f.lower()
                if key not in seen:
                    seen.add(key)
                    images.append(f)
    def natural_key(s):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
    images.sort(key=natural_key)
    return images


# ─────────────────────────────────────────────
#  SHARED CSS / HEAD
# ─────────────────────────────────────────────
COMMON_HEAD = """
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0a0a14">
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Google Tag -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-50K2PXNMXB"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-50K2PXNMXB');
    </script>

    <style>
      :root {{
        --primary: #4f46e5;
        --spirit-blue: #00d2ff;
        --spirit-gold: #f5a623;
        --void: #1e1b4b;
        --darkbg: #0a0a14;
        --surface: #111120;
        --glass: rgba(14,14,28,0.85);
        --text: #e8eaf6;
        --muted: #9094b8;
        --border: rgba(79,70,229,0.25);
        --glow-blue: 0 0 30px rgba(0,210,255,0.35);
        --glow-gold: 0 0 20px rgba(245,166,35,0.4);
      }}
      *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
      html {{ scroll-behavior: smooth; }}
      body {{
        background-color: var(--darkbg);
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        overflow-x: hidden;
      }}
      /* ── SCROLLBAR ── */
      ::-webkit-scrollbar {{ width: 6px; }}
      ::-webkit-scrollbar-track {{ background: var(--darkbg); }}
      ::-webkit-scrollbar-thumb {{ background: var(--primary); border-radius: 3px; }}
      /* ── GLASS PANEL ── */
      .glass {{
        background: var(--glass);
        backdrop-filter: blur(18px) saturate(160%);
        -webkit-backdrop-filter: blur(18px) saturate(160%);
        border-bottom: 1px solid var(--border);
      }}
      /* ── TEXT GRADIENT ── */
      .text-grad {{
        background: linear-gradient(135deg, var(--spirit-blue), var(--primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }}
      /* ── SPIRIT GLOW RING ── */
      @keyframes spin-slow {{ to {{ transform: rotate(360deg); }} }}
      @keyframes float {{
        0%,100% {{ transform: translateY(0px); }}
        50%       {{ transform: translateY(-10px); }}
      }}
      @keyframes pulse-glow {{
        0%,100% {{ box-shadow: 0 0 15px rgba(0,210,255,0.2); }}
        50%      {{ box-shadow: 0 0 35px rgba(0,210,255,0.6); }}
      }}
      /* ── HIDDEN (for load-more) ── */
      .hidden { display: none !important; }
      /* ── FAST SCROLL BUTTONS ── */
      .scroll-btn {{
        position: fixed; right: 18px; z-index: 200;
        width: 46px; height: 46px; border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), #6d28d9);
        border: 2px solid var(--spirit-blue);
        color: #fff; font-size: 20px; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        box-shadow: var(--glow-blue);
        transition: transform 0.25s, box-shadow 0.25s;
      }}
      .scroll-btn:hover {{ transform: scale(1.15); box-shadow: 0 0 40px rgba(0,210,255,0.6); }}
      #btn-up   {{ bottom: 78px; }}
      #btn-down {{ bottom: 20px; }}
      /* ── HEADER SEARCH ── */
      #search-dropdown {{ display: none; max-height: 420px; overflow-y: auto; }}
      #search-dropdown.show {{ display: block; }}
      #search-dropdown::-webkit-scrollbar {{ width: 5px; }}
      #search-dropdown::-webkit-scrollbar-thumb {{ background: #374151; border-radius: 4px; }}
      /* ── CHAPTER CARD ── */
      .ch-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
      }}
      .ch-card:hover {{
        border-color: var(--spirit-blue);
        transform: translateY(-5px) scale(1.02);
        box-shadow: var(--glow-blue);
      }}
      .ch-card img {{ display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s, opacity 0.4s; opacity: 0.75; }}
      .ch-card:hover img {{ transform: scale(1.08); opacity: 1; }}
      /* ── READER IMAGES ── */
      .reader-img {{
        display: block;
        width: 100%;
        max-width: 100%;
        height: auto;
        margin: 0;
        padding: 0;
        border: none;
        vertical-align: top;
        line-height: 0;
      }}
      /* Reader container: strict vertical strip, zero gaps */
      #reader-main {{
        display: block;
        background: #000;
        width: 100%;
        margin: 0;
        padding: 0;
        line-height: 0;
        font-size: 0;
      }}
      /* ── NAV BAR (chapter pages) ── */
      .ch-nav-bar {{
        position: sticky; top: 0; z-index: 100;
        background: var(--glass);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid var(--border);
        padding: 12px 24px;
        display: flex; justify-content: space-between; align-items: center; gap: 12px;
        flex-wrap: wrap;
      }}
      .nav-btn {{
        padding: 7px 20px; border-radius: 999px; font-weight: 600; font-size: 0.85rem;
        border: 1px solid var(--border); background: var(--surface);
        color: var(--text); text-decoration: none;
        transition: background 0.25s, border-color 0.25s, box-shadow 0.25s;
        white-space: nowrap;
      }}
      .nav-btn:hover, .nav-btn.active {{
        background: var(--primary);
        border-color: var(--spirit-blue);
        box-shadow: var(--glow-blue);
      }}
      .nav-btn.gold {{ border-color: var(--spirit-gold); color: var(--spirit-gold); }}
      .nav-btn.gold:hover {{ background: var(--spirit-gold); color: #000; box-shadow: var(--glow-gold); }}
      /* ── CHAPTER SELECT ── */
      .ch-select {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 7px 16px;
        color: var(--text);
        font-size: 0.85rem;
        cursor: pointer;
        outline: none;
        appearance: none;
        max-width: 200px;
      }}
      /* ── PROGRESS BAR ── */
      #read-progress {{
        position: fixed; top: 0; left: 0; height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--spirit-blue));
        z-index: 9999; width: 0%; transition: width 0.1s linear;
      }}
    </style>
"""

SCROLL_BTNS = """
    <button id="btn-up"   class="scroll-btn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="Top">↑</button>
    <button id="btn-down" class="scroll-btn" onclick="window.scrollTo({{top:document.body.scrollHeight,behavior:'smooth'}})" title="Bottom">↓</button>
"""

# ─────────────────────────────────────────────
#  CHAPTER PAGE GENERATOR
# ─────────────────────────────────────────────
def build_chapter_page(c, chapters_sorted):
    """Generate a premium reader page HTML string for a chapter."""
    num       = c['num']
    folder    = c['folder']
    title     = c['title'] or f"Chapter {num}"
    imgs      = c['images']

    # Find prev/next in the sorted (asc) list
    idx = next((i for i, x in enumerate(chapters_sorted) if x['num'] == num), -1)
    prev_ch = chapters_sorted[idx - 1] if idx > 0 else None
    next_ch = chapters_sorted[idx + 1] if idx < len(chapters_sorted) - 1 else None

    prev_link = f'<a href="../{prev_ch["folder"]}/index.html" class="nav-btn">← Ch.{prev_ch["num"]:03d}</a>' if prev_ch else '<span class="nav-btn" style="opacity:0.3;cursor:not-allowed;">← First</span>'
    next_link = f'<a href="../{next_ch["folder"]}/index.html" class="nav-btn gold">Ch.{next_ch["num"]:03d} →</a>' if next_ch else '<span class="nav-btn gold" style="opacity:0.3;cursor:not-allowed;">Last →</span>'

    # Chapter <select> dropdown
    select_opts = ""
    for ch in chapters_sorted:
        sel = " selected" if ch['num'] == num else ""
        select_opts += f'<option value="../{ch["folder"]}/index.html"{sel}>Ch.{ch["num"]:03d} – {ch["title"] or "Chapter "+str(ch["num"])}</option>\n'

    img_tags = "\n".join(
        f'<img src="./{img}" loading="lazy" class="reader-img" alt="Soul Land Chapter {num} Page {i+1}">'
        for i, img in enumerate(imgs)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{COMMON_HEAD}
    <title>Ch.{num:03d} – {title} | {MANGA_NAME}</title>
    <meta name="description" content="Read Soul Land Chapter {num}: {title} online for free. High-quality manga pages with seamless vertical scroll.">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "name": "Chapter {num}: {title}",
      "isPartOf": {{ "@type": "ComicSeries", "name": "{MANGA_NAME}", "url": "{SITE_URL}/" }},
      "url": "{SITE_URL}/manga/Soul Land/{folder}/index.html"
    }}
    </script>
</head>
<body>
    <!-- Reading progress bar -->
    <div id="read-progress"></div>

    <!-- Sticky Nav Bar -->
    <nav class="ch-nav-bar">
        <a href="../../index.html" class="nav-btn" style="font-family:'Cinzel',serif;font-weight:700;color:var(--spirit-blue);">SL</a>
        {prev_link}
        <select class="ch-select" onchange="location.href=this.value">
{select_opts}        </select>
        {next_link}
        <a href="../../index.html" class="nav-btn" style="margin-left:auto;">🏠 Home</a>
    </nav>

    <!-- Chapter Header -->
    <header style="text-align:center;padding:28px 16px 16px;background:linear-gradient(180deg,#0a0a14 60%,transparent);">
        <p style="font-size:0.75rem;letter-spacing:0.15em;color:var(--muted);text-transform:uppercase;margin-bottom:6px;">Soul Land</p>
        <h1 style="font-family:'Cinzel',serif;font-size:clamp(1.2rem,4vw,2rem);font-weight:700;">
            <span style="color:var(--spirit-gold);">Ch.{num:03d}</span> &nbsp;
            <span class="text-grad">{title}</span>
        </h1>
    </header>

    <!-- Reader: full-width webtoon strip -->
    <main id="reader-main">
        {img_tags}
    </main>

    <!-- Bottom Nav -->
    <nav class="ch-nav-bar" style="position:static;margin-top:0;">
        {prev_link}
        <a href="../../index.html" class="nav-btn">🏠 All Chapters</a>
        {next_link}
    </nav>

    <!-- Footer -->
    <footer style="text-align:center;padding:24px;font-size:0.8rem;color:var(--muted);border-top:1px solid var(--border);">
        <p>© 2026 readsoulland.com &nbsp;·&nbsp; Soul Land by Tang Jia San Shao</p>
    </footer>

    {SCROLL_BTNS}

    <script>
      // Reading progress bar
      window.addEventListener('scroll', () => {{
        const doc = document.documentElement;
        const pct = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
        document.getElementById('read-progress').style.width = pct + '%';
      }});
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────────
#  HOME PAGE GENERATOR
# ─────────────────────────────────────────────
def build_home_page(chapters_sorted):
    """Generate the premium homepage HTML."""
    # Build chapter cards (desc order – latest first)
    chapters_desc = sorted(chapters_sorted, key=lambda x: x['num'], reverse=True)
    
    cards_html = ""
    for idx, c in enumerate(chapters_desc):
        hidden = "hidden" if idx >= 50 else ""
        thumb_path = f"./manga/Soul Land/{c['folder']}/{c['thumb']}" if c['thumb'] else ""
        link = f"./manga/Soul Land/{c['folder']}/index.html"
        title = c['title'] or f"Chapter {c['num']}"
        cards_html += f"""        <div class="ch-card {hidden}" data-num="{c['num']}">
            <a href="{link}" style="display:block;text-decoration:none;color:inherit;">
                <div style="aspect-ratio:3/4;position:relative;overflow:hidden;background:#000;">
                    {'<img src="' + thumb_path + '" alt="Ch.' + str(c["num"]) + '" loading="lazy">' if thumb_path else '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:0.75rem;">No Preview</div>'}
                    <div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.85) 0%,rgba(0,0,0,0.1) 60%,transparent 100%);"></div>
                    <div style="position:absolute;bottom:10px;left:10px;">
                        <span style="font-family:'Cinzel',serif;font-size:1rem;font-weight:700;color:#fff;text-shadow:0 2px 8px #000;">Ch.{c['num']:03d}</span>
                        <p style="font-size:0.7rem;color:var(--spirit-blue);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:130px;">{title}</p>
                    </div>
                    <div style="position:absolute;top:8px;right:8px;background:var(--primary);border-radius:999px;padding:2px 10px;font-size:0.65rem;font-weight:700;color:#fff;letter-spacing:0.05em;">READ</div>
                </div>
            </a>
        </div>
"""

    # Search dropdown items
    dropdown_items = ""
    for c in chapters_desc:
        t = c['title'] or f"Chapter {c['num']}"
        dropdown_items += f'<a href="./manga/Soul Land/{c["folder"]}/index.html" class="dropdown-item" style="display:block;padding:10px 20px;border-bottom:1px solid rgba(255,255,255,0.05);color:var(--muted);font-size:0.85rem;text-decoration:none;transition:background 0.2s,color 0.2s;">Ch.{c["num"]:03d} – {t}</a>\n'

    latest = chapters_desc[0] if chapters_desc else None
    latest_link = f'./manga/Soul Land/{latest["folder"]}/index.html' if latest else '#'
    first_link  = f'./manga/Soul Land/{chapters_sorted[0]["folder"]}/index.html' if chapters_sorted else '#'
    total = len(chapters_sorted)

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
{COMMON_HEAD}
    <title>{MANGA_NAME} | Read Online Free – Spirit Awakening</title>
    <meta name="description" content="Read Soul Land: Legend of The Gods' Realm manga online in high quality. {total} chapters available. Join Tang San in a world where spirit power determines destiny.">
    <meta property="og:title" content="{MANGA_NAME}">
    <meta property="og:description" content="Read {total} chapters of Soul Land manga online, free and in HD quality.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ComicSeries",
      "name": "Soul Land",
      "alternateName": ["Douluo Dalu", "Legend of The Gods' Realm"],
      "author": {{ "@type": "Person", "name": "Tang Jia San Shao" }},
      "genre": ["Action","Adventure","Fantasy","Martial Arts"],
      "url": "{SITE_URL}/",
      "numberOfEpisodes": {total}
    }}
    </script>
</head>
<body>

<!-- ── HEADER ── -->
<header class="glass" style="position:fixed;top:0;left:0;width:100%;z-index:500;">
    <div style="max-width:1400px;margin:auto;padding:12px 24px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
        <!-- Logo -->
        <a href="./index.html" style="text-decoration:none;display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--spirit-blue));display:flex;align-items:center;justify-content:center;box-shadow:var(--glow-blue);">
                <span style="font-family:'Cinzel',serif;font-weight:900;font-size:0.9rem;color:#fff;">SL</span>
            </div>
            <span style="font-family:'Cinzel',serif;font-weight:700;font-size:1.15rem;background:linear-gradient(135deg,#fff,var(--spirit-blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Soul Land</span>
        </a>
        <!-- Search -->
        <div style="flex:1;min-width:200px;position:relative;">
            <input id="global-search" type="text" placeholder="🔍  Search chapters..." autocomplete="off"
                style="width:100%;background:rgba(0,0,0,0.6);border:1px solid var(--border);border-radius:999px;padding:9px 18px;color:var(--text);font-size:0.875rem;outline:none;transition:border-color 0.25s;"
                onfocus="this.style.borderColor='var(--spirit-blue)'" onblur="this.style.borderColor='var(--border)'">
            <div id="search-dropdown" style="display:none;position:absolute;top:calc(100% + 6px);left:0;width:100%;background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.8);z-index:600;">
{dropdown_items}            </div>
        </div>
        <!-- CTAs -->
        <a href="{first_link}" style="padding:9px 22px;border-radius:999px;background:linear-gradient(135deg,var(--primary),#6d28d9);color:#fff;font-weight:700;font-size:0.85rem;text-decoration:none;box-shadow:var(--glow-blue);transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">Start Reading</a>
        <a href="{latest_link}" style="padding:9px 22px;border-radius:999px;border:1px solid var(--spirit-gold);color:var(--spirit-gold);font-weight:700;font-size:0.85rem;text-decoration:none;transition:background 0.2s,color 0.2s;" onmouseover="this.style.background='var(--spirit-gold)';this.style.color='#000';" onmouseout="this.style.background='transparent';this.style.color='var(--spirit-gold)';">Latest Ch.{chapters_desc[0]['num']:03d}</a>
    </div>
</header>

<!-- ── HERO ── -->
<section style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:120px 24px 80px;position:relative;overflow:hidden;">
    <!-- Ambient rings -->
    <div style="position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;">
        <div style="position:absolute;top:20%;left:5%;width:600px;height:600px;border-radius:50%;border:40px solid rgba(0,210,255,0.06);animation:float 8s ease-in-out infinite;"></div>
        <div style="position:absolute;bottom:10%;right:5%;width:400px;height:400px;border-radius:50%;border:25px solid rgba(79,70,229,0.08);animation:float 6s ease-in-out infinite 2s;"></div>
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:900px;height:900px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(79,70,229,0.07) 0%,transparent 70%);"></div>
    </div>
    
    <div style="max-width:1200px;width:100%;margin:auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:60px;align-items:center;position:relative;z-index:1;" class="hero-grid">
        <!-- Text -->
        <div>
            <div style="display:inline-block;padding:5px 16px;border-radius:999px;background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);color:var(--spirit-blue);font-size:0.75rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:20px;">{total} Chapters Available</div>
            <h1 style="font-family:'Cinzel',serif;font-size:clamp(2.2rem,5vw,4.5rem);font-weight:900;line-height:1.1;margin-bottom:20px;">
                Awaken Your<br>
                <span class="text-grad">Spirit Power</span>
            </h1>
            <p style="color:var(--muted);font-size:1.05rem;line-height:1.7;max-width:480px;margin-bottom:36px;">Tang San is reborn in Douluo Dalu — a world where everyone awakens a martial spirit and power determines destiny. The legend of the Tang Sect begins here.</p>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
                <a href="{first_link}" style="padding:14px 32px;border-radius:999px;background:linear-gradient(135deg,var(--primary),var(--spirit-blue));color:#fff;font-weight:700;font-size:1rem;text-decoration:none;box-shadow:0 0 30px rgba(79,70,229,0.5);transition:transform 0.2s,box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 0 50px rgba(0,210,255,0.5)'" onmouseout="this.style.transform='none';this.style.boxShadow='0 0 30px rgba(79,70,229,0.5)'">⚡ Awaken (Ch.001)</a>
                <a href="{latest_link}" style="padding:14px 32px;border-radius:999px;border:2px solid var(--spirit-gold);color:var(--spirit-gold);font-weight:700;font-size:1rem;text-decoration:none;transition:all 0.2s;" onmouseover="this.style.background='var(--spirit-gold)';this.style.color='#000';" onmouseout="this.style.background='transparent';this.style.color='var(--spirit-gold)';">Latest Chapter →</a>
            </div>
        </div>
        <!-- Cover art -->
        <div style="display:flex;justify-content:center;">
            <div style="width:100%;max-width:320px;aspect-ratio:3/4;border-radius:20px;overflow:hidden;border:2px solid var(--border);box-shadow:0 0 60px rgba(79,70,229,0.3),0 0 120px rgba(0,210,255,0.1);animation:pulse-glow 4s ease-in-out infinite;position:relative;">
                <img src="./soul_land_hero_art.png" alt="Soul Land Key Art" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display='none'">
                <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 60%,var(--darkbg));"></div>
                <div style="position:absolute;bottom:16px;left:16px;right:16px;text-align:center;">
                    <p style="font-family:'Cinzel',serif;font-size:1.1rem;font-weight:700;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,0.8);">{MANGA_NAME}</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ── CHAPTER GRID ── -->
<section style="padding:60px 24px 100px;background:linear-gradient(to bottom,var(--darkbg),var(--surface));">
    <div style="max-width:1400px;margin:auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;margin-bottom:36px;padding-bottom:20px;border-bottom:1px solid var(--border);">
            <div>
                <h2 style="font-family:'Cinzel',serif;font-size:2rem;font-weight:700;display:flex;align-items:center;gap:12px;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--spirit-blue)"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    <span class="text-grad">Chapter Archive</span>
                </h2>
                <p style="color:var(--muted);font-size:0.9rem;margin-top:4px;">{total} chapters of Tang San's epic journey</p>
            </div>
            <div style="display:flex;gap:12px;">
                <button id="btn-asc"  onclick="sortGrid(true)"  style="padding:9px 22px;border-radius:999px;border:1px solid var(--border);background:var(--surface);color:var(--muted);font-size:0.85rem;cursor:pointer;transition:all 0.2s;">↑ Oldest First</button>
                <button id="btn-desc" onclick="sortGrid(false)" style="padding:9px 22px;border-radius:999px;border:1px solid var(--spirit-blue);background:rgba(0,210,255,0.1);color:var(--spirit-blue);font-weight:700;font-size:0.85rem;cursor:pointer;transition:all 0.2s;">↓ Newest First</button>
            </div>
        </div>

        <!-- Grid -->
        <div id="ch-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:16px;">
{cards_html}
        </div>

        <!-- Load more -->
        <div id="load-more-wrap" style="text-align:center;margin-top:48px;">
            <button id="btn-load" onclick="loadAll()" style="padding:14px 48px;border-radius:999px;background:var(--surface);border:1px solid var(--primary);color:var(--primary);font-weight:700;font-size:0.95rem;cursor:pointer;transition:all 0.3s;box-shadow:0 0 20px rgba(79,70,229,0.15);" onmouseover="this.style.background='var(--primary)';this.style.color='#fff';" onmouseout="this.style.background='var(--surface)';this.style.color='var(--primary)';">Load All {total} Chapters</button>
        </div>
    </div>
</section>

<!-- ── FOOTER ── -->
<footer style="background:#050508;padding:40px 24px;border-top:1px solid var(--border);text-align:center;">
    <p style="font-family:'Cinzel',serif;font-weight:700;font-size:1.1rem;color:#fff;margin-bottom:8px;">Soul Land Online</p>
    <p style="color:var(--muted);font-size:0.85rem;">© 2026 readsoulland.com &nbsp;·&nbsp; {total} Chapters &nbsp;·&nbsp; Author: Tang Jia San Shao</p>
    <div style="margin-top:16px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap;">
        <a href="./chapters.html" style="color:var(--muted);text-decoration:none;font-size:0.85rem;transition:color 0.2s;" onmouseover="this.style.color='var(--spirit-blue)'" onmouseout="this.style.color='var(--muted)'">All Chapters</a>
        <a href="./characters.html" style="color:var(--muted);text-decoration:none;font-size:0.85rem;transition:color 0.2s;" onmouseover="this.style.color='var(--spirit-blue)'" onmouseout="this.style.color='var(--muted)'">Characters</a>
        <a href="./privacy-policy.html" style="color:var(--muted);text-decoration:none;font-size:0.85rem;transition:color 0.2s;" onmouseover="this.style.color='var(--spirit-blue)'" onmouseout="this.style.color='var(--muted)'">Privacy</a>
        <a href="./dmca.html" style="color:var(--muted);text-decoration:none;font-size:0.85rem;transition:color 0.2s;" onmouseover="this.style.color='var(--spirit-blue)'" onmouseout="this.style.color='var(--muted)'">DMCA</a>
    </div>
</footer>

{SCROLL_BTNS}

<style>
@media(max-width:768px){{
  .hero-grid{{grid-template-columns:1fr!important;}}
}}
</style>

<script>
// ── SEARCH DROPDOWN ──
const searchInput = document.getElementById('global-search');
const dropdown    = document.getElementById('search-dropdown');
const dropItems   = dropdown.querySelectorAll('.dropdown-item');

function showDropdown() {{ dropdown.style.display = 'block'; }}
function hideDropdown() {{ dropdown.style.display = 'none'; }}

searchInput.addEventListener('focus', showDropdown);
searchInput.addEventListener('input', () => {{
    const q = searchInput.value.toLowerCase();
    showDropdown();
    dropItems.forEach(el => {{
        el.style.display = el.textContent.toLowerCase().includes(q) ? 'block' : 'none';
    }});
}});
document.addEventListener('click', e => {{
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) hideDropdown();
}});
searchInput.addEventListener('keydown', e => {{ if (e.key === 'Escape') hideDropdown(); }});

// ── GRID SORT ──
const grid  = document.getElementById('ch-grid');
let   cards = Array.from(grid.querySelectorAll('.ch-card'));
let   asc   = false;

function setActive(isAsc) {{
    const on  = 'padding:9px 22px;border-radius:999px;border:1px solid var(--spirit-blue);background:rgba(0,210,255,0.1);color:var(--spirit-blue);font-weight:700;font-size:0.85rem;cursor:pointer;transition:all 0.2s;';
    const off = 'padding:9px 22px;border-radius:999px;border:1px solid var(--border);background:var(--surface);color:var(--muted);font-size:0.85rem;cursor:pointer;transition:all 0.2s;';
    document.getElementById('btn-asc').style.cssText  = isAsc  ? on : off;
    document.getElementById('btn-desc').style.cssText = !isAsc ? on : off;
}}

function sortGrid(ascending) {{
    asc = ascending;
    cards.sort((a,b) => {{
        const na = parseInt(a.dataset.num), nb = parseInt(b.dataset.num);
        return ascending ? na - nb : nb - na;
    }});
    cards.forEach(c => grid.appendChild(c));
    limitDisplay();
    setActive(ascending);
}}

function limitDisplay() {{
    cards.forEach((c, i) => c.classList.toggle('hidden', i >= 50));
    document.getElementById('load-more-wrap').style.display = 'block';
}}

function loadAll() {{
    cards.forEach(c => c.classList.remove('hidden'));
    document.getElementById('load-more-wrap').style.display = 'none';
}}

// Init: show first 50 already done by class, just hide load-btn if <=50 total
if (cards.length <= 50) document.getElementById('load-more-wrap').style.display = 'none';
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
#  SITEMAP GENERATOR
# ─────────────────────────────────────────────
def build_sitemap(chapters_sorted):
    today = "2026-04-16"
    entries = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
  <url><loc>{SITE_URL}/index.html</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>{SITE_URL}/chapters.html</loc><lastmod>{today}</lastmod><changefreq>hourly</changefreq><priority>0.8</priority></url>
  <url><loc>{SITE_URL}/characters.html</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>
  <url><loc>{SITE_URL}/settings.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>
"""
    for c in chapters_sorted:
        path = urllib.parse.quote(f"manga/Soul Land/{c['folder']}/index.html")
        entries += f"  <url><loc>{SITE_URL}/{path}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n"
    entries += "</urlset>"
    return entries

# ─────────────────────────────────────────────
#  CHAPTERS_DATA.JS GENERATOR
# ─────────────────────────────────────────────
def build_chapters_data_js(chapters_sorted):
    data = {}
    for c in chapters_sorted:
        if c['thumb']:
            data[str(c['num'])] = f"/manga/Soul Land/{c['folder']}/{c['thumb']}"
    return "const chaptersData = " + json.dumps(data, indent=2) + ";"

# ─────────────────────────────────────────────
#  MAIN BUILD
# ─────────────────────────────────────────────
def build_project():
    if not os.path.isdir(MANGA_DIR):
        print(f"ERROR: Manga directory not found:\n  {MANGA_DIR}")
        return

    # 1. Discover all chapter folders
    folders = [f for f in os.listdir(MANGA_DIR)
               if os.path.isdir(os.path.join(MANGA_DIR, f)) and re.match(r'Ch\.\d+', f)]
    
    chapters = []
    for folder in folders:
        num    = extract_chapter_number(folder)
        title  = extract_chapter_title(folder)
        imgs   = get_images(os.path.join(MANGA_DIR, folder))
        thumb  = imgs[0] if imgs else ''
        chapters.append({'num': num, 'folder': folder, 'title': title, 'images': imgs, 'thumb': thumb})

    chapters_sorted = sorted(chapters, key=lambda x: x['num'])
    print(f"  Found {len(chapters_sorted)} chapters.")

    # 2. Generate individual chapter index.html files
    print("  Building chapter reader pages...")
    for i, c in enumerate(chapters_sorted):
        out_path = os.path.join(MANGA_DIR, c['folder'], "index.html")
        html = build_chapter_page(c, chapters_sorted)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        if (i + 1) % 50 == 0:
            print(f"    ... {i+1} chapters done")

    # 3. Generate chapters_data.js in assets
    js_dir = os.path.join(ROOT_DIR, "assets", "js")
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, "chapters_data.js"), "w", encoding="utf-8") as f:
        f.write(build_chapters_data_js(chapters_sorted))
    print("  chapters_data.js written.")

    # 4. Generate homepage (root index.html)
    with open(os.path.join(ROOT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_home_page(chapters_sorted))
    print("  Homepage written.")

    # 5. Generate sitemap.xml (root)
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap(chapters_sorted))
    print("  sitemap.xml written.")

    print(f"\nBuild complete! {len(chapters_sorted)} chapter pages generated.")

if __name__ == "__main__":
    build_project()
