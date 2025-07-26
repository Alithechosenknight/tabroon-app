import streamlit as st
from firebase_config import db, auth
import uuid
import base64
import datetime
import hashlib

# ────────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & THEME
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🏆 Kuwait Football App", layout="wide")

st.markdown(
    f"""
    <style>
    :root {{
      --main-yellow: #F9C80E;
      --main-bg: linear-gradient(120deg, #2c3e50, #34495e, #3498db);
      --header-bg: rgba(44, 62, 80, 0.95);
      --card-bg: rgba(255,255,255,0.15);
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
      background: rgba(44, 62, 80, 0.98);
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
    
    .post-card {{
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 6px solid var(--main-yellow);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .post-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 32px #F9C80E44;
    }}
    
    .profile-header {{
        background: linear-gradient(135deg, var(--main-yellow)22, transparent);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 2px solid var(--main-yellow)33;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .stat-item {{
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid var(--main-yellow)33;
    }}
    
    .stat-value {{
        font-size: 2rem;
        font-weight: bold;
        color: var(--main-yellow);
    }}
    
    .stat-label {{
        font-size: 0.9rem;
        color: #ccc;
        margin-top: 0.5rem;
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
SS.setdefault("viewing_profile", None)  # profile being viewed
SS.setdefault("feed_filter", "all")     # feed filter
SS.setdefault("user_data_cache", {})    # cache user data to prevent repeated DB calls
lang = st.sidebar.selectbox("🌐 اللغة / Language", ["English", "العربية"], key="lang_toggle")
SS["lang"] = "ar" if lang == "العربية" else "en"

# Translation dictionary with expanded keys and Kuwaiti Arabic
T = {
    "en": {
        "login": "Login or Register",
        "register": "Register",
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
        "main_title": "🏆 Tbaroon.com",
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
        "feed": "Feed",
        "create_post": "Create Post",
        "post_content": "What's on your mind?",
        "share_post": "Share Post",
        "post_shared": "Post shared successfully!",
        "like": "Like",
        "comment": "Comment",
        "comments": "Comments",
        "add_comment": "Add a comment...",
        "post_comment": "Post Comment",
        "view_profile": "View Profile",
        "edit_profile": "Edit Profile",
        "profile_picture": "Profile Picture",
        "bio": "Bio",
        "speed": "Speed",
        "control": "Control", 
        "dribbling": "Dribbling",
        "weak_foot": "Weak Foot",
        "strong_foot": "Strong Foot",
        "shooting": "Shooting",
        "passing": "Passing",
        "defending": "Defending",
        "physical": "Physical",
        "overall_rating": "Overall Rating",
        "stats": "Stats",
        "about": "About",
        "posts": "Posts",
        "followers": "Followers",
        "following": "Following",
        "follow": "Follow",
        "unfollow": "Unfollow",
        "search_players": "Search Players",
        "search": "Search",
        "no_posts": "No posts yet.",
        "no_comments": "No comments yet.",
        "post_deleted": "Post deleted!",
        "comment_deleted": "Comment deleted!",
        "profile_updated": "Profile updated successfully!",
        "upload_profile_pic": "Upload Profile Picture",
        "save_profile": "Save Profile",
        "cancel": "Cancel",
        "edit": "Edit",
        "delete_post": "Delete Post",
        "delete_comment": "Delete Comment",
        "confirm_delete": "Are you sure?",
        "yes": "Yes",
        "no": "No",
    },
    "ar": {
        "login": "دخول أو تسجيل",
        "register": "تسجيل جديد",
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
        "main_title": "🏆 Tbaroon.com",
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
        "feed": "المنشورات",
        "create_post": "منشور جديد",
        "post_content": "شو في بالك؟",
        "share_post": "شارك المنشور",
        "post_shared": "تم مشاركة المنشور!",
        "like": "إعجاب",
        "comment": "تعليق",
        "comments": "التعليقات",
        "add_comment": "أضف تعليق...",
        "post_comment": "أضف التعليق",
        "view_profile": "عرض الملف الشخصي",
        "edit_profile": "تعديل الملف الشخصي",
        "profile_picture": "صورة الملف الشخصي",
        "bio": "نبذة",
        "speed": "السرعة",
        "control": "التحكم",
        "dribbling": "المراوغة",
        "weak_foot": "الرجل الضعيفة",
        "strong_foot": "الرجل القوية",
        "shooting": "التسديد",
        "passing": "التمرير",
        "defending": "الدفاع",
        "physical": "البدنية",
        "overall_rating": "التقييم العام",
        "stats": "الإحصائيات",
        "about": "حول",
        "posts": "المنشورات",
        "followers": "المتابعون",
        "following": "المتابَعون",
        "follow": "متابعة",
        "unfollow": "إلغاء المتابعة",
        "search_players": "البحث عن لاعبين",
        "search": "بحث",
        "no_posts": "لا توجد منشورات بعد.",
        "no_comments": "لا توجد تعليقات بعد.",
        "post_deleted": "تم حذف المنشور!",
        "comment_deleted": "تم حذف التعليق!",
        "profile_updated": "تم تحديث الملف الشخصي!",
        "upload_profile_pic": "رفع صورة الملف الشخصي",
        "save_profile": "حفظ الملف الشخصي",
        "cancel": "إلغاء",
        "edit": "تعديل",
        "delete_post": "حذف المنشور",
        "delete_comment": "حذف التعليق",
        "confirm_delete": "هل أنت متأكد؟",
        "yes": "نعم",
        "no": "لا",
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

def get_user_data(uid: str):
    """Get user data with caching to prevent repeated DB calls"""
    if uid not in SS.get("user_data_cache", {}):
        user_doc = db.collection("users").document(uid).get()
        user_data = user_doc.to_dict() or {}
        SS["user_data_cache"][uid] = user_data
    return SS["user_data_cache"][uid]

def update_user_data_cache(uid: str):
    """Update the user data cache"""
    user_doc = db.collection("users").document(uid).get()
    user_data = user_doc.to_dict() or {}
    SS["user_data_cache"][uid] = user_data

# ────────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ────────────────────────────────────────────────────────────────────────────────

def header():
    st.markdown(
        f"""
        <div class='main-header-bar'>
            <div style='display:flex;align-items:center;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/1/1d/Football_Pallo_valmiina-cropped.jpg' width='60' style='margin-right:18px;'>
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
                    f"<img src='https://upload.wikimedia.org/wikipedia/commons/1/1d/Football_Pallo_valmiina-cropped.jpg' class='sidebar-avatar'>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"## {tr('navigation')}")
        def nav_btn(label, icon, page, on_click_args=None):
            active = SS["page"] == page
            style = 'sidebar-active' if active else ''
            st.markdown(f"<div class='{style}'>", unsafe_allow_html=True)
            if page == 'profile' and SS.get('user'):
                # Always set viewing_profile to current user when clicking profile
                st.button(f"{icon} {label}", on_click=lambda: set_profile_page_to_self(), key='sidebar_profile_btn')
            else:
                st.button(f"{icon} {label}", on_click=reroute, args=(page,))
            st.markdown("</div>", unsafe_allow_html=True)
        if SS["user"]:
            nav_btn(tr('feed'), '📰', 'feed')
            nav_btn(tr('home_btn'), '🏠', 'main')
            nav_btn(tr('profile'), '👤', 'profile')
            nav_btn(tr('dashboard_btn'), '📋', 'dashboard')
            nav_btn(tr('messages_btn'), '💬', 'messages')
            nav_btn(tr('challenges_btn'), '⚔️', 'challenges')
            if is_admin():
                nav_btn(tr('admin'), '🛡️', 'admin')
            st.button(f"🚪 {tr('logout_btn')}", on_click=logout)
        else:
            st.button(f"🔐 {tr('login_register')}", on_click=reroute, args=("login",))

def set_profile_page_to_self():
    SS["viewing_profile"] = SS["user"]["localId"]
    reroute("profile")

def logout():
    SS["user"] = None
    SS["user_data_cache"] = {}  # Clear cache on logout
    reroute("main")

def check_session():
    """Check if user session is still valid"""
    if SS.get("user") and SS["user"].get("localId"):
        # Verify user still exists in database
        try:
            user_doc = db.collection("users").document(SS["user"]["localId"]).get()
            if user_doc.exists:
                return True
        except:
            pass
    return False

# ────────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION PAGES
# ────────────────────────────────────────────────────────────────────────────────

def page_login():
    if SS.get("restored_profile"):
        st.success("Profile restored! Please log in with your password.")
        SS["restored_profile"] = False
    st.header(tr("login"))
    option = st.radio(tr("login"), [tr("login"), tr("register")])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if option == tr("register"):
        username = st.text_input(tr("player_name"))
        if st.button(tr("register")):
            try:
                # Create user with Firebase Admin SDK
                user_record = auth.create_user(
                    email=email,
                    password=password,
                    display_name=username
                )
                uid = user_record.uid
                
                # Hash password for storage
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                # Create user document in Firestore
                db.collection("users").document(uid).set({
                    "username": username,
                    "email": email,
                    "password_hash": hashed_password,
                    "profile": {},
                    "stats": {
                        "speed": 50, "control": 50, "dribbling": 50,
                        "shooting": 50, "passing": 50, "defending": 50,
                        "physical": 50, "weak_foot": 50, "strong_foot": "right",
                        "overall": 50
                    },
                    "following": [],
                    "followers": [],
                    "bio": "",
                    "profile_picture": None
                })
                st.success(tr("account_created"))
            except Exception as e:
                if "EMAIL_EXISTS" in str(e):
                    st.error("Account already exists. Please log in instead.")
                else:
                    st.error(f"Registration error: {str(e)}")
    else:  # Login
        if st.button(tr("login")):
            try:
                # Simple login: check if user exists in Firestore
                users_ref = db.collection("users")
                query = users_ref.where("email", "==", email).limit(1).stream()
                user_docs = list(query)
                
                if user_docs:
                    user_doc = user_docs[0]
                    user_data = user_doc.to_dict()
                    
                    # Verify password
                    stored_hash = user_data.get("password_hash", "")
                    input_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    if stored_hash == input_hash:
                        SS["user"] = {
                            "localId": user_doc.id,
                            "email": user_data.get("email"),
                            "displayName": user_data.get("username")
                        }
                        reroute("dashboard")
                    else:
                        st.error(tr("invalid_credentials"))
                else:
                    # Check if user exists in Auth but not Firestore
                    try:
                        user_record = auth.get_user_by_email(email)
                        # If found, offer to restore Firestore profile
                        st.warning("Account exists in authentication but not in app database. Click below to restore your profile.")
                        if st.button("Restore Profile"):
                            uid = user_record.uid
                            hashed_password = hashlib.sha256(password.encode()).hexdigest()
                            db.collection("users").document(uid).set({
                                "username": user_record.display_name or email.split('@')[0],
                                "email": email,
                                "password_hash": hashed_password,
                                "profile": {},
                                "stats": {
                                    "speed": 50, "control": 50, "dribbling": 50,
                                    "shooting": 50, "passing": 50, "defending": 50,
                                    "physical": 50, "weak_foot": 50, "strong_foot": "right",
                                    "overall": 50
                                },
                                "following": [],
                                "followers": [],
                                "bio": "",
                                "profile_picture": None
                            })
                            SS["restored_profile"] = True
                            st.experimental_rerun()
                    except Exception:
                        st.error("User not found. Please register first.")
            except Exception as e:
                st.error(f"Login error: {str(e)}")


# ────────────────────────────────────────────────────────────────────────────────
# FEED PAGE (LinkedIn-like posts)
# ────────────────────────────────────────────────────────────────────────────────

def page_feed():
    if not SS["user"]:
        st.warning(tr("please_login"))
        if st.button(tr("go_to_login")):
            reroute("login")
        return
    
    uid = SS["user"]["localId"]
    st.header(f"📰 {tr('feed')}")
    
    # Create post section
    with st.expander(f"✏️ {tr('create_post')}", expanded=False):
        post_content = st.text_area(tr("post_content"), height=100)
        post_image = st.file_uploader(tr("upload_image"), ["jpg", "jpeg", "png"], key="post_image")
        img64 = base64.b64encode(post_image.read()).decode() if post_image else None
        
        if st.button(tr("share_post")):
            if post_content.strip():
                post_id = str(uuid.uuid4())
                db.collection("posts").document(post_id).set({
                    "author_id": uid,
                    "content": post_content,
                    "image_base64": img64,
                    "likes": [],
                    "comments": [],
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                })
                st.success(tr("post_shared"))
                st.rerun()
            else:
                st.error("Please write something to post!")
    
    # Feed filter
    filter_option = st.selectbox("Filter", ["All Posts", "My Posts", "Following"], key="feed_filter")
    
    # Get posts
    posts_ref = db.collection("posts")
    if filter_option == "My Posts":
        posts = posts_ref.where("author_id", "==", uid).order_by("timestamp", direction="DESCENDING").stream()
    elif filter_option == "Following":
        # Get following list
        user_doc = db.collection("users").document(uid).get()
        user_data = user_doc.to_dict() or {}
        following = user_data.get("following", [])
        if following:
            posts = posts_ref.where("author_id", "in", following).order_by("timestamp", direction="DESCENDING").stream()
        else:
            posts = []
            st.info("You're not following anyone yet!")
    else:
        posts = posts_ref.order_by("timestamp", direction="DESCENDING").stream()
    
    # Display posts
    for post in posts:
        post_data = post.to_dict() or {}
        author_id = post_data.get("author_id")
        
        # Get author info
        author_doc = db.collection("users").document(author_id).get()
        author_data = author_doc.to_dict() or {}
        author_name = author_data.get("username", "Unknown Player")
        author_pic = author_data.get("profile_picture")
        
        # Post card
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex;align-items:center;margin-bottom:1rem;'>
                    <img src='{"data:image/png;base64," + author_pic if author_pic else "https://via.placeholder.com/50x50/666/fff?text=⚽"}' 
                         style='width:50px;height:50px;border-radius:50%;margin-right:1rem;object-fit:cover;'>
                    <div>
                        <strong style='color:var(--main-yellow);'>{author_name}</strong><br>
                        <small style='color:#ccc;'>{post_data.get('timestamp', '')[:19]}</small>
                    </div>
                </div>
                <div style='margin-bottom:1rem;'>{post_data.get('content', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Post image
            if post_data.get("image_base64"):
                st.image(base64.b64decode(post_data["image_base64"]), width=400)
            
            # Like and comment buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                liked = uid in post_data.get("likes", [])
                like_text = "❤️" if liked else "🤍"
                if st.button(f"{like_text} {len(post_data.get('likes', []))}", key=f"like_{post.id}"):
                    likes = post_data.get("likes", [])
                    if uid in likes:
                        likes.remove(uid)
                    else:
                        likes.append(uid)
                    db.collection("posts").document(post.id).update({"likes": likes})
                    st.rerun()
            
            with col2:
                if st.button(f"💬 {len(post_data.get('comments', []))}", key=f"comment_btn_{post.id}"):
                    SS[f"show_comments_{post.id}"] = not SS.get(f"show_comments_{post.id}", False)
                    st.rerun()
            
            with col3:
                if author_id == uid:
                    if st.button("🗑️", key=f"delete_post_{post.id}"):
                        if st.checkbox(tr("confirm_delete"), key=f"confirm_delete_{post.id}"):
                            db.collection("posts").document(post.id).delete()
                            st.success(tr("post_deleted"))
                            st.rerun()
            
            # Comments section
            if SS.get(f"show_comments_{post.id}", False):
                st.markdown("---")
                st.subheader(tr("comments"))
                
                # Add comment
                new_comment = st.text_input(tr("add_comment"), key=f"comment_input_{post.id}")
                if st.button(tr("post_comment"), key=f"post_comment_{post.id}"):
                    if new_comment.strip():
                        comment_id = str(uuid.uuid4())
                        comments = post_data.get("comments", [])
                        comments.append({
                            "id": comment_id,
                            "author_id": uid,
                            "content": new_comment,
                            "timestamp": datetime.datetime.utcnow().isoformat()
                        })
                        db.collection("posts").document(post.id).update({"comments": comments})
                        st.rerun()
                
                # Display comments
                for comment in post_data.get("comments", []):
                    comment_author_doc = db.collection("users").document(comment["author_id"]).get()
                    comment_author_data = comment_author_doc.to_dict() or {}
                    comment_author_name = comment_author_data.get("username", "Unknown")
                    
                    st.markdown(f"""
                    <div style='margin:0.5rem 0;padding:0.5rem;background:rgba(255,255,255,0.05);border-radius:8px;'>
                        <strong style='color:var(--main-yellow);'>{comment_author_name}</strong>: {comment['content']}
                        <br><small style='color:#ccc;'>{comment['timestamp'][:19]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Delete comment button (for comment author)
                    if comment["author_id"] == uid:
                        if st.button("🗑️", key=f"delete_comment_{comment['id']}"):
                            comments = post_data.get("comments", [])
                            comments = [c for c in comments if c["id"] != comment["id"]]
                            db.collection("posts").document(post.id).update({"comments": comments})
                            st.success(tr("comment_deleted"))
                            st.rerun()
            
            st.markdown("<div style='margin:2rem 0;'></div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PROFILE PAGE
# ────────────────────────────────────────────────────────────────────────────────

def page_profile():
    if not SS["user"]:
        st.warning(tr("please_login"))
        if st.button(tr("go_to_login")):
            reroute("login")
        return
    uid = SS["user"]["localId"]
    # Only set viewing_profile to self if not set
    if SS.get("viewing_profile") is None:
        SS["viewing_profile"] = uid
    viewing_uid = SS.get("viewing_profile", uid)  # View own profile by default
    
    # Get user data
    user_data = get_user_data(viewing_uid)
    
    # Profile header
    profile_pic = user_data.get("profile_picture")
    username = user_data.get("username", "Unknown Player")
    bio = user_data.get("bio", "")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if profile_pic:
            st.image(base64.b64decode(profile_pic), width=200)
        else:
            st.markdown("""
            <div style='width:200px;height:200px;border:3px dashed var(--main-yellow);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:4rem;'>
                ⚽
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.title(username)
        if bio:
            st.write(bio)
        
        # Follow/Unfollow button (if viewing someone else's profile)
        if viewing_uid != uid:
            current_user_doc = db.collection("users").document(uid).get()
            current_user_data = current_user_doc.to_dict() or {}
            following = current_user_data.get("following", [])
            
            if viewing_uid in following:
                if st.button(tr("unfollow")):
                    following.remove(viewing_uid)
                    db.collection("users").document(uid).update({"following": following})
                    st.rerun()
            else:
                if st.button(tr("follow")):
                    following.append(viewing_uid)
                    db.collection("users").document(uid).update({"following": following})
                    st.rerun()
        
        # Stats summary
        stats = user_data.get("stats", {})
        if stats:
            st.subheader(tr("stats"))
            cols = st.columns(4)
            with cols[0]:
                st.metric(tr("speed"), stats.get("speed", 0))
            with cols[1]:
                st.metric(tr("control"), stats.get("control", 0))
            with cols[2]:
                st.metric(tr("dribbling"), stats.get("dribbling", 0))
            with cols[3]:
                st.metric(tr("shooting"), stats.get("shooting", 0))
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([tr("about"), tr("stats"), tr("posts")])
    
    with tab1:
        st.subheader(tr("about"))
        if viewing_uid == uid:  # Edit mode for own profile
            new_bio = st.text_area(tr("bio"), value=bio, height=100)
            if st.button(tr("save_profile"), key="save_profile_bio"):
                db.collection("users").document(uid).update({"bio": new_bio})
                update_user_data_cache(uid)  # Update cache
                st.success(tr("profile_updated"))
                st.rerun()
        else:
            st.write(bio if bio else "No bio available.")
    
    with tab2:
        st.subheader(tr("stats"))
        if viewing_uid == uid:  # Edit mode for own profile
            stats = user_data.get("stats", {})
            col1, col2 = st.columns(2)
            
            with col1:
                speed = st.slider(tr("speed"), 0, 100, stats.get("speed", 50))
                control = st.slider(tr("control"), 0, 100, stats.get("control", 50))
                dribbling = st.slider(tr("dribbling"), 0, 100, stats.get("dribbling", 50))
                shooting = st.slider(tr("shooting"), 0, 100, stats.get("shooting", 50))
            
            with col2:
                passing = st.slider(tr("passing"), 0, 100, stats.get("passing", 50))
                defending = st.slider(tr("defending"), 0, 100, stats.get("defending", 50))
                physical = st.slider(tr("physical"), 0, 100, stats.get("physical", 50))
                weak_foot = st.slider(tr("weak_foot"), 0, 100, stats.get("weak_foot", 50))
            
            strong_foot = st.selectbox(tr("strong_foot"), [tr("right"), tr("left")], 
                                     index=0 if stats.get("strong_foot", "right") == "right" else 1)
            
            if st.button(tr("save_profile"), key="save_profile_stats"):
                new_stats = {
                    "speed": speed, "control": control, "dribbling": dribbling,
                    "shooting": shooting, "passing": passing, "defending": defending,
                    "physical": physical, "weak_foot": weak_foot, "strong_foot": strong_foot
                }
                # Calculate overall rating (only numeric stats)
                numeric_stats = [v for k, v in new_stats.items() if isinstance(v, (int, float))]
                overall = sum(numeric_stats) // len(numeric_stats)
                new_stats["overall"] = overall
                
                db.collection("users").document(uid).update({"stats": new_stats})
                update_user_data_cache(uid)  # Update cache
                st.success(tr("profile_updated"))
                st.rerun()
        else:
            # Display stats
            stats = user_data.get("stats", {})
            if stats:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(tr("speed"), stats.get("speed", 0))
                    st.metric(tr("control"), stats.get("control", 0))
                    st.metric(tr("dribbling"), stats.get("dribbling", 0))
                    st.metric(tr("shooting"), stats.get("shooting", 0))
                with col2:
                    st.metric(tr("passing"), stats.get("passing", 0))
                    st.metric(tr("defending"), stats.get("defending", 0))
                    st.metric(tr("physical"), stats.get("physical", 0))
                    st.metric(tr("weak_foot"), stats.get("weak_foot", 0))
                
                st.metric(tr("overall_rating"), stats.get("overall", 0))
                st.write(f"{tr('strong_foot')}: {stats.get('strong_foot', 'Right')}")
            else:
                st.info("No stats available.")
    
    with tab3:
        st.subheader(tr("posts"))
        # Get user's posts
        posts = db.collection("posts").where("author_id", "==", viewing_uid).order_by("timestamp", direction="DESCENDING").stream()
        posts_list = list(posts)
        
        if posts_list:
            for post in posts_list:
                post_data = post.to_dict() or {}
                st.markdown(f"""
                <div class='card'>
                    <div style='margin-bottom:1rem;'>{post_data.get('content', '')}</div>
                    <small style='color:#ccc;'>{post_data.get('timestamp', '')[:19]}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if post_data.get("image_base64"):
                    st.image(base64.b64decode(post_data["image_base64"]), width=300)
                
                st.markdown(f"❤️ {len(post_data.get('likes', []))} 💬 {len(post_data.get('comments', []))}")
                st.markdown("---")
        else:
            st.info(tr("no_posts"))

# ────────────────────────────────────────────────────────────────────────────────
# MAIN LANDING PAGE
# ────────────────────────────────────────────────────────────────────────────────

def page_main():
    if SS["user"]:
        # Search players and teams
        st.header(f"🔍 {tr('search_players')}")
        search_query = st.text_input(tr("search"), placeholder="Search by player or team name...")
        
        if search_query:
            # Search in users collection
            users = db.collection("users").stream()
            matching_users = []
            for user in users:
                user_data = user.to_dict() or {}
                username = user_data.get("username", "").lower()
                if search_query.lower() in username:
                    matching_users.append((user.id, user_data))
            # Search in teams collection
            teams = db.collection("teams").stream()
            matching_teams = []
            for team in teams:
                team_data = team.to_dict() or {}
                team_name = team_data.get("name", "").lower()
                if search_query.lower() in team_name:
                    matching_teams.append((team.id, team_data))
            if matching_users:
                st.subheader(f"Found {len(matching_users)} players:")
                for user_id, user_data in matching_users:
                    username = user_data.get("username", "Unknown")
                    profile_pic = user_data.get("profile_picture")
                    bio = user_data.get("bio", "")
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        if profile_pic:
                            st.image(base64.b64decode(profile_pic), width=80)
                        else:
                            st.markdown("""
                            <div style='width:80px;height:80px;border:2px dashed var(--main-yellow);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2rem;'>
                                ⚽
                            </div>
                            """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**{username}**")
                        if bio:
                            st.markdown(f"*{bio[:100]}{'...' if len(bio) > 100 else ''}*")
                    with col3:
                        if st.button(tr("view_profile"), key=f"view_{user_id}"):
                            SS["viewing_profile"] = user_id
                            reroute("profile")
                    st.markdown("---")
            if matching_teams:
                st.subheader(f"Found {len(matching_teams)} teams:")
                for team_id, team_data in matching_teams:
                    team_name = team_data.get("name", "Unknown Team")
                    logo = team_data.get("logo_base64")
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if logo:
                            st.image(base64.b64decode(logo), width=80)
                        else:
                            st.markdown("""
                            <div style='width:80px;height:80px;border:2px dashed var(--main-yellow);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2rem;'>
                                🏟️
                            </div>
                            """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**{team_name}**")
                        st.markdown(f"<span style='color:#aaa;'>Team ID: {team_id}</span>", unsafe_allow_html=True)
                    st.markdown("---")
            if not matching_users and not matching_teams:
                st.info("No players or teams found matching your search.")
    
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
    udata = get_user_data(uid)
    st.header(tr("welcome", username=udata.get('username',tr('player_name'))))
    tab1, tab2, tab3 = st.tabs([f"👤 {tr('profile')}", f"⚽ {tr('my_teams')}", f"🖼️ {tr('edit_teams_tab')}"])

    # ── Profile ──────────────────
    with tab1:
        profile = udata.get("profile", {})
        
        # Profile picture upload
        st.subheader(tr("profile_picture"))
        profile_pic = st.file_uploader(tr("upload_profile_pic"), ["jpg", "jpeg", "png"], key="profile_pic")
        if profile_pic:
            pic64 = base64.b64encode(profile_pic.read()).decode()
            st.image(base64.b64decode(pic64), width=200)
            if st.button(tr("save_profile"), key="save_profile_pic"):
                db.collection("users").document(uid).update({"profile_picture": pic64})
                update_user_data_cache(uid)  # Update cache
                st.success(tr("profile_updated"))
                # Don't rerun here to keep the form state
        
        # Basic info
        st.subheader("Basic Information")
        h = st.number_input(tr("height"), 100, 250, value=int(profile.get("height", 170)))
        w = st.number_input(tr("weight"), 30, 200, value=int(profile.get("weight", 70)))
        bio = st.text_area(tr("bio"), value=udata.get("bio", ""), height=100)
        
        if st.button(tr("save_profile"), key="save_profile_basic"):
            db.collection("users").document(uid).update({
                "profile": {"height": h, "weight": w},
                "bio": bio
            })
            update_user_data_cache(uid)  # Update cache
            st.success(tr("profile_updated"))
            # Don't rerun here to keep the form state
        
        # Quick profile view
        st.markdown("---")
        st.subheader("Quick Profile Preview")
        if st.button(tr("view_profile"), key="view_profile_dashboard"):
            SS["viewing_profile"] = uid
            reroute("profile")

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

# Check session validity
if SS.get("user") and not check_session():
    SS["user"] = None
    SS["user_data_cache"] = {}

page = SS["page"]
if page == "login":
    page_login()
elif page == "feed":
    page_feed()
elif page == "profile":
    page_profile()
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
