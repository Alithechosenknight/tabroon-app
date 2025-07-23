import streamlit as st
from firebase_config import db  # custom module with firebase_admin or pyrebase init
import uuid
import base64
import datetime

# ────────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & THEME
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🏆 Kuwait Football App", layout="wide")

st.markdown(
    f"""
    <style>
    :root {{
      --main-yellow: #F9C80E;
      --main-bg: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
      --header-bg: rgba(20,30,50,0.95);
      --card-bg: rgba(255,255,255,0.10);
      --shadow: 0 4px 24px #0002;
    }}

    html, body, [class*='css'] {{
      background: var(--main-bg);
      color: #fff;
      min-height: 100vh;
      font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
      scroll-behavior: smooth;
    }}

    .stApp {{
      background: url('https://www.transparenttextures.com/patterns/football-no-lines.png'), var(--main-bg);
      background-blend-mode: overlay;
    }}

    .main-header-bar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--header-bg);
      box-shadow: 0 2px 16px 0 #0006;
      border-bottom: 2px solid var(--main-yellow);
      padding: 0.5rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: background 0.3s;
    }}

    .main-header-bar img {{
      border-radius: 50%;
      box-shadow: 0 2px 8px #0004;
      width: 60px;
      height: 60px;
      object-fit: cover;
    }}

    .main-header-title {{
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: 1px;
      color: var(--main-yellow);
      margin: 0;
      transition: font-size 0.2s;
    }}

    .lang-toggle {{
      font-size: 1.1rem;
      font-weight: 600;
      color: #fff;
      background: var(--main-yellow);
      border-radius: 8px;
      padding: 0.2rem 1rem;
      border: none;
      margin-left: 1rem;
      cursor: pointer;
      transition: background 0.2s;
    }}

    .lang-toggle:hover, .lang-toggle:focus {{
      background: #ffe066;
      color: #222;
    }}

    .stSidebar {{
      background: rgba(20,30,50,0.98);
      border-right: 2px solid var(--main-yellow);
    }}

    .sidebar-avatar {{
      width: 70px;
      height: 70px;
      border-radius: 50%;
      border: 3px solid var(--main-yellow);
      margin-bottom: 1rem;
      object-fit: cover;
    }}

    .sidebar-active {{
      background: #F9C80E22;
      border-radius: 8px;
    }}

    .stButton>button {{
      background: var(--main-yellow)!important;
      color: #000;
      font-weight: 600;
      border-radius: 8px;
      border: none;
      box-shadow: 0 2px 8px #0002;
      transition: background 0.2s, transform 0.2s;
    }}

    .stButton>button:hover, .stButton>button:focus {{
      background: #ffe066!important;
      transform: scale(1.04);
    }}

    .card {{
      background: var(--card-bg);
      padding: 1.2rem 1.5rem;
      border-left: 6px solid var(--main-yellow);
      border-radius: 16px;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow);
      position: relative;
      transition: box-shadow 0.2s, transform 0.2s;
      will-change: box-shadow, transform;
    }}

    .card:hover {{
      box-shadow: 0 8px 32px #F9C80E44;
      transform: translateY(-2px) scale(1.01);
    }}

    @media (max-width: 900px) {{
      .main-header-title {{ font-size: 1.5rem; }}
      .main-header-bar {{ flex-direction: column; align-items: flex-start; }}
      .card {{ padding: 1rem; }}
    }}

    @media (max-width: 600px) {{
      .main-header-title {{ font-size: 1.1rem; }}
      .main-header-bar {{ padding: 0.5rem 1rem; }}
      .card {{ padding: 0.7rem; }}
      .sidebar-avatar {{ width: 50px; height: 50px; }}
    }}
    .player-badge {{
        display: inline-block; background: var(--main-yellow); color: #222; font-size: 0.9rem; font-weight: 700;
        border-radius: 6px; padding: 0.1rem 0.7rem; margin-left: 0.5rem;
    }}
    .player-icons {{ font-size: 1.1rem; margin-right: 0.3rem; color: var(--main-yellow); }}
    .divider {{ border-top: 2px dashed #F9C80E33; margin: 2rem 0; }}
    .section-title {{ font-size: 1.5rem; font-weight: 700; color: var(--main-yellow); margin-bottom: 1rem; }}
    .watermark-bg {{
        position: fixed; left: 0; top: 0; width: 100vw; height: 100vh; z-index: 0;
        background: url('https://cdn.pixabay.com/photo/2013/07/13/12/46/soccer-146674_1280.png') center/40vw no-repeat;
        opacity: 0.04;
        pointer-events: none;
    }}
    </style>
    <div class='watermark-bg'></div>
    """,
    unsafe_allow_html=True,
)

