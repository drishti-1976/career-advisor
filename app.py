import streamlit as st
import pandas as pd
import numpy as np
import re, io, os
from collections import Counter

st.set_page_config(
    page_title="Smart Career Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Slate & Cyan theme ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html,[class*="css"]          { font-family:'Plus Jakarta Sans',sans-serif; }
.stApp                       { background:#f1f5f9; }
#MainMenu,footer,header      { visibility:hidden; }

/* ── hero ── */
.hero                { text-align:center; padding:44px 20px 28px; }
.hero h1             { font-size:clamp(24px,4.5vw,42px); font-weight:800; color:#0f172a;
                       margin:0 0 10px; letter-spacing:-1.2px; }
.hero h1 span        { color:#0891b2; }
.hero p              { color:#64748b; font-size:15px; margin:0; }
.badge               { display:inline-block; background:#e0f2fe; border:1px solid #bae6fd;
                       color:#0369a1; border-radius:20px; padding:4px 16px; font-size:11px;
                       font-weight:700; letter-spacing:1.5px; margin-bottom:14px; }

/* ── cards ── */
.card                { background:#ffffff; border:1px solid #e2e8f0;
                       border-radius:16px; padding:22px 26px; margin-bottom:16px;
                       box-shadow:0 1px 6px rgba(15,23,42,.06); }
.card h3             { font-size:14px; font-weight:700; color:#0f172a; margin:0 0 16px; }

/* ── result cards ── */
.res-card            { background:#f8fafc; border-radius:0; padding:16px 20px;
                       margin-bottom:10px; border-left:3px solid;
                       border-right:none; border-top:none; border-bottom:none; }
.res-title           { font-size:15px; font-weight:700; color:#0f172a; margin-bottom:4px; }
.res-desc            { font-size:13px; color:#64748b; line-height:1.6; }

/* ── pills ── */
.pill                { display:inline-block; background:#e0f2fe; color:#0369a1;
                       border:1px solid #bae6fd; border-radius:20px; padding:3px 12px;
                       font-size:12px; font-weight:600; margin:3px; }
.pill-miss           { background:#fff1f2; color:#be123c; border-color:#fecdd3; }

/* ── ATS score ── */
.ats-num             { font-family:'DM Mono',monospace; font-size:68px;
                       font-weight:800; letter-spacing:-2px; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"]  { background:#e2e8f0; border-radius:14px;
                                      padding:5px; gap:4px; border:none; }
.stTabs [data-baseweb="tab"]       { border-radius:10px; color:#64748b; font-weight:600;
                                      font-size:14px; padding:9px 22px; border:none!important; }
.stTabs [aria-selected="true"]     { background:#0891b2!important; color:#ffffff!important; }

/* ── inputs ── */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea             { background:#f8fafc!important; border:1.5px solid #cbd5e1!important;
                                   color:#0f172a!important; border-radius:10px!important;
                                   caret-color:#0891b2!important; }
.stTextInput input::placeholder  { color:#94a3b8!important; }
.stTextInput input:focus,
.stTextArea textarea:focus       { border-color:#0891b2!important;
                                   box-shadow:0 0 0 3px rgba(8,145,178,.12)!important;
                                   caret-color:#0891b2!important; }

/* ── selectbox ── */
.stSelectbox div[data-baseweb="select"]     { background:#f8fafc!important; border:1.5px solid #cbd5e1!important;
                                              color:#0f172a!important; border-radius:10px!important; }
.stSelectbox div[data-baseweb="select"]>div { background:#f8fafc!important; color:#0f172a!important; }
div[data-baseweb="popover"]                 { background:#ffffff!important; border:1px solid #e2e8f0!important; }
div[data-baseweb="option"]                  { background:#ffffff!important; color:#0f172a!important; }
div[data-baseweb="option"]:hover            { background:#f0f9ff!important; }

/* ── multiselect ── */
.stMultiSelect>div               { background:#f8fafc!important; border:1.5px solid #cbd5e1!important;
                                   border-radius:10px!important; }
span[data-baseweb="tag"]         { background:#e0f2fe!important; color:#0369a1!important;
                                   border:1px solid #bae6fd!important; }

/* ── file uploader ── */
.stFileUploader>div              { background:#f8fafc!important;
                                   border:1.5px dashed #cbd5e1!important;
                                   border-radius:10px!important;
                                   padding:10px 14px!important;
                                   min-height:unset!important; }
.stFileUploader>div>div          { gap:6px!important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
                                   font-size:12px!important;
                                   padding:4px 0!important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] > div {
                                   font-size:12px!important; }
.stFileUploader svg              { width:24px!important; height:24px!important; }

/* ── uploaded filename ── */
.stFileUploader [data-testid="stFileUploaderFile"],
.stFileUploader [data-testid="stFileUploaderFile"] span,
.stFileUploader [data-testid="stFileUploaderFile"] p,
.stFileUploader [data-testid="stFileUploaderFileName"],
.stFileUploader span[title],
.stFileUploader .uploadedFileName  { color:#0f172a!important; }

/* ── button ── */
.stButton>button                 { background:linear-gradient(135deg,#0e7490,#0891b2 55%,#06b6d4)!important;
                                   color:#ffffff!important; border:none!important; border-radius:11px!important;
                                   font-weight:700!important; font-size:14px!important;
                                   padding:12px 28px!important; width:100%;
                                   box-shadow:0 4px 14px rgba(8,145,178,.25)!important;
                                   transition:all .2s!important; }
.stButton>button:hover           { box-shadow:0 6px 22px rgba(8,145,178,.4)!important; }

/* ── progress ── */
.stProgress>div>div              { background:linear-gradient(90deg,#0e7490,#06b6d4)!important;
                                   border-radius:4px; }

/* ── metrics ── */
[data-testid="metric-container"] { background:#ffffff!important; border:1px solid #e2e8f0!important;
                                   border-radius:14px; padding:16px!important;
                                   box-shadow:0 1px 4px rgba(15,23,42,.05)!important; }
[data-testid="metric-container"] label
                                 { color:#64748b!important; font-size:11px!important;
                                   letter-spacing:1.2px!important; text-transform:uppercase;
                                   font-weight:600!important; }
[data-testid="metric-container"] [data-testid="stMetricValue"]
                                 { color:#0891b2!important; font-size:22px!important;
                                   font-weight:800!important; font-family:"DM Mono",monospace!important; }

/* ── misc ── */
hr                               { border-color:#e2e8f0!important; }
label                            { color:#475569!important; font-size:13px!important; font-weight:500!important; }
h2,h3                            { color:#0f172a!important; }
p,li                             { color:#475569; }
code                             { background:#e0f2fe!important; color:#0369a1!important;
                                   border-radius:5px!important; padding:1px 6px!important; }

/* ── FIX: pre block text always dark ── */
pre,
pre *,
pre code,
.stMarkdown pre,
.stMarkdown pre *,
div[data-testid="stMarkdownContainer"] pre,
div[data-testid="stMarkdownContainer"] pre * {
                                   background:#f1f5f9!important;
                                   border:1px solid #e2e8f0!important;
                                   border-radius:12px!important;
                                   color:#0f172a!important;
                                   font-family:'DM Mono',monospace!important;
                                   font-size:13px!important;
                                   padding:14px 18px!important;
                                   display:block!important; }

.stDataFrame                     { border:1px solid #e2e8f0!important; border-radius:10px!important; }

/* ── install-block helper class ── */
.install-block {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 6px 0;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #0f172a !important;
    display: block;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
ROLE_COLORS = ["#0891b2","#6366f1","#059669","#db2777","#d97706","#7c3aed"]
ALGO_COLORS = {
    "Random Forest": "#0891b2",
    "XGBoost":       "#059669",
    "Decision Tree": "#d97706",
    "SVM":           "#6366f1",
}

JOB_CLUSTERS = {
    "Software Engineer / Developer": [
        "software engineer","software developer","computer software engineer",
        "back end developer","front end developer","full stack developer",
        "application developer","asp.net developer","java developer","developer",
        "associate software engineer","specialist programmer","programmer analyst","programmer"
    ],
    "Data Analyst / Business Analyst": [
        "data analyst","business analyst","analyst","application development analyst",
        "associate consultant","data analytics","reporting analyst"
    ],
    "Data Scientist / ML Engineer": [
        "data scientist","machine learning engineer","ai engineer","data engineer",
        "research scientist","scientist"
    ],
    "Mechanical Engineer": [
        "mechanical engineer","mechanical design engineer","design engineer",
        "production engineer","maintenance engineer-mechanical","ces-cae- fea analyst"
    ],
    "Civil / Structural Engineer": [
        "civil & structural engineer","civil engineer","site engineer","structural engineer"
    ],
    "Project Manager": ["project manager","program manager","scrum master"],
    "Cyber Security Analyst": [
        "cyber security analyst","information security analyst","security engineer","ethical hacker"
    ],
    "DevOps / Cloud Engineer": [
        "devops engineer","aws architect","aws developer","cloud engineer","infrastructure engineer"
    ],
    "Web Developer": [
        "web developer","ui developer","frontend developer","react developer","ux developer"
    ],
    "Teacher / Professor": [
        "teacher","teaching","assistant professor","professor","lecturer","faculty"
    ],
    "Research Associate": [
        "research associate","research analyst","researcher","lab technician",
        "research and development","scientist"
    ],
    "Marketing Manager": [
        "marketing manager","digital marketing","social media manager","brand manager",
        "marketing executive","content marketing"
    ],
    "Sales Executive": [
        "sales executive","sales","sales manager","business development","tele-caller",
        "active trading service","relationships manager"
    ],
    "Financial Analyst": [
        "financial analyst","finance analyst","accountant","account assistant",
        "associate operations processor","financial advisor","investment analyst","trading"
    ],
    "HR Executive": [
        "hr","hr executive","human resources","talent acquisition","recruiter","people manager"
    ],
    "Graphic / UI-UX Designer": [
        "graphic designer","ui/ux designer","designer","visual designer","creative designer","design"
    ],
    "Database Administrator": [
        "database administrator","sql developer","dba","data administrator"
    ],
    "Embedded / Hardware Engineer": [
        "hardware design engineer","embedded engineer","instrumentation and control engineer",
        "engineer-power electronics","electronics engineer"
    ],
    "Quality / Testing Engineer": [
        "quality engineer","qa engineer","test engineer","software tester","quality assurance"
    ],
    "Journalist / Content Writer": [
        "journalist","sub-editor","content writer","technical writer","news coverage","editor"
    ],
    "Company Secretary / Legal": [
        "company secretary","advocate","legal advisor","lawyer","compliance officer"
    ],
    "Medical / Healthcare": [
        "medical practitioner","doctor","nurse","pharmacist","lab technician","healthcare"
    ],
}

SKILL_KEYWORDS = {
    "Python": ["python","pandas","numpy","django","flask","fastapi","scikit","tensorflow","pytorch"],
    "Java": ["java","spring","hibernate","maven","j2ee"],
    "SQL / Database": ["sql","mysql","postgresql","oracle","nosql","mongodb","database"],
    "JavaScript / Web": ["javascript","react","angular","vue","node","html","css","typescript"],
    "C / C++": ["c++","c programming","embedded c","oop"],
    "Data Science / ML": ["machine learning","deep learning","nlp","ai","data science","tensorflow","keras","sklearn","xgboost","neural network"],
    "Data Analysis": ["data analysis","tableau","power bi","excel","pivot","matplotlib","seaborn","visualization"],
    "Cloud / DevOps": ["aws","azure","gcp","docker","kubernetes","jenkins","ci/cd","terraform","linux","git","devops"],
    "Cyber Security": ["cyber security","ethical hacking","penetration testing","firewall","kali linux","network security"],
    "Project Management": ["project management","agile","scrum","jira","pmp","kanban"],
    "Communication": ["communication","presentation","leadership","teamwork","interpersonal","negotiation"],
    "Finance / Accounting": ["finance","accounting","tally","gst","audit","budgeting","financial analysis","investment"],
    "Marketing / Sales": ["marketing","seo","sem","google ads","social media","crm","salesforce","digital marketing"],
    "Design": ["figma","adobe","photoshop","illustrator","canva","ui/ux","graphic design","autocad","solidworks"],
    "Research": ["research","literature review","academic writing","data collection","survey","qualitative","quantitative"],
}

ATS_JD_KEYWORDS = {
    "Software Engineer / Developer":      ["python","java","c++","javascript","sql","git","api","oop","agile","docker","debugging","algorithms"],
    "Data Analyst / Business Analyst":    ["sql","excel","power bi","tableau","data analysis","python","reporting","dashboard","kpi","visualization"],
    "Data Scientist / ML Engineer":       ["python","machine learning","deep learning","tensorflow","sklearn","nlp","statistics","model","prediction"],
    "Mechanical Engineer":                ["autocad","solidworks","catia","design","manufacturing","cad","thermodynamics","production","quality"],
    "Civil / Structural Engineer":        ["autocad","staad","revit","structural","civil","construction","site","concrete","design","estimation"],
    "Project Manager":                    ["project management","agile","scrum","pmp","stakeholder","budget","timeline","risk","jira","planning"],
    "Cyber Security Analyst":             ["cyber security","ethical hacking","penetration","network","firewall","kali","vulnerability","siem","encryption"],
    "DevOps / Cloud Engineer":            ["aws","azure","docker","kubernetes","jenkins","ci/cd","linux","terraform","ansible","git","pipeline"],
    "Web Developer":                      ["html","css","javascript","react","node","mysql","api","responsive","git","frontend","backend"],
    "Teacher / Professor":                ["teaching","curriculum","lesson plan","assessment","classroom","communication","education","research","mentor"],
    "Research Associate":                 ["research","analysis","literature","data collection","publication","methodology","lab","statistics"],
    "Marketing Manager":                  ["digital marketing","seo","sem","google ads","social media","content","campaign","analytics","brand","crm"],
    "Sales Executive":                    ["sales","crm","target","client","negotiation","lead generation","revenue","business development","presentation"],
    "Financial Analyst":                  ["excel","financial modeling","valuation","accounting","tally","gst","audit","balance sheet","investment"],
    "HR Executive":                       ["recruitment","hr","payroll","policy","onboarding","performance management","hrms","communication","training"],
    "Graphic / UI-UX Designer":           ["figma","adobe xd","photoshop","illustrator","ui","ux","design","wireframe","prototype","branding"],
    "Database Administrator":             ["sql","database","oracle","query optimization","dba","backup","performance","mysql","postgresql"],
    "Embedded / Hardware Engineer":       ["embedded","microcontroller","vhdl","pcb","electronics","firmware","arm","fpga","circuit design"],
    "Quality / Testing Engineer":         ["testing","quality","selenium","jira","bug","test case","automation","regression","qa","manual testing"],
    "Journalist / Content Writer":        ["writing","editing","content","seo","research","communication","wordpress","journalism","proofreading"],
    "Company Secretary / Legal":          ["company law","secretarial","legal","compliance","mca","roc","sebi","contract","corporate governance"],
    "Medical / Healthcare":               ["patient care","clinical","diagnosis","medical","pharmacology","anatomy","lab","treatment","biology","chemistry"],
}

CAREER_TIPS = {
    "Software Engineer / Developer":   "Build a strong GitHub portfolio. Contribute to open-source. Learn system design for senior roles.",
    "Data Analyst / Business Analyst": "Master SQL and Power BI/Tableau. Practice on Kaggle. Learn to communicate insights to non-technical stakeholders.",
    "Data Scientist / ML Engineer":    "Build end-to-end ML projects. Learn MLOps and model deployment. Publish on Medium or Kaggle.",
    "Mechanical Engineer":             "Get hands-on with CAD tools. Pursue GATE for PSUs. Six Sigma certification adds value.",
    "Civil / Structural Engineer":     "Learn STAAD Pro and AutoCAD. Pursue PMP for site management. Look for government infrastructure projects.",
    "Project Manager":                 "Get PMP or Agile/Scrum certified. Build stakeholder management skills. Track your project delivery metrics.",
    "Cyber Security Analyst":          "Pursue CEH, OSCP, or CompTIA Security+. Practice on TryHackMe and HackTheBox. Stay updated with CVE databases.",
    "DevOps / Cloud Engineer":         "Get AWS/Azure certified. Build CI/CD pipelines on personal projects. Kubernetes (CKA) certification is highly valued.",
    "Web Developer":                   "Build 5+ real-world projects. Learn React and Node.js. Understand REST APIs and basic cloud deployment.",
    "Teacher / Professor":             "Pursue B.Ed or M.Ed if needed. Publish research papers. Build engaging content with modern teaching tools.",
    "Research Associate":              "Publish in indexed journals. Master statistical tools (SPSS/R). Pursue a PhD for senior research positions.",
    "Marketing Manager":               "Get Google/Meta certifications. Build a personal brand. Learn analytics tools to prove ROI.",
    "Sales Executive":                 "Improve CRM skills (Salesforce). Learn consultative selling. Track your conversion metrics.",
    "Financial Analyst":               "Pursue CFA or CPA. Master Excel financial modeling. Learn Python/SQL for automation.",
    "HR Executive":                    "Get SHRM certified. Learn HRIS tools. Understand employment law and stay updated on HR trends.",
    "Graphic / UI-UX Designer":        "Build a Behance/Dribbble portfolio. Learn Figma deeply. Study user psychology and accessibility.",
    "Database Administrator":          "Get Oracle or SQL Server certified. Learn query optimization. Explore cloud databases (AWS RDS, Firebase).",
    "Embedded / Hardware Engineer":    "Learn Embedded C and RTOS. Get hands-on with Arduino/Raspberry Pi. Pursue VLSI or FPGA specialization.",
    "Quality / Testing Engineer":      "Learn Selenium and test automation. Get ISTQB certified. Explore API testing with Postman.",
    "Journalist / Content Writer":     "Build a writing portfolio. Learn SEO basics. Specialize in a niche for better opportunities.",
    "Company Secretary / Legal":       "Clear CS exams from ICSI. Learn corporate law and SEBI regulations. Internships at CA/CS firms are valuable.",
    "Medical / Healthcare":            "Stay current with medical literature. Build clinical experience. Consider specialization for better prospects.",
}


# ══════════════════════════════════════════════════════════════════════════════
# ML MODEL
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_and_train():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.feature_extraction.text import TfidfVectorizer
    import scipy.sparse as sp

    df = pd.read_csv("career_recommender.csv", encoding="utf-8-sig")
    df.columns = ["name","gender","course","specialization","interests",
                  "skills","cgpa","cert_yn","cert_title","working","job","masters"]

    def clean_job(j):
        j = str(j).strip().lower()
        for cluster, kws in JOB_CLUSTERS.items():
            if any(kw in j for kw in kws):
                return cluster
        return None

    df["job_clean"] = df["job"].apply(clean_job)
    df = df[df["job_clean"].notna()].copy()

    def make_text(row):
        return " ".join([str(row["course"]), str(row["specialization"]),
                         str(row["interests"]), str(row["skills"]),
                         str(row["cert_title"]), str(row["masters"])]).lower()

    df["text_feat"] = df.apply(make_text, axis=1)

    def parse_cgpa(v):
        try:
            v = float(str(v).replace("%","").strip())
            return v if v <= 10 else v / 10
        except:
            return 6.0

    df["cgpa_norm"] = df["cgpa"].apply(parse_cgpa)

    le    = LabelEncoder()
    y     = le.fit_transform(df["job_clean"])
    tfidf = TfidfVectorizer(max_features=600, ngram_range=(1,2), min_df=1)
    X_txt = tfidf.fit_transform(df["text_feat"])
    X     = sp.hstack([X_txt, sp.csr_matrix(df[["cgpa_norm"]].values)])

    clf = RandomForestClassifier(n_estimators=250, random_state=42,
                                 class_weight="balanced", n_jobs=-1)
    clf.fit(X, y)
    return clf, le, tfidf


def predict_careers(course, spec, interests, skills, cert, masters, cgpa, top_k=6):
    import scipy.sparse as sp
    clf, le, tfidf = load_and_train()
    text    = " ".join([course, spec, " ".join(interests), " ".join(skills), cert, masters]).lower()
    X_txt   = tfidf.transform([text])
    cgpa_n  = cgpa if cgpa <= 10 else cgpa / 10
    X       = sp.hstack([X_txt, sp.csr_matrix([[cgpa_n]])])
    proba   = clf.predict_proba(X)[0]
    top_idx = np.argsort(proba)[::-1][:top_k]
    return [{"role": le.classes_[i], "score": round(float(proba[i]) * 100, 1)} for i in top_idx]


def compute_ats(resume_text, target_role=None):
    tl = resume_text.lower()
    sec_scores, found_kws = {}, {}

    for cat, kws in SKILL_KEYWORDS.items():
        hits = [kw for kw in kws if kw in tl]
        sec_scores[cat] = min(len(hits) / max(len(kws) * 0.4, 1), 1.0)
        if hits:
            found_kws[cat] = hits

    jd_score, jd_hits = 0.0, []
    if target_role and target_role in ATS_JD_KEYWORDS:
        jd_kws   = ATS_JD_KEYWORDS[target_role]
        jd_hits  = [k for k in jd_kws if k in tl]
        jd_score = len(jd_hits) / len(jd_kws)

    checks = {
        "Email found":       bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', resume_text)),
        "Phone found":       bool(re.search(r'(\+?\d[\d\s\-]{8,}\d)', resume_text)),
        "LinkedIn URL":      "linkedin" in tl,
        "GitHub URL":        "github"   in tl,
        "Education section": any(w in tl for w in ["education","university","college","bachelor","master","b.tech","degree"]),
        "Experience section":any(w in tl for w in ["experience","work","internship","project","company"]),
        "Skills section":    any(w in tl for w in ["skill","proficient","expertise","technologies","tools"]),
    }
    struct  = sum(checks.values()) / 7
    skill_a = np.mean(list(sec_scores.values())) if sec_scores else 0
    overall = (0.45*jd_score + 0.35*skill_a + 0.20*struct) if target_role else (0.55*skill_a + 0.45*struct)
    overall = min(overall * 1.25, 1.0)

    return {
        "overall":       round(overall * 100),
        "skill_match":   round(skill_a  * 100),
        "jd_match":      round(jd_score * 100),
        "structure":     round(struct   * 100),
        "found_keywords":found_kws,
        "jd_hits":       jd_hits,
        "checks":        checks,
    }


def extract_text(uploaded_file):
    fname = uploaded_file.name.lower()
    raw   = uploaded_file.read()
    if fname.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    if fname.endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        except Exception:
            pass
        try:
            import PyPDF2
            r = PyPDF2.PdfReader(io.BytesIO(raw))
            return "\n".join(p.extract_text() or "" for p in r.pages)
        except Exception:
            return ""
    if fname.endswith(".docx"):
        try:
            from docx import Document
            return "\n".join(p.text for p in Document(io.BytesIO(raw)).paragraphs)
        except Exception:
            return ""
    return ""


def ats_color(s):
    return "#059669" if s >= 75 else "#d97706" if s >= 50 else "#dc2626"


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="badge">ML-POWERED · 1,195 GRADUATE PROFILES</div>
  <h1>Smart Career <span>Advisor</span></h1>
  <p>AI-driven career predictions for technical &amp; non-technical roles · Resume ATS scoring</p>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading ML model…"):
    load_and_train()

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📋  Profile & Predict", "📄  Resume ATS Score", "📊  About the Model"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    col_l, col_r = st.columns([1.1, 1], gap="large")

    with col_l:
        st.markdown('<div class="card"><h3>🎓 Academic Background</h3>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
            gender = st.selectbox("Gender", ["Prefer not to say","Female","Male","Other"])
        with c2:
            course = st.selectbox("UG Course / Degree", [
                "B.Tech","B.E","B.Sc","BCA","BBA","B.Com","BA","B.Arch",
                "B.Pharm","BALLB","BMS","MBA","MCA","M.Tech","M.Sc","Diploma","Other"])
            cgpa   = st.number_input("CGPA / Percentage", 0.0, 100.0, 72.0, 0.5)
        spec    = st.text_input("Specialization / Major",
                                placeholder="e.g. Computer Science, Electronics, Commerce…")
        masters = st.text_input("Masters / PG (optional)",
                                placeholder="e.g. M.Tech in AI, MBA Finance — leave blank if none")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card"><h3>🛠️ Skills & Interests</h3>', unsafe_allow_html=True)
        interests = st.multiselect("Your Interests", [
            "Technology","Data Analytics","Data Science","Machine Learning / AI",
            "Web Development","Cloud Computing","Cyber Security","Software Development",
            "Business & Management","Financial Analysis","Sales / Marketing",
            "Teaching & Education","Research & Development","Design & Creativity",
            "Healthcare & Medicine","Civil / Structural Engineering","Mechanical Engineering",
            "Journalism / Content Writing","Legal / Company Secretary","Supply Chain / Logistics",
            "HR / People Management","Game Development","Social Media",
            "Entrepreneurship","Government Jobs",
        ])
        skills = st.multiselect("Your Skills (select all that apply)", [
            "Python","Java","C++","JavaScript","SQL","R","MATLAB",
            "Machine Learning","Deep Learning","Data Analysis","Power BI","Tableau","Excel",
            "AWS","Azure","Docker","Kubernetes","Linux","Git","DevOps",
            "React","Node.js","HTML/CSS","Django","Flask","PHP",
            "Cyber Security","Ethical Hacking","Network Security",
            "AutoCAD","SolidWorks","CATIA","STAAD Pro",
            "Figma","Adobe XD","Photoshop","Illustrator",
            "Project Management","Agile / Scrum","Leadership",
            "Communication Skills","Critical Thinking","Problem Solving",
            "Accounting / Tally","Financial Modeling","CFA / CPA",
            "Digital Marketing","SEO/SEM","CRM / Salesforce",
            "Research / Academic Writing","SPSS / Stata",
            "Medical / Clinical Skills","Teaching / Pedagogy",
        ])
        cert = st.text_input("Certifications (optional)",
                             placeholder="e.g. AWS, Google Data Analytics, CFA Level 1")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    btn = st.button("🚀  Get My Career Predictions", use_container_width=True)

    if btn:
        if not spec.strip():
            st.warning("⚠️ Please fill in your specialization to continue.")
        else:
            with st.spinner("Analysing your profile against 1,195 graduate records…"):
                preds = predict_careers(course, spec, interests, skills, cert, masters, cgpa)

            st.markdown("---")
            st.markdown(f"### 🎯 Career Matches for **{name or 'you'}**")
            st.markdown("<p style='color:#64748b;margin-bottom:20px'>Ranked by ML confidence · Based on real graduate profiles</p>",
                        unsafe_allow_html=True)

            # top 3 cards
            cols = st.columns(3)
            medals = ["🥇","🥈","🥉"]
            for i, pred in enumerate(preds[:3]):
                clr = ROLE_COLORS[i]
                with cols[i]:
                    st.markdown(f"""
                    <div style="background:#ffffff;border:1px solid {clr}33;
                                border-top:3px solid {clr};border-radius:14px;
                                padding:20px;text-align:center;margin-bottom:6px;
                                box-shadow:0 2px 8px rgba(15,23,42,.07)">
                      <div style="font-size:26px;margin-bottom:8px">{medals[i]}</div>
                      <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:8px">{pred['role']}</div>
                      <div style="font-size:30px;font-weight:800;color:{clr};
                                  font-family:'DM Mono',monospace">{pred['score']}%</div>
                      <div style="font-size:11px;color:#94a3b8;margin-top:4px">match score</div>
                    </div>""", unsafe_allow_html=True)
                    st.progress(int(pred["score"]))

            st.markdown("<br>", unsafe_allow_html=True)

            # salary & skill gap
            top_role = preds[0]["role"]
            gap = [kw for kw in ATS_JD_KEYWORDS.get(top_role, [])
                   if not any(kw in s.lower() for s in skills)][:6]
            tip = CAREER_TIPS.get(top_role, "Keep building domain-specific skills and practical experience.")

            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"""
                <div class="card"><h3>📚 Skills Gap — {top_role}</h3>
                  {'<p style="color:#059669;font-size:13px;font-weight:600">✅ Your skills align well!</p>'
                   if not gap else
                   '<p style="color:#64748b;font-size:13px">Skills to acquire:</p>' +
                   ''.join(f'<span class="pill pill-miss">{g}</span>' for g in gap)}
                </div>""", unsafe_allow_html=True)
            with sc2:
                st.markdown(f"""
                <div class="card"><h3>💡 Career Tip</h3>
                  <p style="font-size:13px;line-height:1.7;color:#475569">{tip}</p>
                </div>""", unsafe_allow_html=True)

            # remaining roles
            st.markdown("**Other Strong Matches**")
            for i, pred in enumerate(preds[3:], 3):
                clr  = ROLE_COLORS[i % len(ROLE_COLORS)]
                keys = list(ATS_JD_KEYWORDS.get(pred["role"], {}))[: 4]
                st.markdown(f"""
                <div class="res-card" style="border-color:{clr}">
                  <div class="res-title">
                    <span style="background:{clr}18;color:{clr};border-radius:5px;
                                 padding:1px 9px;font-size:10px;font-weight:700;
                                 font-family:'DM Mono',monospace;margin-right:8px">#{i+1}</span>
                    {pred['role']}
                    <span style="float:right;color:{clr};font-size:13px;
                                 font-family:'DM Mono',monospace;font-weight:700">{pred['score']}%</span>
                  </div>
                  <div class="res-desc">Key skills: {", ".join(keys)}</div>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — ATS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns([1, 1.15], gap="large")

    with col_a:
        st.markdown('<div class="card"><h3>📤 Upload Resume</h3>', unsafe_allow_html=True)
        uploaded  = st.file_uploader("Drag & drop or browse",
                                     type=["pdf","docx","txt"],
                                     help="Supported: PDF, DOCX, TXT",
                                     label_visibility="collapsed")
        tgt_role  = st.selectbox("Target Job Role (optional — improves ATS analysis)",
                                 ["(Auto-detect)"] + list(JOB_CLUSTERS.keys()))
        tgt_role  = None if tgt_role == "(Auto-detect)" else tgt_role
        ats_btn   = st.button("🔍  Analyse Resume", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card"><h3>What is an ATS Score?</h3>
        <p style="font-size:13.5px;line-height:1.8;color:#475569">
          Applicant Tracking Systems screen resumes before a recruiter sees them.
          A high score means your resume is <b style="color:#0891b2">keyword-rich,
          well-structured, and relevant</b> to the role.<br><br>
          <b style="color:#059669">75–100</b> — Excellent · passes most ATS filters<br>
          <b style="color:#d97706">50–74</b> — Good · minor improvements needed<br>
          <b style="color:#dc2626">0–49</b> — Needs work · add relevant keywords
        </p></div>""", unsafe_allow_html=True)

    with col_b:
        if ats_btn and uploaded:
            with st.spinner("Parsing resume…"):
                text = extract_text(uploaded)

            if not text.strip():
                st.error("⚠️ Could not extract text from this file. Try a text-based PDF or DOCX.")
            else:
                ats   = compute_ats(text, tgt_role)
                score = ats["overall"]
                clr   = ats_color(score)
                label = ("🟢 Excellent" if score >= 75 else "🟡 Good" if score >= 50
                         else "🔴 Needs Improvement")

                st.markdown(f"""
                <div class="card" style="text-align:center;border-top:3px solid {clr}">
                  <p style="color:#94a3b8;font-size:11px;letter-spacing:1.5px;font-weight:600;margin:0 0 6px">ATS SCORE</p>
                  <div class="ats-num" style="color:{clr}">{score}</div>
                  <p style="color:{clr};font-weight:700;font-size:15px;margin:0">{label}</p>
                </div>""", unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                m1.metric("Skill Match",  f"{ats['skill_match']}%")
                m2.metric("JD Match",     f"{ats['jd_match']}%" if tgt_role else "N/A")
                m3.metric("Structure",    f"{ats['structure']}%")

                st.markdown("<br>**📋 Resume Structure Checklist**", unsafe_allow_html=True)
                chk_cols = st.columns(2)
                for i, (lbl, passed) in enumerate(ats["checks"].items()):
                    icon  = "✅" if passed else "❌"
                    color2 = "#059669" if passed else "#dc2626"
                    with chk_cols[i % 2]:
                        st.markdown(f"<span style='color:{color2};font-size:13px'>{icon} {lbl}</span>",
                                    unsafe_allow_html=True)

                if ats["found_keywords"]:
                    st.markdown("<br>**🔑 Keywords Detected**", unsafe_allow_html=True)
                    for cat, kws in list(ats["found_keywords"].items())[:6]:
                        st.markdown(f"<p style='color:#94a3b8;font-size:11px;margin:8px 0 4px;"
                                    f"text-transform:uppercase;letter-spacing:1px'>{cat}</p>",
                                    unsafe_allow_html=True)
                        st.markdown("".join(
                            f'<span class="pill">{kw}</span>' for kw in kws
                        ), unsafe_allow_html=True)

                missing = [k for k, v in ats["checks"].items() if not v]
                if missing:
                    st.markdown(f"""
                    <br><div style="background:#fff1f2;border:1px solid #fecdd3;
                                border-radius:12px;padding:18px 22px;margin-top:8px">
                      <h4 style="color:#be123c;margin:0 0 10px;font-size:14px">⚠️ Improve Your Resume</h4>
                      {"".join(f'<p style="color:#f43f5e;margin:4px 0;font-size:13px">• Add <b>{s.lower()}</b></p>'
                               for s in missing)}
                    </div>""", unsafe_allow_html=True)

        elif ats_btn and not uploaded:
            st.warning("⚠️ Please upload a resume file first.")
        else:
            st.markdown("""
            <div style="background:#ffffff;border:2px dashed #cbd5e1;
                        border-radius:14px;padding:60px 30px;text-align:center;margin-top:8px">
              <div style="font-size:48px;margin-bottom:12px">📄</div>
              <p style="color:#94a3b8;font-size:15px;margin:0">
                Upload your resume on the left<br>to see your ATS score
              </p>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ABOUT
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Training Records", "1,195")
    c2.metric("Job Categories",   str(len(JOB_CLUSTERS)))
    c3.metric("ML Algorithm",     "Random Forest")
    c4.metric("Feature Engine",   "TF-IDF + CGPA")

    st.markdown("<br>", unsafe_allow_html=True)
    col_i, col_ii = st.columns(2)

    with col_i:
        st.markdown("""
        <div class="card"><h3>🧠 How the Model Works</h3>
        <p style="font-size:13.5px;line-height:1.9;color:#475569">
          <b style="color:#0f172a">1. Data Collection</b><br>
          Survey data from 1,195 graduates across engineering, management, arts, science, law, and healthcare.<br><br>
          <b style="color:#0f172a">2. Preprocessing</b><br>
          Job titles are cleaned and mapped to 22 career clusters. Skills, interests, course, and CGPA are vectorized using TF-IDF.<br><br>
          <b style="color:#0f172a">3. Class Balancing</b><br>
          Random Forest trained with <code>class_weight="balanced"</code> handles unequal career distributions fairly.<br><br>
          <b style="color:#0f172a">4. Prediction</b><br>
          Top-k predictions returned with probability scores showing how closely your profile matches each career cluster.
        </p></div>""", unsafe_allow_html=True)

    with col_ii:
        tech_roles = [r for r in JOB_CLUSTERS if any(
            w in r.lower() for w in ["engineer","developer","data","cyber","cloud","devops","web","database","embedded","quality"])]
        non_tech = [r for r in JOB_CLUSTERS if r not in tech_roles]
        st.markdown(f"""
        <div class="card"><h3>📊 Career Categories Covered</h3>
        <p style="color:#0891b2;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:6px">
          TECHNICAL ({len(tech_roles)})</p>
        {"".join(f'<p style="color:#475569;font-size:13px;margin:3px 0">▸ {r}</p>' for r in tech_roles)}
        <p style="color:#6366f1;font-size:11px;font-weight:700;letter-spacing:1px;margin:14px 0 6px">
          NON-TECHNICAL ({len(non_tech)})</p>
        {"".join(f'<p style="color:#475569;font-size:13px;margin:3px 0">▸ {r}</p>' for r in non_tech)}
        </div>""", unsafe_allow_html=True)

    # ── Installation block — use styled <div> instead of <pre> to guarantee dark text ──
    st.markdown("""
    <div class="card"><h3>📦 Installation</h3>
      <div class="install-block">pip install -r requirements.txt</div>
      <div class="install-block">streamlit run app.py</div>
    </div>""", unsafe_allow_html=True)