# ────────────────────────────────────────────────────────────────────────────────
# SESSION STATE HELPERS
# ────────────────────────────────────────────────────────────────────────────────
SS = st.session_state
SS.setdefault("user", None)          # firebase user dict
SS.setdefault("page", "main")        # routing
SS.setdefault("active_chat", None)    # conversation id
SS.setdefault("lang", "en")
lang = st.sidebar.selectbox("🌐 اللغة / Language", ["English", "العربية"], key="lang_toggle")
SS["lang"] = "ar" if lang == "العربية" else "en"

# Translation dictionary with expanded keys and Kuwaiti Arabic
T = {
    "en": {
        "login": "Login or Register",
        "home": "Home",
        "dashboard": "Dashboard",
        "messages": "Messages",
        "challenges": "Challenges",
        "logout": "Logout",
        "team_name": "Team Name",
        "player_name": "Player Name",
        "add_player": "Add Player",
        "create_team": "Create Team",
        "edit_team": "Edit Teams",
        "create_team_first": "Create a team first.",
        "no_teams_edit": "No teams to edit.",
        "save_profile": "Save Profile",
        "profile_updated": "Profile updated!",
        "height": "Height (cm)",
        "weight": "Weight (kg)",
        "my_teams": "My Teams",
        "add_player_to_team": "Add Player",
        "select_team": "Select Team",
        "player_name": "Player Name",
        "age": "Age",
        "position": "Position",
        "preferred_foot": "Preferred Foot",
        "right": "Right",
        "left": "Left",
        "ready_to_play": "Ready to play",
        "upload_image": "Upload Image",
        "add_player_btn": "Add Player",
        "player_added": "Player added!",
        "edit_teams": "Edit Teams",
        "select_team_edit": "Select Team",
        "new_team_name": "New Team Name",
        "new_logo": "New Logo",
        "save_changes": "Save Changes",
        "team_updated": "Team updated!",
        "latest_articles": "Latest Football Articles",
        "improve_dribbling": "How to improve your dribbling skills",
        "best_stadiums": "Best football stadiums in Kuwait",
        "top_young_stars": "Top 5 young football stars to watch",
        "teams_in_league": "Teams in Kuwait Football League",
        "login_required": "Login required.",
        "please_login": "Please login first.",
        "go_to_login": "Go to Login",
        "contacts": "Contacts",
        "chat_with": "Chat with {user}",
        "type_message": "Type a message",
        "send": "Send",
        "invalid_credentials": "Invalid credentials",
        "account_created": "Account created! Please login.",
        "issue_challenge": "Issue a Challenge",
        "your_team": "Your Team",
        "opponent": "Opponent",
        "message_details": "Message / Details",
        "send_challenge": "Send Challenge",
        "challenge_sent": "Challenge sent!",
        "need_teams": "Need at least one of your team and another team in league.",
        "incoming_challenges": "Incoming Challenges",
        "accept": "Accept",
        "reject": "Reject",
        "status": "Status",
        "challenge_history": "Challenge History",
        "from_on_status": "From {name} on {date}: Status — {status}",
        "challenged_you": "{name} challenged you: {msg}",
        "main_title": "🏆 Kuwait Football App",
        "navigation": "Navigation",
        "login_register": "Login / Register",
        "logout_btn": "Logout",
        "home_btn": "Home",
        "dashboard_btn": "Dashboard",
        "messages_btn": "Messages",
        "challenges_btn": "Challenges",
        "profile": "Profile",
        "edit_teams_tab": "Edit Teams",
        "create_team_tab": "Create Team",
        "add_player_tab": "Add Player",
        "welcome": "Welcome, {username}",
        "delete": "Delete",
    },
    "ar": {
        "login": "دخول أو تسجيل",
        "home": "الرئيسية",
        "dashboard": "لوحة التحكم",
        "messages": "الرسائل",
        "challenges": "التحديات",
        "logout": "تسجيل خروج",
        "team_name": "اسم الفريق",
        "player_name": "اسم اللاعب",
        "add_player": "ضيف لاعب",
        "create_team": "سوي فريق",
        "edit_team": "عدل الفرق",
        "create_team_first": "سوي فريق أول شي.",
        "no_teams_edit": "ما عندك فرق تعدلها.",
        "save_profile": "حفظ الملف الشخصي",
        "profile_updated": "تم تحديث الملف!",
        "height": "الطول (سم)",
        "weight": "الوزن (كجم)",
        "my_teams": "فرقي",
        "add_player_to_team": "ضيف لاعب",
        "select_team": "اختار فريق",
        "player_name": "اسم اللاعب",
        "age": "العمر",
        "position": "المركز",
        "preferred_foot": "الرجل المفضلة",
        "right": "يمين",
        "left": "يسار",
        "ready_to_play": "جاهز يلعب",
        "upload_image": "رفع صورة",
        "add_player_btn": "ضيف اللاعب",
        "player_added": "تم إضافة اللاعب!",
        "edit_teams": "عدل الفرق",
        "select_team_edit": "اختار فريق",
        "new_team_name": "اسم الفريق الجديد",
        "new_logo": "شعار جديد",
        "save_changes": "حفظ التغييرات",
        "team_updated": "تم تحديث الفريق!",
        "latest_articles": "آخر مقالات الكرة",
        "improve_dribbling": "شلون تطور مهاراتك بالمراوغة",
        "best_stadiums": "أفضل ملاعب الكويت",
        "top_young_stars": "أفضل ٥ لاعبين شباب تتابعهم",
        "teams_in_league": "فرق الدوري الكويتي",
        "login_required": "لازم تسجل دخول.",
        "please_login": "سجل دخول أول شي.",
        "go_to_login": "روح للتسجيل",
        "contacts": "جهات الاتصال",
        "chat_with": "دردشة مع {user}",
        "type_message": "اكتب رسالة",
        "send": "إرسال",
        "invalid_credentials": "بيانات الدخول غلط",
        "account_created": "تم إنشاء الحساب! سجل دخولك.",
        "issue_challenge": "تحد فريق",
        "your_team": "فريقك",
        "opponent": "الفريق الثاني",
        "message_details": "رسالة / تفاصيل",
        "send_challenge": "ارسل التحدي",
        "challenge_sent": "تم إرسال التحدي!",
        "need_teams": "لازم يكون عندك فريق وفريق ثاني بالدوري.",
        "incoming_challenges": "تحديات جايتك",
        "accept": "أقبل",
        "reject": "أرفض",
        "status": "الحالة",
        "challenge_history": "سجل التحديات",
        "from_on_status": "من {name} بتاريخ {date}: الحالة — {status}",
        "challenged_you": "{name} تحداك: {msg}",
        "main_title": "🏆 تطبيق كورة الكويت",
        "navigation": "التنقل",
        "login_register": "دخول / تسجيل",
        "logout_btn": "تسجيل خروج",
        "home_btn": "الرئيسية",
        "dashboard_btn": "لوحة التحكم",
        "messages_btn": "الرسائل",
        "challenges_btn": "التحديات",
        "profile": "الملف الشخصي",
        "edit_teams_tab": "عدل الفرق",
        "create_team_tab": "سوي فريق",
        "add_player_tab": "ضيف لاعب",
        "welcome": "هلا {username}",
        "delete": "حذف",
    },
}

T["en"].update({
    "location": "Location",
    "matches": "Matches",
    "no_matches": "No matches scheduled.",
    "no_articles": "No articles yet.",
})
T["ar"].update({
    "location": "المكان",
    "matches": "المباريات",
    "no_matches": "لا توجد مباريات.",
    "no_articles": "لا توجد مقالات بعد.",
})

ADMIN_EMAIL = "3lo0oialsharefe@gmail.com"

def is_admin():
    return SS.get("user") and SS["user"].get("email") == ADMIN_EMAIL

def tr(key, **kwargs):
    txt = T[SS["lang"]].get(key, key)
    if txt is None:
        txt = key
    if kwargs:
        return txt.format(**kwargs)
    return txt

# Add RTL CSS for Arabic
if SS["lang"] == "ar":
    st.markdown(
        """
        <style>
        html, body, [class*='css'] { direction: rtl; text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def reroute(page: str):
    SS["page"] = page
    st.rerun()

# ────────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ────────────────────────────────────────────────────────────────────────────────

def header():
    st.markdown(
        f"""
        <div class='main-header-bar'>
            <div style='display:flex;align-items:center;'>
                <img src='https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Kuwait_FA_logo.svg/1200px-Kuwait_FA_logo.svg.png' width='60' style='margin-right:18px;'>
                <span class='main-header-title'>{tr('main_title')}</span>
            </div>
            <div style='display:flex;align-items:center;'>
                <form action='#' method='post'>
                    <select onchange='this.form.submit()' name='lang' class='lang-toggle'>
                        <option value='en' {'selected' if SS['lang']=='en' else ''}>English</option>
                        <option value='ar' {'selected' if SS['lang']=='ar' else ''}>العربية</option>
                    </select>
                </form>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def sidebar():
    with st.sidebar:
        st.markdown(f"<div style='text-align:center;margin-bottom:1.5rem;'>"
                    f"<img src='https://www.bornfree.org.uk/wp-content/uploads/2023/09/Web-image-iStock-492611032-1024x683.jpg' class='sidebar-avatar'>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"## {tr('navigation')}")
        def nav_btn(label, icon, page):
            active = SS["page"] == page
            style = 'sidebar-active' if active else ''
            st.markdown(f"<div class='{style}'>", unsafe_allow_html=True)
            st.button(f"{icon} {label}", on_click=reroute, args=(page,))
            st.markdown("</div>", unsafe_allow_html=True)
        if SS["user"]:
            nav_btn(tr('home_btn'), '🏠', 'main')
            nav_btn(tr('dashboard_btn'), '📋', 'dashboard')
            nav_btn(tr('messages_btn'), '💬', 'messages')
            nav_btn(tr('challenges_btn'), '⚔️', 'challenges')
            if is_admin():
                nav_btn(tr('admin'), '🛡️', 'admin')
            st.button(f"🚪 {tr('logout_btn')}", on_click=logout)
        else:
            st.button(f"🔐 {tr('login_register')}", on_click=reroute, args=("login",))

def logout():
    SS["user"] = None
    reroute("main")

# ────────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION PAGES
# ────────────────────────────────────────────────────────────────────────────────

def page_login():
    st.header(tr("login"))
    option = st.radio(tr("login"), [tr("login"), tr("create_team")])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if option == tr("create_team"):
        username = st.text_input(tr("player_name"))
        if st.button(tr("login_register")):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                uid = user["localId"]
                db.collection("users").document(uid).set({
                    "username": username,
                    "email": email,
                    "profile": {},
                })
                st.success(tr("account_created"))
            except Exception as e:
                st.error(e)
    else:  # Login
        if st.button(tr("login")):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                SS["user"] = user
                reroute("dashboard")
            except Exception:
                st.error(tr("invalid_credentials"))


# ────────────────────────────────────────────────────────────────────────────────
# MAIN LANDING PAGE
# ────────────────────────────────────────────────────────────────────────────────

def page_main():
    st.header(f"📖 {tr('latest_articles')}")
    # Articles horizontal scroll
    articles = list(db.collection("articles").stream())
    if articles:
        st.markdown("""
        <div style='display:flex;flex-direction:row;overflow-x:auto;gap:2rem;padding-bottom:1rem;'>
        """, unsafe_allow_html=True)
        for a in articles:
            ad = a.to_dict() or {}
            st.markdown(f"""
            <div class='card' style='min-width:320px;max-width:320px;flex:0 0 320px;display:flex;flex-direction:column;align-items:center;'>
                {f'<img src="data:image/png;base64,{ad.get('image_base64','')}" style="width:100%;border-radius:12px 12px 0 0;">' if ad.get('image_base64') else ''}
                <h4 style='color:#F9C80E;margin:0.5rem 0 0.2rem 0'>{ad.get('title', tr('article_title'))}</h4>
                <div style='font-size:1rem;color:#fff;text-align:center'>{ad.get('content', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(tr("no_articles"))
    st.divider()
    st.header(f"🏟️ {tr('matches')}")
    # Matches horizontal scroll
    matches = list(db.collection("matches").stream())
    if matches:
        st.markdown("""
        <div style='display:flex;flex-direction:row;overflow-x:auto;gap:2rem;padding-bottom:1rem;'>
        """, unsafe_allow_html=True)
        for m in matches:
            md = m.to_dict() or {}
            st.markdown(f"""
            <div class='card' style='min-width:260px;max-width:260px;flex:0 0 260px;display:flex;flex-direction:column;align-items:center;'>
                <h4 style='color:#F9C80E;margin:0.5rem 0 0.2rem 0'>{md.get('team1','?')} <span style='color:#fff'>vs</span> {md.get('team2','?')}</h4>
                <div style='font-size:1rem;color:#fff;text-align:center'><b>{tr('match_date')}:</b> {md.get('date','?')}</div>
                <div style='font-size:1rem;color:#fff;text-align:center'><b>{tr('location')}:</b> {md.get('location','-')}</div>
                <div style='font-size:1rem;color:#fff;text-align:center'><b>{tr('status')}:</b> {md.get('status','?')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(tr("no_matches"))
    st.divider()
    st.header(f"⚽ {tr('teams_in_league')}")
    teams = db.collection("teams").stream()
    for t in teams:
        data = t.to_dict() or {}
        logo = data.get("logo_base64")
        with st.container():
            st.markdown(f"<div class='card'><h3>📌 {data.get('name',tr('team_name'))}</h3>", unsafe_allow_html=True)
            if logo:
                st.image(base64.b64decode(logo), width=120)
            players = db.collection("teams").document(t.id).collection("players").stream()
            for p in players:
                pd = p.to_dict() or {}
                player_img = pd.get("image_base64")
                cols = st.columns([1, 4])
                with cols[0]:
                    if player_img:
                        st.image(base64.b64decode(player_img), width=70)
                    else:
                        st.markdown("<div style='width:70px;height:70px;border:2px dashed #F9C80E;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2rem;'>⚽</div>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"<span style='font-size:1.1rem;font-weight:700;'>{pd.get('name',tr('player_name'))}</span> "
                                f"<span class='player-badge'>{pd.get('position','?')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='player-icons'>🎂</span> {tr('age')} {pd.get('age','?')}  "
                                f"<span class='player-icons'>📏</span> {tr('height')} {pd.get('height','?')}cm  "
                                f"<span class='player-icons'>⚖️</span> {tr('weight')} {pd.get('weight','?')}kg  "
                                f"<span class='player-icons'>🦶</span> {tr('preferred_foot')}: {pd.get('foot','?')}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────────
# DASHBOARD (PROFILE & TEAM MGMT)
# ────────────────────────────────────────────────────────────────────────────────

def page_dashboard():
    if not SS["user"]:
        st.warning(tr("please_login"))
        if st.button(tr("go_to_login")):
            reroute("login")
        return
    uid = SS["user"]["localId"]
    user_doc = db.collection("users").document(uid).get()
    udata = user_doc.to_dict() or {}
    st.header(tr("welcome", username=udata.get('username',tr('player_name'))))
    tab1, tab2, tab3 = st.tabs([f"👤 {tr('profile')}", f"⚽ {tr('my_teams')}", f"🖼️ {tr('edit_teams_tab')}"])

    # ── Profile ──────────────────
    with tab1:
        profile = udata.get("profile", {})
        h = st.number_input(tr("height"), 100, 250, value=int(profile.get("height", 170)))
        w = st.number_input(tr("weight"), 30, 200, value=int(profile.get("weight", 70)))
        if st.button(tr("save_profile")):
            db.collection("users").document(uid).update({"profile": {"height": h, "weight": w}})
            st.success(tr("profile_updated"))

    # ── My Teams (Create & Add Players) ──────────────────
    with tab2:
        st.subheader(f"➕ {tr('create_team_tab')}")
        tname = st.text_input(tr("team_name"))
        if st.button(tr("create_team")) and tname:
            tid = str(uuid.uuid4())
            db.collection("teams").document(tid).set({"name": tname, "created_by": uid})
            st.success(tr("create_team") + f" '{tname}' " + tr("team_updated"))
        st.divider()
        st.subheader(f"➕ {tr('add_player_tab')}")
        team_docs = db.collection("teams").where("created_by", "==", uid).stream()
        tdict = {d.id: (d.to_dict() or {}).get("name", tr("team_name")) for d in team_docs}
        if tdict:
            sel_team_name = st.selectbox(tr("select_team"), list(tdict.values()), key="add_player_team_select")
            sel_team_id = next(k for k, v in tdict.items() if v == sel_team_name)
            pname = st.text_input(tr("player_name"))
            age = st.slider(tr("age"), 10, 60, 20)
            pos = st.selectbox(tr("position"), [tr("goalkeeper") if 'goalkeeper' in T[SS['lang']] else "Goalkeeper", tr("defender") if 'defender' in T[SS['lang']] else "Defender", tr("midfielder") if 'midfielder' in T[SS['lang']] else "Midfielder", tr("forward") if 'forward' in T[SS['lang']] else "Forward"])
            foot = st.radio(tr("preferred_foot"), [tr("right"), tr("left")])
            ready = st.checkbox(tr("ready_to_play"), True)
            ph, pw = st.columns(2)
            with ph:
                height = st.number_input(tr("height"), 100, 250, 175)
            with pw:
                weight = st.number_input(tr("weight"), 30, 150, 70)
            pimg = st.file_uploader(tr("upload_image"), ["jpg", "jpeg", "png"])
            img64 = base64.b64encode(pimg.read()).decode() if pimg else None
            if st.button(tr("add_player_btn")):
                pid = str(uuid.uuid4())
                db.collection("teams").document(sel_team_id).collection("players").document(pid).set({
                    "name": pname,
                    "age": age,
                    "position": pos,
                    "ready": ready,
                    "foot": foot,
                    "height": height,
                    "weight": weight,
                    "image_base64": img64,
                })
                st.success(tr("player_added"))
        else:
            st.info(tr("create_team_first"))

    # ── Edit Teams ──────────────────
    with tab3:
        teams_edit = db.collection("teams").where("created_by", "==", uid).stream()
        edit_dict = {d.id: (d.to_dict() or {}).get("name", tr("team_name")) for d in teams_edit}
        if edit_dict:
            ename = st.selectbox(tr("select_team_edit"), list(edit_dict.values()), key="edit_team_select")
            eid = next(k for k, v in edit_dict.items() if v == ename)
            team_doc = db.collection("teams").document(eid).get()
            team_data = team_doc.to_dict() or {}
            new_name = st.text_input(tr("new_team_name"), value=team_data.get("name", ename))

            logo = st.file_uploader(tr("new_logo"), ["jpg", "jpeg", "png"])
            logo64 = base64.b64encode(logo.read()).decode() if logo else None
            if st.button(tr("save_changes")):
                upd = {"name": new_name}
                if logo64:
                    upd["logo_base64"] = logo64
                db.collection("teams").document(eid).update(upd)
                st.success(tr("team_updated"))

            # --- Player Management ---
            st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)
            st.subheader(tr("add_player_tab") + " / " + tr("edit_team"))
            players_ref = db.collection("teams").document(eid).collection("players")
            players = list(players_ref.stream())
            for p in players:
                pd = p.to_dict() or {}
                pid = p.id
                with st.expander(f"{pd.get('name', tr('player_name'))}"):
                    cols = st.columns([1, 3, 1])
                    with cols[0]:
                        if pd.get("image_base64"):
                            st.image(base64.b64decode(pd["image_base64"]), width=70)
                        else:
                            st.markdown("<div style='width:70px;height:70px;border:2px dashed #F9C80E;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2rem;'>⚽</div>", unsafe_allow_html=True)
                    with cols[1]:
                        pname = st.text_input(tr("player_name"), value=pd.get("name", ""), key=f"edit_name_{pid}")
                        age = st.slider(tr("age"), 10, 60, int(pd.get("age", 20)), key=f"edit_age_{pid}")
                        pos = st.selectbox(tr("position"), [tr("goalkeeper") if 'goalkeeper' in T[SS['lang']] else "Goalkeeper", tr("defender") if 'defender' in T[SS['lang']] else "Defender", tr("midfielder") if 'midfielder' in T[SS['lang']] else "Midfielder", tr("forward") if 'forward' in T[SS['lang']] else "Forward"], index=[tr("goalkeeper"),tr("defender"),tr("midfielder"),tr("forward")].index(pd.get("position", tr("midfielder"))) if pd.get("position") in [tr("goalkeeper"),tr("defender"),tr("midfielder"),tr("forward")] else 2, key=f"edit_pos_{pid}")
                        foot = st.radio(tr("preferred_foot"), [tr("right"), tr("left")], index=0 if pd.get("foot", "Right")==tr("right") else 1, key=f"edit_foot_{pid}")
                        ready = st.checkbox(tr("ready_to_play"), value=pd.get("ready", True), key=f"edit_ready_{pid}")
                        height = st.number_input(tr("height"), 100, 250, int(pd.get("height", 170)), key=f"edit_height_{pid}")
                        weight = st.number_input(tr("weight"), 30, 150, int(pd.get("weight", 70)), key=f"edit_weight_{pid}")
                        pimg = st.file_uploader(tr("upload_image"), ["jpg", "jpeg", "png"], key=f"edit_img_{pid}")
                        img64 = base64.b64encode(pimg.read()).decode() if pimg else pd.get("image_base64")
                        if st.button(tr("save_changes"), key=f"save_player_{pid}"):
                            players_ref.document(pid).update({
                                "name": pname,
                                "age": age,
                                "position": pos,
                                "foot": foot,
                                "ready": ready,
                                "height": height,
                                "weight": weight,
                                "image_base64": img64,
                            })
                            st.success(tr("player_added"))
                            st.rerun()
                    with cols[2]:
                        confirm_key = f"delete_confirm_{pid}"
                        if st.button("🗑️", key=f"delete_{pid}"):
                            SS[confirm_key] = True
                        if SS.get(confirm_key):
                            if st.checkbox(tr("delete") + f" {pname}?", key=f"confirm_box_{pid}"):
                                players_ref.document(pid).delete()
                                st.success(tr("player_name") + " " + tr("delete"))
                                SS[confirm_key] = False
                                st.rerun()
        else:
            st.info(tr("no_teams_edit"))


# ────────────────────────────────────────────────────────────────────────────────
# MESSAGES PAGE
# ────────────────────────────────────────────────────────────────────────────────

def get_conversation_id(a: str, b: str) -> str:
    return "_".join(sorted([a, b]))


def page_messages():
    if not SS["user"]:
        st.warning(tr("login_required"))
        return
    uid = SS["user"]["localId"]
    st.header(f"💬 {tr('messages')}")
    users = db.collection("users").stream()
    user_map = {u.id: (u.to_dict() or {}).get("username", tr("player_name")) for u in users if u.id != uid}
    col1, col2 = st.columns([2, 5])
    with col1:
        st.subheader(tr("contacts"))
        selected_user = st.radio("", list(user_map.values())) if user_map else None
    if selected_user:
        sel_uid = next(k for k, v in user_map.items() if v == selected_user)
        conv_id = get_conversation_id(uid, sel_uid)
        SS["active_chat"] = conv_id
    if SS.get("active_chat"):
        conv_ref = db.collection("messages").document(SS["active_chat"]).collection("msgs")
        msgs = conv_ref.order_by("ts").stream()
        with col2:
            st.subheader(tr("chat_with", user=selected_user))
            for m in msgs:
                md = m.to_dict()
                align = "flex-end" if md["sender"] == uid else "flex-start"
                st.markdown(
                    f"<div style='display:flex;justify-content:{align};'><div class='card' style='max-width:60%;'>" +
                    f"<small>{md['text']}</small><br><span style='font-size:10px;'>{md['ts']}</span></div></div>",
                    unsafe_allow_html=True,
                )
            new_msg = st.text_input(tr("type_message"), key="msg_box")
            if st.button(tr("send")) and new_msg:
                conv_ref.add({
                    "sender": uid,
                    "recipient": sel_uid,
                    "text": new_msg,
                    "ts": datetime.datetime.utcnow().isoformat(),
                })
                st.rerun()


# ────────────────────────────────────────────────────────────────────────────────
# CHALLENGES PAGE
# ────────────────────────────────────────────────────────────────────────────────

def page_challenges():
    if not SS["user"]:
        st.warning(tr("login_required"))
        return
    uid = SS["user"]["localId"]
    st.header(f"⚔️ {tr('challenges')}")
    # list your teams
    my_teams = {d.id: (d.to_dict() or {}).get("name", tr("team_name")) for d in db.collection("teams").where("created_by", "==", uid).stream()}
    other_teams = {d.id: (d.to_dict() or {}).get("name", tr("team_name")) for d in db.collection("teams").where("created_by", "!=", uid).stream()}
    col1, col2 = st.columns(2)
    # Create challenge
    with col1:
        st.subheader(tr("issue_challenge"))
        if my_teams and other_teams:
            from_team_name = st.selectbox(tr("your_team"), list(my_teams.values()))
            to_team_name = st.selectbox(tr("opponent"), list(other_teams.values()))
            msg = st.text_input(tr("message_details"))
            if st.button(tr("send_challenge")):
                cid = str(uuid.uuid4())
                db.collection("challenges").document(cid).set({
                    "from_team": next(k for k, v in my_teams.items() if v == from_team_name),
                    "to_team": next(k for k, v in other_teams.items() if v == to_team_name),
                    "message": msg,
                    "status": "pending",
                    "ts": datetime.datetime.utcnow().isoformat(),
                })
                st.success(tr("challenge_sent"))
        else:
            st.info(tr("need_teams"))

    # View incoming challenges & history
    with col2:
        st.subheader(tr("incoming_challenges"))
        incoming = db.collection("challenges").where("to_team", "in", list(my_teams.keys()) or ["none"]).stream()
        active_challenges = []
        completed_challenges = []
        for c in incoming:
            cd = c.to_dict() or {}
            # Safe fetch from_team name
            from_doc = db.collection("teams").document(cd.get("from_team", "")).get()
            from_data = from_doc.to_dict() if from_doc else None
            from_name = from_data.get("name", "?") if from_data else "?"

            st.markdown(tr("challenged_you", name=from_name, msg=cd.get('message', '')))
            if cd.get("status") == "pending":
                acc, rej = st.columns(2)
                with acc:
                    if st.button(tr("accept"), key=f"a{c.id}"):
                        db.collection("challenges").document(c.id).update({"status": "accepted"})
                        st.rerun()
                with rej:
                    if st.button(tr("reject"), key=f"r{c.id}"):
                        db.collection("challenges").document(c.id).update({"status": "rejected"})
                        st.rerun()
                active_challenges.append((c.id, cd, from_name))
            else:
                completed_challenges.append((c.id, cd, from_name))
                st.markdown(f"{tr('status')}: {cd.get('status', '?')}")

        if completed_challenges:
            st.markdown("---")
            st.subheader(tr("challenge_history"))
            for cid, cd, fname in completed_challenges:
                status = cd.get("status", "?")
                ts = cd.get("ts", "?")
                st.markdown(tr("from_on_status", name=fname, date=ts, status=status))


# ────────────────────────────────────────────────────────────────────────────────
# Admin page skeleton and team management
# ────────────────────────────────────────────────────────────────────────────────

def page_admin():
    if not is_admin():
        st.error("Not authorized.")
        return
    st.header(f"🛡️ {tr('admin_dashboard')}")
    tab1, tab2, tab3 = st.tabs([tr("manage_teams"), tr("manage_matches"), tr("manage_articles")])
    # --- Teams Tab ---
    with tab1:
        st.subheader(tr("manage_teams"))
        teams = list(db.collection("teams").stream())
        for t in teams:
            data = t.to_dict() or {}
            tid = t.id
            with st.expander(data.get("name", tr("team_name"))):
                new_name = st.text_input(tr("team_name"), value=data.get("name", ""), key=f"admin_team_name_{tid}")
                if st.button(tr("save"), key=f"admin_save_team_{tid}"):
                    db.collection("teams").document(tid).update({"name": new_name})
                    st.success(tr("team_updated"))
                    st.rerun()
                if st.button(tr("delete"), key=f"admin_delete_team_{tid}"):
                    db.collection("teams").document(tid).delete()
                    st.success(tr("team_deleted"))
                    st.rerun()
    # --- Matches Tab ---
    with tab2:
        st.subheader(tr("manage_matches"))
        matches_ref = db.collection("matches")
        matches = list(matches_ref.stream())
        for m in matches:
            md = m.to_dict() or {}
            mid = m.id
            with st.expander(f"{md.get('team1', '?')} vs {md.get('team2', '?')} - {md.get('date', '?')}"):
                team1 = st.text_input(tr("team_name") + " 1", value=md.get("team1", ""), key=f"match_team1_{mid}")
                team2 = st.text_input(tr("team_name") + " 2", value=md.get("team2", ""), key=f"match_team2_{mid}")
                date = st.date_input(tr("match_date"), value=None if not md.get("date") else md.get("date"), key=f"match_date_{mid}")
                location = st.text_input(tr("location"), value=md.get("location", ""), key=f"match_location_{mid}")
                status = st.selectbox(tr("status"), ["upcoming", "live", "finished"], index=["upcoming", "live", "finished"].index(md.get("status", "upcoming")), key=f"match_status_{mid}")
                if st.button(tr("save"), key=f"save_match_{mid}"):
                    matches_ref.document(mid).update({
                        "team1": team1,
                        "team2": team2,
                        "date": str(date),
                        "location": location,
                        "status": status,
                    })
                    st.success(tr("team_updated"))
                    st.rerun()
                if st.button(tr("delete"), key=f"delete_match_{mid}"):
                    matches_ref.document(mid).delete()
                    st.success(tr("team_deleted"))
                    st.rerun()
        st.markdown("---")
        st.subheader(tr("add") + " " + tr("current_matches"))
        with st.form("add_match_form"):
            team1 = st.text_input(tr("team_name") + " 1", key="add_match_team1")
            team2 = st.text_input(tr("team_name") + " 2", key="add_match_team2")
            date = st.date_input(tr("match_date"), key="add_match_date")
            location = st.text_input(tr("location"), key="add_match_location")
            status = st.selectbox(tr("status"), ["upcoming", "live", "finished"], key="add_match_status")
            submitted = st.form_submit_button(tr("add"))
            if submitted:
                matches_ref.add({
                    "team1": team1,
                    "team2": team2,
                    "date": str(date),
                    "location": location,
                    "status": status,
                })
                st.success(tr("team_updated"))
                st.rerun()
    # --- Articles Tab ---
    with tab3:
        st.subheader(tr("manage_articles"))
        articles_ref = db.collection("articles")
        articles = list(articles_ref.stream())
        for a in articles:
            ad = a.to_dict() or {}
            aid = a.id
            with st.expander(ad.get("title", tr("article_title"))):
                title = st.text_input(tr("article_title"), value=ad.get("title", ""), key=f"article_title_{aid}")
                content = st.text_area(tr("article_content"), value=ad.get("content", ""), key=f"article_content_{aid}")
                img_file = st.file_uploader(tr("upload_image"), ["jpg", "jpeg", "png"], key=f"article_img_{aid}")
                img64 = base64.b64encode(img_file.read()).decode() if img_file else ad.get("image_base64")
                if st.button(tr("save"), key=f"save_article_{aid}"):
                    articles_ref.document(aid).update({
                        "title": title,
                        "content": content,
                        "image_base64": img64,
                    })
                    st.success(tr("article_updated"))
                    st.rerun()
                if st.button(tr("delete"), key=f"delete_article_{aid}"):
                    articles_ref.document(aid).delete()
                    st.success(tr("article_deleted"))
                    st.rerun()
        st.markdown("---")
        st.subheader(tr("add") + " " + tr("manage_articles"))
        with st.form("add_article_form"):
            title = st.text_input(tr("article_title"), key="add_article_title")
            content = st.text_area(tr("article_content"), key="add_article_content")
            img_file = st.file_uploader(tr("upload_image"), ["jpg", "jpeg", "png"], key="add_article_img")
            img64 = base64.b64encode(img_file.read()).decode() if img_file else None
            submitted = st.form_submit_button(tr("add"))
            if submitted:
                articles_ref.add({
                    "title": title,
                    "content": content,
                    "image_base64": img64,
                })
                st.success(tr("article_added"))
                st.rerun()


# ────────────────────────────────────────────────────────────────────────────────
# ROUTING
# ────────────────────────────────────────────────────────────────────────────────
header()
sidebar()

page = SS["page"]
if page == "login":
    page_login()
elif page == "dashboard":
    page_dashboard()
elif page == "messages":
    page_messages()
elif page == "challenges":
    page_challenges()
elif page == "admin":
    page_admin()
else:
    page_main()
