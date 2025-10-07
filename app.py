import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from collections import Counter
import json

st.set_page_config(
    page_title="RetentionIQ Pro - Attrition Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Grey Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ECF0F1 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h3 {
        color: #BDC3C7 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 12px !important;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        letter-spacing: -1px;
    }
    
    h2, h3 {
        color: #2C3E50 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(44, 62, 80, 0.08);
        border: 1px solid #E9ECEF;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #5D6D7E 0%, #85929E 100%);
    }
    
    .metric-card:hover {
        box-shadow: 0 12px 48px rgba(44, 62, 80, 0.15);
        transform: translateY(-4px);
        border-color: #5D6D7E;
    }
    
    /* Employee Cards */
    .employee-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #95A5A6;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .employee-card:hover {
        box-shadow: 0 8px 32px rgba(44, 62, 80, 0.15);
        transform: translateX(4px);
    }
    
    /* Risk Level Colors */
    .risk-critical {
        border-left-color: #2C3E50 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
    }
    
    .risk-high {
        border-left-color: #566573 !important;
    }
    
    .risk-medium {
        border-left-color: #7F8C8D !important;
    }
    
    .risk-low {
        border-left-color: #95A5A6 !important;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 24px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        color: white;
    }
    
    .badge-high {
        background: linear-gradient(135deg, #566573 0%, #5D6D7E 100%);
        color: white;
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #7F8C8D 0%, #85929E 100%);
        color: white;
    }
    
    .badge-low {
        background: linear-gradient(135deg, #95A5A6 0%, #ABB2B9 100%);
        color: white;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        box-shadow: 0 6px 20px rgba(44, 62, 80, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #1A252F 0%, #2C3E50 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(44, 62, 80, 0.35) !important;
    }
    
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background: linear-gradient(135deg, #7F8C8D 0%, #95A5A6 100%) !important;
    }
    
    /* Intervention Cards */
    .intervention-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #5D6D7E;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.08);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #ECF0F1 0%, #D5DBDB 100%);
        border-left: 5px solid #2C3E50;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 12px rgba(44, 62, 80, 0.06);
    }
    
    /* Priority Cards */
    .priority-critical {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(44, 62, 80, 0.2);
    }
    
    .priority-high {
        background: linear-gradient(135deg, #566573 0%, #5D6D7E 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(86, 101, 115, 0.2);
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #7F8C8D 0%, #85929E 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(127, 140, 141, 0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #2C3E50 0%, #566573 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #7F8C8D !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2C3E50 0%, #566573 100%);
        border-radius: 10px;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(44, 62, 80, 0.08);
        border: 1px solid #E9ECEF;
    }
    
    /* Forms */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        border: 2px solid #D5DBDB !important;
        border-radius: 10px !important;
        padding: 14px !important;
        font-size: 15px !important;
        transition: all 0.2s !important;
        background: white !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #5D6D7E !important;
        box-shadow: 0 0 0 3px rgba(93, 109, 126, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: white;
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #7F8C8D;
        font-weight: 700;
        padding: 14px 28px;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-size: 12px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #F8F9FA;
        color: #2C3E50;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        color: white !important;
        box-shadow: 0 4px 16px rgba(44, 62, 80, 0.25);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border-left: 4px solid #5D6D7E !important;
        font-weight: 700 !important;
        padding: 18px !important;
        box-shadow: 0 2px 12px rgba(44, 62, 80, 0.06) !important;
        transition: all 0.2s !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F8F9FA !important;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.12) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #ECF0F1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #5D6D7E 0%, #7F8C8D 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2C3E50 0%, #566573 100%);
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #ECF0F1 0%, #D5DBDB 100%);
        border-left: 4px solid #5D6D7E;
        border-radius: 12px;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #D5DBDB 0%, #BDC3C7 100%);
        border-left: 4px solid #2C3E50;
        border-radius: 12px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #F8F9FA 0%, #ECF0F1 100%);
        border-left: 4px solid #7F8C8D;
        border-radius: 12px;
    }
    
    /* Risk Score Display */
    .risk-score-display {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #2C3E50 0%, #566573 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    /* Stat Cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(44, 62, 80, 0.06);
        border-left: 3px solid #95A5A6;
        margin: 8px 0;
        transition: all 0.2s;
    }
    
    .stat-card:hover {
        border-left-color: #2C3E50;
        box-shadow: 0 6px 24px rgba(44, 62, 80, 0.12);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced data
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {
            'id': 1,
            'name': 'Sarah Johnson',
            'department': 'Engineering',
            'role': 'Senior Software Engineer',
            'tenure_months': 18,
            'performance_score': 4.2,
            'engagement_score': 3.1,
            'last_promotion_months': 24,
            'salary_percentile': 45,
            'manager_1on1_frequency': 2,
            'recent_absences': 4,
            'peer_review_score': 3.8,
            'training_hours': 8,
            'overtime_hours': 45,
            'team_changes': 2,
            'manager_changes': 1,
            'projects_completed': 12,
            'certifications': 2,
            'mentorship_hours': 0,
            'feedback_received': 3
        },
        {
            'id': 2,
            'name': 'Michael Chen',
            'department': 'Sales',
            'role': 'Account Executive',
            'tenure_months': 36,
            'performance_score': 4.8,
            'engagement_score': 4.5,
            'last_promotion_months': 12,
            'salary_percentile': 75,
            'manager_1on1_frequency': 4,
            'recent_absences': 1,
            'peer_review_score': 4.6,
            'training_hours': 24,
            'overtime_hours': 15,
            'team_changes': 0,
            'manager_changes': 0,
            'projects_completed': 28,
            'certifications': 3,
            'mentorship_hours': 15,
            'feedback_received': 8
        },
        {
            'id': 3,
            'name': 'Emily Rodriguez',
            'department': 'Marketing',
            'role': 'Marketing Manager',
            'tenure_months': 8,
            'performance_score': 3.9,
            'engagement_score': 2.8,
            'last_promotion_months': 30,
            'salary_percentile': 40,
            'manager_1on1_frequency': 1,
            'recent_absences': 6,
            'peer_review_score': 3.5,
            'training_hours': 4,
            'overtime_hours': 60,
            'team_changes': 3,
            'manager_changes': 2,
            'projects_completed': 8,
            'certifications': 1,
            'mentorship_hours': 0,
            'feedback_received': 2
        },
        {
            'id': 4,
            'name': 'David Park',
            'department': 'Engineering',
            'role': 'Tech Lead',
            'tenure_months': 48,
            'performance_score': 4.5,
            'engagement_score': 4.2,
            'last_promotion_months': 18,
            'salary_percentile': 70,
            'manager_1on1_frequency': 3,
            'recent_absences': 2,
            'peer_review_score': 4.4,
            'training_hours': 20,
            'overtime_hours': 25,
            'team_changes': 1,
            'manager_changes': 0,
            'projects_completed': 35,
            'certifications': 4,
            'mentorship_hours': 20,
            'feedback_received': 10
        },
        {
            'id': 5,
            'name': 'Jessica Martinez',
            'department': 'Product',
            'role': 'Product Manager',
            'tenure_months': 14,
            'performance_score': 4.0,
            'engagement_score': 3.3,
            'last_promotion_months': 20,
            'salary_percentile': 50,
            'manager_1on1_frequency': 2,
            'recent_absences': 3,
            'peer_review_score': 3.9,
            'training_hours': 12,
            'overtime_hours': 40,
            'team_changes': 1,
            'manager_changes': 1,
            'projects_completed': 15,
            'certifications': 2,
            'mentorship_hours': 5,
            'feedback_received': 5
        },
        {
            'id': 6,
            'name': 'Alex Thompson',
            'department': 'Data Science',
            'role': 'Data Scientist',
            'tenure_months': 22,
            'performance_score': 4.4,
            'engagement_score': 3.6,
            'last_promotion_months': 15,
            'salary_percentile': 65,
            'manager_1on1_frequency': 3,
            'recent_absences': 2,
            'peer_review_score': 4.2,
            'training_hours': 30,
            'overtime_hours': 20,
            'team_changes': 0,
            'manager_changes': 0,
            'projects_completed': 18,
            'certifications': 3,
            'mentorship_hours': 10,
            'feedback_received': 6
        }
    ]

# DATA MIGRATION: Add missing fields to existing employees
REQUIRED_FIELDS = {
    'mentorship_hours': 0,
    'feedback_received': 3,
    'projects_completed': 10,
    'certifications': 1,
    'peer_review_score': 3.5,
    'training_hours': 10,
    'overtime_hours': 20,
    'team_changes': 0,
    'manager_changes': 0,
    'recent_absences': 2
}

for emp in st.session_state.employees:
    for field, default_value in REQUIRED_FIELDS.items():
        if field not in emp:
            emp[field] = default_value

if 'interventions' not in st.session_state:
    st.session_state.interventions = []

if 'exit_interviews' not in st.session_state:
    st.session_state.exit_interviews = [
        {
            'employee': 'John Smith',
            'department': 'Engineering',
            'tenure_months': 24,
            'reason_primary': 'Compensation',
            'reason_secondary': 'Career Growth',
            'would_recommend': False,
            'manager_rating': 3,
            'date': '2024-12-15',
            'satisfaction_score': 2.5
        },
        {
            'employee': 'Lisa Wang',
            'department': 'Sales',
            'tenure_months': 18,
            'reason_primary': 'Work-Life Balance',
            'reason_secondary': 'Management',
            'would_recommend': True,
            'manager_rating': 4,
            'date': '2025-01-05',
            'satisfaction_score': 3.5
        },
        {
            'employee': 'Robert Kim',
            'department': 'Marketing',
            'tenure_months': 30,
            'reason_primary': 'Career Growth',
            'reason_secondary': 'Compensation',
            'would_recommend': True,
            'manager_rating': 4,
            'date': '2024-11-20',
            'satisfaction_score': 3.8
        }
    ]

# Enhanced risk calculation engine
def calculate_attrition_risk(employee):
    """Enhanced attrition risk calculation with weighted factors"""
    
    risk_score = 0
    risk_factors = []
    confidence_level = 100
    
    # Use .get() method with defaults to avoid KeyError
    engagement_score = employee.get('engagement_score', 3.5)
    performance_score = employee.get('performance_score', 3.5)
    salary_percentile = employee.get('salary_percentile', 50)
    last_promotion_months = employee.get('last_promotion_months', 18)
    training_hours = employee.get('training_hours', 10)
    tenure_months = employee.get('tenure_months', 12)
    manager_1on1_frequency = employee.get('manager_1on1_frequency', 2)
    overtime_hours = employee.get('overtime_hours', 20)
    recent_absences = employee.get('recent_absences', 2)
    team_changes = employee.get('team_changes', 0)
    manager_changes = employee.get('manager_changes', 0)
    peer_review_score = employee.get('peer_review_score', 3.5)
    mentorship_hours = employee.get('mentorship_hours', 0)
    certifications = employee.get('certifications', 1)
    
    # ENGAGEMENT (Weight: 30%) - Most critical factor
    if engagement_score < 2.5:
        risk_score += 30
        risk_factors.append(("Critical: Severely low engagement", "Critical"))
    elif engagement_score < 3.0:
        risk_score += 25
        risk_factors.append(("Low engagement score", "High"))
    elif engagement_score < 3.5:
        risk_score += 15
        risk_factors.append(("Below average engagement", "Medium"))
    
    # PERFORMANCE-ENGAGEMENT MISMATCH (Weight: 25%)
    if performance_score >= 4.2 and engagement_score < 3.5:
        risk_score += 25
        risk_factors.append(("High performer with low engagement - FLIGHT RISK", "Critical"))
        confidence_level += 15
    
    # COMPENSATION (Weight: 20%)
    if salary_percentile < 40:
        risk_score += 20
        risk_factors.append(("Significantly below market compensation", "Critical"))
    elif salary_percentile < 50:
        risk_score += 15
        risk_factors.append(("Below market compensation", "High"))
    
    # CAREER DEVELOPMENT (Weight: 15%)
    if last_promotion_months > 30:
        risk_score += 15
        risk_factors.append(("No promotion in 2.5+ years", "High"))
    elif last_promotion_months > 24:
        risk_score += 10
        risk_factors.append(("No promotion in 2+ years", "Medium"))
    
    if training_hours < 10:
        risk_score += 8
        risk_factors.append(("Minimal learning & development", "Medium"))
    
    # TENURE RISK (Weight: 10%)
    if tenure_months < 12:
        risk_score += 12
        risk_factors.append(("Early tenure (< 1 year) - high turnover period", "High"))
    elif 18 <= tenure_months <= 30:
        risk_score += 8
        risk_factors.append(("Critical tenure window (18-30 months)", "Medium"))
    
    # MANAGER RELATIONSHIP (Weight: 10%)
    if manager_1on1_frequency < 2:
        risk_score += 12
        risk_factors.append(("Infrequent manager check-ins", "High"))
    
    # WORKLOAD & BURNOUT (Weight: 10%)
    if overtime_hours > 60:
        risk_score += 15
        risk_factors.append(("Excessive overtime - severe burnout risk", "Critical"))
    elif overtime_hours > 50:
        risk_score += 12
        risk_factors.append(("High overtime - burnout risk", "High"))
    
    if recent_absences > 5:
        risk_score += 10
        risk_factors.append(("Increased absences (disengagement indicator)", "Medium"))
    
    # ORGANIZATIONAL INSTABILITY (Weight: 8%)
    if team_changes > 2:
        risk_score += 8
        risk_factors.append(("Multiple team changes", "Medium"))
    
    if manager_changes > 1:
        risk_score += 10
        risk_factors.append(("Multiple manager changes (instability)", "High"))
    
    # PEER DISCONNECT (Weight: 5%)
    if abs(performance_score - peer_review_score) > 0.7:
        risk_score += 10
        risk_factors.append(("Significant performance-peer review disconnect", "Medium"))
    
    # POSITIVE FACTORS (Risk Reduction)
    if mentorship_hours > 10:
        risk_score -= 5
        risk_factors.append(("Active mentor (protective factor)", "Positive"))
    
    if certifications >= 3:
        risk_score -= 3
        risk_factors.append(("Invested in certifications", "Positive"))
    
    # Cap at 100
    risk_score = max(0, min(100, risk_score))
    confidence_level = min(100, confidence_level)
    
    return risk_score, risk_factors, confidence_level

def get_risk_level(score):
    """Enhanced risk categorization"""
    if score >= 75:
        return 'Critical', 'critical', '#2C3E50'
    elif score >= 55:
        return 'High', 'high', '#566573'
    elif score >= 35:
        return 'Medium', 'medium', '#7F8C8D'
    else:
        return 'Low', 'low', '#95A5A6'

def generate_interventions(employee, risk_factors):
    """Generate comprehensive intervention recommendations"""
    interventions = []
    
    factor_texts = [f[0] for f in risk_factors]
    
    # Critical interventions
    if any("severely low engagement" in f.lower() or "flight risk" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Critical',
            'action': 'Emergency Retention Meeting',
            'description': f'Immediate executive-level conversation with {employee["name"]}. Discuss career aspirations, concerns, and potential counteroffers. Authorized to make on-spot commitments within approved budget.',
            'timeline': 'Within 24 hours',
            'owner': 'Department Head + HR Director',
            'estimated_cost': 'Up to $25K retention package',
            'success_probability': '65%'
        })
    
    if any("high performer with low engagement" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Critical',
            'action': 'High Performer Retention Program',
            'description': 'Enroll in executive fast-track program. Provide visibility to C-suite, challenging projects, and clear path to senior leadership. Consider spot bonus or equity refresh.',
            'timeline': 'Immediate',
            'owner': 'VP + CEO',
            'estimated_cost': '$15K-$40K',
            'success_probability': '70%'
        })
    
    if any("below market compensation" in f.lower() or "significantly below" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Critical',
            'action': 'Emergency Compensation Review',
            'description': 'Conduct immediate market analysis. Approve off-cycle salary adjustment to at least 60th percentile. Consider sign-on equivalent retention bonus.',
            'timeline': 'Within 1 week',
            'owner': 'HR + Finance + Direct Manager',
            'estimated_cost': f'${(100 - employee.get("salary_percentile", 50)) * 800:,.0f} annual adjustment',
            'success_probability': '80%'
        })
    
    # High priority interventions
    if any("no promotion" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'High',
            'action': 'Accelerated Career Development Plan',
            'description': 'Create detailed 6-month promotion roadmap with specific deliverables. Assign executive mentor. Schedule monthly progress reviews with skip-level manager.',
            'timeline': 'Within 1 week',
            'owner': 'Direct Manager + Department Head',
            'estimated_cost': '$2K (mentor time + resources)',
            'success_probability': '75%'
        })
    
    if any("infrequent" in f.lower() and "check-in" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'High',
            'action': 'Enhanced Manager Engagement Protocol',
            'description': 'Mandate weekly 30-minute 1-on-1s with structured agenda: wins, challenges, career growth, and personal development. Manager to complete leadership coaching.',
            'timeline': 'This week',
            'owner': 'Direct Manager',
            'estimated_cost': '$500 (coaching)',
            'success_probability': '60%'
        })
    
    if any("burnout" in f.lower() or "excessive overtime" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Critical',
            'action': 'Immediate Workload Rebalancing',
            'description': 'Remove 30% of current workload. Redistribute to team or hire contractor. Mandatory 2-week "recovery period" with no new projects. Offer wellness stipend.',
            'timeline': 'Immediate',
            'owner': 'Direct Manager + Resource Planning',
            'estimated_cost': '$5K-$15K (contractor + stipend)',
            'success_probability': '70%'
        })
    
    # Medium priority interventions
    if any("learning" in f.lower() or "development" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Medium',
            'action': 'Personalized Learning & Development Plan',
            'description': f'Budget $3K for courses, conferences, or certifications aligned with {employee["name"]}\'s career goals. Approve 4 hours/week for learning during work hours.',
            'timeline': '2 weeks',
            'owner': 'Direct Manager + L&D Team',
            'estimated_cost': '$3K annually',
            'success_probability': '55%'
        })
    
    if any("team changes" in f.lower() or "manager changes" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Medium',
            'action': 'Stability & Integration Program',
            'description': 'Assign consistent project teams for next 6 months. Pair with senior buddy for organizational navigation. Monthly check-ins with skip-level manager.',
            'timeline': '1 week',
            'owner': 'Department Head',
            'estimated_cost': '$1K (buddy time)',
            'success_probability': '60%'
        })
    
    if any("early tenure" in f.lower() or "critical tenure" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'High',
            'action': 'Enhanced Onboarding & Integration',
            'description': 'Enroll in extended onboarding cohort. Assign peer mentor from same hire class. Schedule monthly "how are you really doing?" sessions with HR Business Partner.',
            'timeline': 'This week',
            'owner': 'HR Business Partner + Manager',
            'estimated_cost': '$800 (program admin)',
            'success_probability': '65%'
        })
    
    if any("disconnect" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Medium',
            'action': '360-Degree Feedback & Calibration',
            'description': 'Conduct comprehensive 360 review to understand perception gaps. Facilitate mediated discussion between employee, manager, and peers to align expectations.',
            'timeline': '2 weeks',
            'owner': 'HR Business Partner',
            'estimated_cost': '$1.5K (360 tool + facilitation)',
            'success_probability': '50%'
        })
    
    if any("absences" in f.lower() for f in factor_texts):
        interventions.append({
            'priority': 'Medium',
            'action': 'Wellness & Support Check-in',
            'description': 'Confidential HR conversation to understand root cause. Offer EAP services, flexible work arrangements, or additional PTO. Ensure no underlying health/personal crisis.',
            'timeline': '3-5 days',
            'owner': 'HR Business Partner',
            'estimated_cost': '$0 (existing benefits)',
            'success_probability': '55%'
        })
    
    # Sort by priority
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2}
    interventions.sort(key=lambda x: priority_order[x['priority']])
    
    return interventions

# Sidebar Navigation
st.sidebar.markdown("### 🎯 RETENTIONIQ PRO")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "NAVIGATE TO",
    ["📊 Dashboard", "👥 Employee Risk Profiles", "🎯 Intervention Manager", "📈 Analytics & Insights", "💬 Exit Intelligence", "➕ Add Employee"]
)

# DASHBOARD PAGE
if page == "📊 Dashboard":
    st.markdown("<h1>🎯 RetentionIQ Pro - Executive Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("### Real-time Attrition Intelligence & Predictive Analytics")
    st.markdown("---")
    
    # Calculate all metrics
    employees_df = pd.DataFrame(st.session_state.employees)
    risk_data = []
    
    for emp in st.session_state.employees:
        risk_score, risk_factors, confidence = calculate_attrition_risk(emp)
        risk_level, risk_class, _ = get_risk_level(risk_score)
        risk_data.append({
            'employee': emp,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_class': risk_class,
            'risk_factors': risk_factors,
            'confidence': confidence
        })
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = sum(1 for r in risk_data if r['risk_level'] == 'Critical')
    high_count = sum(1 for r in risk_data if r['risk_level'] == 'High')
    avg_risk = sum(r['risk_score'] for r in risk_data) / len(risk_data)
    total_employees = len(st.session_state.employees)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7F8C8D; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">CRITICAL RISK</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #2C3E50; line-height: 1;">{critical_count}</div>
            <div style="color: #95A5A6; font-size: 13px; margin-top: 8px; font-weight: 600;">Immediate action required</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7F8C8D; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">HIGH RISK</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #566573; line-height: 1;">{high_count}</div>
            <div style="color: #95A5A6; font-size: 13px; margin-top: 8px; font-weight: 600;">Needs intervention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7F8C8D; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">AVG RISK SCORE</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #7F8C8D; line-height: 1;">{avg_risk:.0f}</div>
            <div style="color: #95A5A6; font-size: 13px; margin-top: 8px; font-weight: 600;">Organization health</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        risk_percentage = ((critical_count + high_count) / total_employees * 100)
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7F8C8D; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">AT RISK</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #E74C3C; line-height: 1;">{risk_percentage:.0f}%</div>
            <div style="color: #95A5A6; font-size: 13px; margin-top: 8px; font-weight: 600;">Of total workforce</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚨 Highest Risk Employees - Immediate Action Required")
        
        # Sort by risk score
        risk_data_sorted = sorted(risk_data, key=lambda x: x['risk_score'], reverse=True)
        
        for item in risk_data_sorted[:4]:  # Top 4 highest risk
            emp = item['employee']
            risk_score = item['risk_score']
            risk_level = item['risk_level']
            risk_class = item['risk_class']
            
            st.markdown(f"""
            <div class="employee-card risk-{risk_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>
                        <h3 style="margin: 0; color: #2C3E50; font-size: 1.3rem;">{emp['name']}</h3>
                        <p style="margin: 4px 0 0 0; color: #7F8C8D; font-size: 14px; font-weight: 600;">{emp['role']} • {emp['department']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge badge-{risk_class}">{risk_level} RISK</span>
                        <div style="margin-top: 8px; font-size: 2rem; font-weight: 900; color: #2C3E50;">{risk_score}</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; padding: 16px; background: #F8F9FA; border-radius: 8px;">
                    <div>
                        <div style="font-size: 11px; color: #7F8C8D; font-weight: 700; margin-bottom: 4px;">TENURE</div>
                        <div style="font-size: 16px; font-weight: 700; color: #2C3E50;">{emp['tenure_months']}mo</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #7F8C8D; font-weight: 700; margin-bottom: 4px;">ENGAGEMENT</div>
                        <div style="font-size: 16px; font-weight: 700; color: #2C3E50;">{emp['engagement_score']}/5</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #7F8C8D; font-weight: 700; margin-bottom: 4px;">PERFORMANCE</div>
                        <div style="font-size: 16px; font-weight: 700; color: #2C3E50;">{emp['performance_score']}/5</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #7F8C8D; font-weight: 700; margin-bottom: 4px;">SALARY %</div>
                        <div style="font-size: 16px; font-weight: 700; color: #2C3E50;">{emp['salary_percentile']}th</div>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <div style="font-size: 11px; color: #7F8C8D; font-weight: 700; margin-bottom: 8px;">TOP RISK FACTORS:</div>
            """, unsafe_allow_html=True)
            
            for factor, severity in item['risk_factors'][:3]:
                severity_colors = {
                    'Critical': '#2C3E50',
                    'High': '#566573',
                    'Medium': '#7F8C8D',
                    'Positive': '#27AE60'
                }
                color = severity_colors.get(severity, '#95A5A6')
                st.markdown(f"""
                    <div style="display: flex; align-items: center; margin: 6px 0;">
                        <span style="width: 8px; height: 8px; background: {color}; border-radius: 50%; margin-right: 10px;"></span>
                        <span style="color: #34495E; font-size: 13px; font-weight: 500;">{factor}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # Risk Distribution Chart
        st.markdown("### 📊 Risk Distribution")
        risk_counts = Counter([r['risk_level'] for r in risk_data])
        
        fig_dist = go.Figure(data=[go.Pie(
            labels=list(risk_counts.keys()),
            values=list(risk_counts.values()),
            hole=0.5,
            marker=dict(colors=['#2C3E50', '#566573', '#7F8C8D', '#95A5A6']),
            textfont=dict(size=16, color='white', family='Inter'),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_dist.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=14, color='#2C3E50')
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Department Risk Analysis
        st.markdown("### 🏢 Department Risk Analysis")
        dept_risk = {}
        for item in risk_data:
            dept = item['employee']['department']
            if dept not in dept_risk:
                dept_risk[dept] = []
            dept_risk[dept].append(item['risk_score'])
        
        dept_avg_risk = {dept: sum(scores)/len(scores) for dept, scores in dept_risk.items()}
        dept_df = pd.DataFrame(list(dept_avg_risk.items()), columns=['Department', 'Avg Risk'])
        dept_df = dept_df.sort_values('Avg Risk', ascending=False)
        
        fig_dept = go.Figure(data=[go.Bar(
            y=dept_df['Department'],
            x=dept_df['Avg Risk'],
            orientation='h',
            marker=dict(
                color=dept_df['Avg Risk'],
                colorscale=[[0, '#95A5A6'], [0.5, '#7F8C8D'], [1, '#2C3E50']],
                showscale=False
            ),
            text=dept_df['Avg Risk'].round(0),
            textposition='outside',
            textfont=dict(size=14, color='#2C3E50', family='Inter', weight='bold')
        )])
        
        fig_dept.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E9ECEF', range=[0, 100]),
            yaxis=dict(showgrid=False),
            font=dict(family='Inter', size=12, color='#2C3E50')
        )
        
        st.plotly_chart(fig_dept, use_container_width=True)
        
        # Key Insights
        st.markdown("### 💡 Key Insights")
        st.markdown(f"""
        <div class="insight-box">
            <div style="font-weight: 700; margin-bottom: 12px; color: #2C3E50; font-size: 14px;">🎯 PRIORITY ACTIONS</div>
            <ul style="margin: 0; padding-left: 20px; color: #34495E; font-size: 13px; line-height: 1.8;">
                <li><strong>{critical_count + high_count}</strong> employees need immediate intervention</li>
                <li><strong>{len([r for r in risk_data if r['employee']['engagement_score'] < 3.0])}</strong> showing low engagement</li>
                <li><strong>{len([r for r in risk_data if r['employee']['salary_percentile'] < 50])}</strong> below market compensation</li>
                <li><strong>{len([r for r in risk_data if r['employee']['last_promotion_months'] > 24])}</strong> overdue for promotion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# EMPLOYEE RISK PROFILES PAGE
elif page == "👥 Employee Risk Profiles":
    st.markdown("<h1>👥 Employee Risk Profiles</h1>", unsafe_allow_html=True)
    st.markdown("### Detailed Risk Analysis & Intervention Recommendations")
    st.markdown("---")
    
    # Calculate risk for all employees
    risk_data = []
    for emp in st.session_state.employees:
        risk_score, risk_factors, confidence = calculate_attrition_risk(emp)
        risk_level, risk_class, color = get_risk_level(risk_score)
        risk_data.append({
            'employee': emp,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_class': risk_class,
            'risk_factors': risk_factors,
            'confidence': confidence,
            'color': color
        })
    
    # Sort by risk score
    risk_data_sorted = sorted(risk_data, key=lambda x: x['risk_score'], reverse=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.selectbox("Filter by Department", ["All"] + list(set(emp['department'] for emp in st.session_state.employees)))
    with col2:
        risk_filter = st.selectbox("Filter by Risk Level", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Risk Score (High to Low)", "Risk Score (Low to High)", "Name", "Department"])
    
    # Apply filters
    filtered_data = risk_data_sorted
    if dept_filter != "All":
        filtered_data = [r for r in filtered_data if r['employee']['department'] == dept_filter]
    if risk_filter != "All":
        filtered_data = [r for r in filtered_data if r['risk_level'] == risk_filter]
    
    # Apply sorting
    if sort_by == "Risk Score (Low to High)":
        filtered_data = sorted(filtered_data, key=lambda x: x['risk_score'])
    elif sort_by == "Name":
        filtered_data = sorted(filtered_data, key=lambda x: x['employee']['name'])
    elif sort_by == "Department":
        filtered_data = sorted(filtered_data, key=lambda x: x['employee']['department'])
    
    st.markdown(f"### Showing {len(filtered_data)} employees")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display employee profiles
    for item in filtered_data:
        emp = item['employee']
        risk_score = item['risk_score']
        risk_level = item['risk_level']
        risk_class = item['risk_class']
        risk_factors = item['risk_factors']
        confidence = item['confidence']
        
        with st.expander(f"{'🚨' if risk_level == 'Critical' else '⚠️' if risk_level == 'High' else '📊'} **{emp['name']}** - {emp['role']} | Risk Score: **{risk_score}** ({risk_level})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <h3 style="color: #2C3E50; margin-top: 0;">Employee Overview</h3>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">DEPARTMENT</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['department']}</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">ROLE</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['role']}</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">TENURE</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['tenure_months']} months</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">LAST PROMOTION</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['last_promotion_months']} months ago</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">PERFORMANCE SCORE</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['performance_score']}/5.0</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">ENGAGEMENT SCORE</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['engagement_score']}/5.0</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">SALARY PERCENTILE</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['salary_percentile']}th percentile</div>
                        </div>
                        <div>
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">1-ON-1 FREQUENCY</div>
                            <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{emp['manager_1on1_frequency']}/month</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Risk Factors
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🔍 Risk Factors Analysis")
                
                for factor, severity in risk_factors:
                    severity_class = severity.lower()
                    if severity == "Positive":
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #D5DBDB 0%, #BDC3C7 100%); padding: 12px 16px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #27AE60;">
                            <span style="color: #27AE60; font-weight: 700; font-size: 11px;">✓ {severity.upper()}</span>
                            <div style="color: #2C3E50; margin-top: 4px; font-size: 14px;">{factor}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        severity_colors = {'Critical': '#2C3E50', 'High': '#566573', 'Medium': '#7F8C8D', 'Low': '#95A5A6'}
                        color = severity_colors.get(severity, '#95A5A6')
                        st.markdown(f"""
                        <div style="background: white; padding: 12px 16px; border-radius: 8px; margin: 8px 0; border-left: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                            <span style="color: {color}; font-weight: 700; font-size: 11px;">⚠ {severity.upper()}</span>
                            <div style="color: #2C3E50; margin-top: 4px; font-size: 14px;">{factor}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                # Risk Score Visualization
                st.markdown(f"""
                <div style="background: white; padding: 24px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 16px;">ATTRITION RISK SCORE</div>
                    <div style="font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #2C3E50 0%, #566573 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;">{risk_score}</div>
                    <span class="badge badge-{risk_class}" style="margin-top: 16px;">{risk_level} RISK</span>
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #E9ECEF;">
                        <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">CONFIDENCE LEVEL</div>
                        <div style="color: #2C3E50; font-size: 2rem; font-weight: 700;">{confidence}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick Stats
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="stat-card">
                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">RECENT ABSENCES</div>
                    <div style="color: #2C3E50; font-size: 1.8rem; font-weight: 700;">{emp.get('recent_absences', 0)}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">OVERTIME HOURS</div>
                    <div style="color: #2C3E50; font-size: 1.8rem; font-weight: 700;">{emp.get('overtime_hours', 0)}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">TRAINING HOURS</div>
                    <div style="color: #2C3E50; font-size: 1.8rem; font-weight: 700;">{emp.get('training_hours', 0)}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">TEAM CHANGES</div>
                    <div style="color: #2C3E50; font-size: 1.8rem; font-weight: 700;">{emp.get('team_changes', 0)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommended Interventions
            st.markdown("---")
            st.markdown("### 🎯 Recommended Interventions")
            
            interventions = generate_interventions(emp, risk_factors)
            
            if interventions:
                for intervention in interventions:
                    priority_class = intervention['priority'].lower()
                    st.markdown(f"""
                    <div class="intervention-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                            <div>
                                <span class="badge badge-{priority_class}">{intervention['priority']} PRIORITY</span>
                                <h4 style="color: #2C3E50; margin: 12px 0 8px 0;">{intervention['action']}</h4>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: #7F8C8D; font-size: 11px; font-weight: 700;">SUCCESS RATE</div>
                                <div style="color: #27AE60; font-size: 1.5rem; font-weight: 700;">{intervention['success_probability']}</div>
                            </div>
                        </div>
                        <p style="color: #34495E; margin: 12px 0; line-height: 1.6;">{intervention['description']}</p>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #E9ECEF;">
                            <div>
                                <div style="color: #7F8C8D; font-size: 10px; font-weight: 700; margin-bottom: 4px;">TIMELINE</div>
                                <div style="color: #2C3E50; font-size: 13px; font-weight: 600;">{intervention['timeline']}</div>
                            </div>
                            <div>
                                <div style="color: #7F8C8D; font-size: 10px; font-weight: 700; margin-bottom: 4px;">OWNER</div>
                                <div style="color: #2C3E50; font-size: 13px; font-weight: 600;">{intervention['owner']}</div>
                            </div>
                            <div>
                                <div style="color: #7F8C8D; font-size: 10px; font-weight: 700; margin-bottom: 4px;">EST. COST</div>
                                <div style="color: #2C3E50; font-size: 13px; font-weight: 600;">{intervention['estimated_cost']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No specific interventions recommended at this time. Continue monitoring.")


# INTERVENTION MANAGER PAGE
elif page == "🎯 Intervention Manager":
    st.markdown("<h1>🎯 Intervention Manager</h1>", unsafe_allow_html=True)
    st.markdown("### Track and manage retention interventions")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📋 Active Interventions", "➕ Create New Intervention"])
    
    with tab1:
        if st.session_state.interventions:
            st.markdown(f"### {len(st.session_state.interventions)} Active Interventions")
            
            for idx, intervention in enumerate(st.session_state.interventions):
                priority_class = intervention['priority'].lower()
                status_colors = {'Planned': '#5D6D7E', 'In Progress': '#F39C12', 'Completed': '#27AE60', 'Cancelled': '#95A5A6'}
                status_color = status_colors.get(intervention.get('status', 'Planned'), '#7F8C8D')
                
                with st.expander(f"**{intervention.get('employee_name', 'Unknown')}** - {intervention.get('action', 'N/A')} ({intervention.get('status', 'Planned')})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 12px;">
                            <span class="badge badge-{priority_class}">{intervention.get('priority', 'Medium')} PRIORITY</span>
                            <h3 style="color: #2C3E50; margin: 16px 0 8px 0;">{intervention.get('action', 'N/A')}</h3>
                            <p style="color: #34495E; line-height: 1.6; margin: 12px 0;">{intervention.get('description', 'No description')}</p>
                            
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px;">
                                <div>
                                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">TIMELINE</div>
                                    <div style="color: #2C3E50; font-size: 14px; font-weight: 600;">{intervention.get('timeline', 'TBD')}</div>
                                </div>
                                <div>
                                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">OWNER</div>
                                    <div style="color: #2C3E50; font-size: 14px; font-weight: 600;">{intervention.get('owner', 'TBD')}</div>
                                </div>
                                <div>
                                    <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">ESTIMATED COST</div>
                                    <div style="color: #2C3E50; font-size: 14px; font-weight: 600;">{intervention.get('estimated_cost', 'TBD')}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Notes section
                        if 'notes' in intervention and intervention['notes']:
                            st.markdown("**📝 Notes:**")
                            st.info(intervention['notes'])
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background: {status_color}; color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 16px;">
                            <div style="font-size: 12px; opacity: 0.9; margin-bottom: 8px;">STATUS</div>
                            <div style="font-size: 1.5rem; font-weight: 700;">{intervention.get('status', 'Planned')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 12px; text-align: center;">
                            <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">SUCCESS PROBABILITY</div>
                            <div style="color: #27AE60; font-size: 2.5rem; font-weight: 900;">{intervention.get('success_probability', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Update status
                        new_status = st.selectbox(
                            "Update Status",
                            ["Planned", "In Progress", "Completed", "Cancelled"],
                            index=["Planned", "In Progress", "Completed", "Cancelled"].index(intervention.get('status', 'Planned')),
                            key=f"status_{idx}"
                        )
                        
                        if st.button("Update", key=f"update_{idx}"):
                            st.session_state.interventions[idx]['status'] = new_status
                            st.success("Status updated!")
                            st.rerun()
                        
                        if st.button("🗑️ Delete", key=f"delete_{idx}"):
                            st.session_state.interventions.pop(idx)
                            st.success("Intervention deleted!")
                            st.rerun()
        else:
            st.info("No active interventions. Create one from the 'Create New Intervention' tab or from employee risk profiles.")
    
    with tab2:
        st.markdown("### Create New Intervention")
        
        with st.form("new_intervention_form"):
            employee_name = st.selectbox("Select Employee", [emp['name'] for emp in st.session_state.employees])
            
            col1, col2 = st.columns(2)
            with col1:
                priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
                action = st.text_input("Action Title", placeholder="e.g., Emergency Retention Meeting")
            
            with col2:
                timeline = st.text_input("Timeline", placeholder="e.g., Within 24 hours")
                owner = st.text_input("Owner", placeholder="e.g., Department Head + HR")
            
            description = st.text_area("Description", placeholder="Detailed description of the intervention...")
            estimated_cost = st.text_input("Estimated Cost", placeholder="e.g., $5,000")
            success_probability = st.slider("Success Probability", 0, 100, 50, help="Estimated likelihood of success")
            notes = st.text_area("Additional Notes (Optional)")
            
            submitted = st.form_submit_button("Create Intervention")
            
            if submitted:
                if action and description:
                    new_intervention = {
                        'employee_name': employee_name,
                        'priority': priority,
                        'action': action,
                        'description': description,
                        'timeline': timeline,
                        'owner': owner,
                        'estimated_cost': estimated_cost,
                        'success_probability': f"{success_probability}%",
                        'status': 'Planned',
                        'notes': notes,
                        'created_date': datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.interventions.append(new_intervention)
                    st.success(f"✅ Intervention created for {employee_name}!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (Action and Description)")

# ANALYTICS & INSIGHTS PAGE
elif page == "📈 Analytics & Insights":
    st.markdown("<h1>📈 Analytics & Insights</h1>", unsafe_allow_html=True)
    st.markdown("### Deep-dive analytics and predictive insights")
    st.markdown("---")
    
    # Calculate risk data
    risk_data = []
    for emp in st.session_state.employees:
        risk_score, risk_factors, confidence = calculate_attrition_risk(emp)
        risk_level, risk_class, color = get_risk_level(risk_score)
        risk_data.append({
            'employee': emp,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_class': risk_class,
            'risk_factors': risk_factors
        })
    
    # Risk vs. Performance Matrix
    st.markdown("### 🎯 Risk vs. Performance Matrix")
    st.markdown("Identify high-performing flight risks and low-performing employees")
    
    fig_matrix = go.Figure()
    
    for item in risk_data:
        emp = item['employee']
        risk_level = item['risk_level']
        colors = {'Critical': '#2C3E50', 'High': '#566573', 'Medium': '#7F8C8D', 'Low': '#95A5A6'}
        
        fig_matrix.add_trace(go.Scatter(
            x=[emp.get('performance_score', 3.5)],
            y=[item['risk_score']],
            mode='markers+text',
            name=risk_level,
            marker=dict(size=20, color=colors[risk_level], line=dict(width=2, color='white')),
            text=emp['name'].split()[0],
            textposition='top center',
            textfont=dict(size=10, color='#2C3E50', family='Inter'),
            hovertemplate=f"<b>{emp['name']}</b><br>Performance: {emp.get('performance_score', 'N/A')}<br>Risk Score: {item['risk_score']}<br>Department: {emp['department']}<extra></extra>",
            showlegend=False
        ))
    
    fig_matrix.update_layout(
        height=500,
        xaxis_title="Performance Score",
        yaxis_title="Attrition Risk Score",
        xaxis=dict(range=[0, 5], showgrid=True, gridcolor='#E9ECEF'),
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor='#E9ECEF'),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#2C3E50'),
        shapes=[
            dict(type='line', x0=3.5, x1=3.5, y0=0, y1=100, line=dict(color='#BDC3C7', width=2, dash='dash')),
            dict(type='line', x0=0, x1=5, y0=50, y1=50, line=dict(color='#BDC3C7', width=2, dash='dash'))
        ],
        annotations=[
            dict(x=4.5, y=90, text="High Performer<br>Flight Risk", showarrow=False, font=dict(size=12, color='#2C3E50', family='Inter')),
            dict(x=1.5, y=90, text="Underperformer<br>High Risk", showarrow=False, font=dict(size=12, color='#2C3E50', family='Inter')),
            dict(x=4.5, y=10, text="High Performer<br>Low Risk", showarrow=False, font=dict(size=12, color='#27AE60', family='Inter')),
            dict(x=1.5, y=10, text="Underperformer<br>Low Risk", showarrow=False, font=dict(size=12, color='#95A5A6', family='Inter'))
        ]
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Trend Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Risk Factor Frequency")
        
        # Count all risk factors
        all_factors = []
        for item in risk_data:
            for factor, severity in item['risk_factors']:
                if severity != 'Positive':
                    all_factors.append(factor.split(':')[0] if ':' in factor else factor[:40])
        
        factor_counts = Counter(all_factors).most_common(8)
        
        if factor_counts:
            fig_factors = go.Figure(data=[go.Bar(
                x=[count for _, count in factor_counts],
                y=[factor for factor, _ in factor_counts],
                orientation='h',
                marker=dict(
                    color=[count for _, count in factor_counts],
                    colorscale=[[0, '#95A5A6'], [1, '#2C3E50']],
                    showscale=False
                ),
                text=[count for _, count in factor_counts],
                textposition='outside',
                textfont=dict(size=14, color='#2C3E50', family='Inter', weight='bold')
            )])
            
            fig_factors.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
                yaxis=dict(showgrid=False),
                plot_bgcolor='white',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=11, color='#2C3E50')
            )
            
            st.plotly_chart(fig_factors, use_container_width=True)
        else:
            st.info("No risk factors to display")
    
    with col2:
        st.markdown("### 💰 Salary Distribution by Risk Level")
        
        risk_salary = {level: [] for level in ['Critical', 'High', 'Medium', 'Low']}
        for item in risk_data:
            risk_salary[item['risk_level']].append(item['employee'].get('salary_percentile', 50))
        
        fig_salary = go.Figure()
        
        colors = {'Critical': '#2C3E50', 'High': '#566573', 'Medium': '#7F8C8D', 'Low': '#95A5A6'}
        for level in ['Critical', 'High', 'Medium', 'Low']:
            if risk_salary[level]:
                fig_salary.add_trace(go.Box(
                    y=risk_salary[level],
                    name=level,
                    marker_color=colors[level],
                    boxmean='sd'
                ))
        
        fig_salary.update_layout(
            height=400,
            yaxis_title="Salary Percentile",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=12, color='#2C3E50'),
            yaxis=dict(range=[0, 100], showgrid=True, gridcolor='#E9ECEF')
        )
        
        st.plotly_chart(fig_salary, use_container_width=True)
    
    # Engagement vs Tenure
    st.markdown("### 📉 Engagement Trends by Tenure")
    
    fig_engagement = go.Figure()
    
    tenure_buckets = {'0-12 mo': [], '12-24 mo': [], '24-36 mo': [], '36+ mo': []}
    for item in risk_data:
        emp = item['employee']
        tenure = emp.get('tenure_months', 12)
        engagement = emp.get('engagement_score', 3.5)
        
        if tenure < 12:
            tenure_buckets['0-12 mo'].append(engagement)
        elif tenure < 24:
            tenure_buckets['12-24 mo'].append(engagement)
        elif tenure < 36:
            tenure_buckets['24-36 mo'].append(engagement)
        else:
            tenure_buckets['36+ mo'].append(engagement)
    
    avg_engagement = {k: (sum(v)/len(v) if v else 0) for k, v in tenure_buckets.items()}
    
    fig_engagement.add_trace(go.Bar(
        x=list(avg_engagement.keys()),
        y=list(avg_engagement.values()),
        marker=dict(
            color=list(avg_engagement.values()),
            colorscale=[[0, '#E74C3C'], [0.5, '#F39C12'], [1, '#27AE60']],
            showscale=False
        ),
        text=[f"{v:.2f}" for v in avg_engagement.values()],
        textposition='outside',
        textfont=dict(size=16, color='#2C3E50', family='Inter', weight='bold')
    ))
    
    fig_engagement.update_layout(
        height=400,
        yaxis_title="Average Engagement Score",
        xaxis_title="Tenure Range",
        yaxis=dict(range=[0, 5], showgrid=True, gridcolor='#E9ECEF'),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#2C3E50')
    )
    
    st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Key Insights
    st.markdown("### 💡 Strategic Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_perf_flight_risk = len([r for r in risk_data if r['employee'].get('performance_score', 0) >= 4.2 and r['risk_score'] >= 55])
        st.markdown(f"""
        <div class="insight-box">
            <div style="font-size: 3rem; font-weight: 900; color: #E74C3C; text-align: center;">{high_perf_flight_risk}</div>
            <div style="text-align: center; color: #2C3E50; font-weight: 700; margin-top: 8px;">High Performers at Risk</div>
            <p style="color: #7F8C8D; font-size: 13px; text-align: center; margin-top: 8px;">Immediate retention action needed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        critical_employees = [r for r in risk_data if r['risk_level'] == 'Critical']
        avg_salary_critical = sum(r['employee'].get('salary_percentile', 50) for r in critical_employees) / max(1, len(critical_employees))
        st.markdown(f"""
        <div class="insight-box">
            <div style="font-size: 3rem; font-weight: 900; color: #F39C12; text-align: center;">{avg_salary_critical:.0f}%</div>
            <div style="text-align: center; color: #2C3E50; font-weight: 700; margin-top: 8px;">Avg Salary (Critical Risk)</div>
            <p style="color: #7F8C8D; font-size: 13px; text-align: center; margin-top: 8px;">Compensation review recommended</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        no_promotion_24mo = len([r for r in risk_data if r['employee'].get('last_promotion_months', 0) > 24])
        st.markdown(f"""
        <div class="insight-box">
            <div style="font-size: 3rem; font-weight: 900; color: #3498DB; text-align: center;">{no_promotion_24mo}</div>
            <div style="text-align: center; color: #2C3E50; font-weight: 700; margin-top: 8px;">Overdue for Promotion</div>
            <p style="color: #7F8C8D; font-size: 13px; text-align: center; margin-top: 8px;">Career development focus area</p>
        </div>
        """, unsafe_allow_html=True)

# EXIT INTELLIGENCE PAGE
elif page == "💬 Exit Intelligence":
    st.markdown("<h1>💬 Exit Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("### Learn from departures and prevent future attrition")
    st.markdown("---")
    
    if st.session_state.exit_interviews:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_exits = len(st.session_state.exit_interviews)
        avg_tenure = sum(e.get('tenure_months', 0) for e in st.session_state.exit_interviews) / total_exits
        would_recommend = sum(1 for e in st.session_state.exit_interviews if e.get('would_recommend', False))
        avg_satisfaction = sum(e.get('satisfaction_score', 3.0) for e in st.session_state.exit_interviews) / total_exits
        
        with col1:
            st.metric("Total Exits", total_exits)
        with col2:
            st.metric("Avg Tenure", f"{avg_tenure:.0f} mo")
        with col3:
            st.metric("Would Recommend", f"{(would_recommend/total_exits*100):.0f}%")
        with col4:
            st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Reason analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Primary Exit Reasons")
            
            reasons = Counter([e.get('reason_primary', 'Unknown') for e in st.session_state.exit_interviews])
            
            fig_reasons = go.Figure(data=[go.Pie(
                labels=list(reasons.keys()),
                values=list(reasons.values()),
                hole=0.4,
                marker=dict(colors=['#2C3E50', '#566573', '#7F8C8D', '#95A5A6', '#BDC3C7']),
                textfont=dict(size=14, color='white', family='Inter'),
                textinfo='label+percent'
            )])
            
            fig_reasons.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=True,
                legend=dict(orientation="v", x=1.1, y=0.5),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=12, color='#2C3E50')
            )
            
            st.plotly_chart(fig_reasons, use_container_width=True)
        
        with col2:
            st.markdown("### 🏢 Exits by Department")
            
            dept_exits = Counter([e.get('department', 'Unknown') for e in st.session_state.exit_interviews])
            
            fig_dept = go.Figure(data=[go.Bar(
                x=list(dept_exits.keys()),
                y=list(dept_exits.values()),
                marker=dict(
                    color=list(dept_exits.values()),
                    colorscale=[[0, '#95A5A6'], [1, '#2C3E50']],
                    showscale=False
                ),
                text=list(dept_exits.values()),
                textposition='outside',
                textfont=dict(size=16, color='#2C3E50', family='Inter', weight='bold')
            )])
            
            fig_dept.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
                plot_bgcolor='white',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=12, color='#2C3E50')
            )
            
            st.plotly_chart(fig_dept, use_container_width=True)
        
        # Exit interview details
        st.markdown("### 📋 Recent Exit Interviews")
        
        for exit_int in sorted(st.session_state.exit_interviews, key=lambda x: x.get('date', '2000-01-01'), reverse=True):
            with st.expander(f"**{exit_int.get('employee', 'Unknown')}** - {exit_int.get('department', 'Unknown')} ({exit_int.get('date', 'N/A')})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 12px;">
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                            <div>
                                <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">PRIMARY REASON</div>
                                <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{exit_int.get('reason_primary', 'N/A')}</div>
                            </div>
                            <div>
                                <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">SECONDARY REASON</div>
                                <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{exit_int.get('reason_secondary', 'N/A')}</div>
                            </div>
                            <div>
                                <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">TENURE</div>
                                <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{exit_int.get('tenure_months', 0)} months</div>
                            </div>
                            <div>
                                <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 6px;">WOULD RECOMMEND</div>
                                <div style="color: #2C3E50; font-size: 16px; font-weight: 600;">{"✅ Yes" if exit_int.get('would_recommend', False) else "❌ No"}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 12px; text-align: center;">
                        <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">MANAGER RATING</div>
                        <div style="color: #2C3E50; font-size: 3rem; font-weight: 900;">{exit_int.get('manager_rating', 'N/A')}</div>
                        <div style="color: #95A5A6; font-size: 13px;">out of 5</div>
                        <hr style="margin: 16px 0; border: none; border-top: 2px solid #E9ECEF;">
                        <div style="color: #7F8C8D; font-size: 11px; font-weight: 700; margin-bottom: 8px;">SATISFACTION</div>
                        <div style="color: #2C3E50; font-size: 2rem; font-weight: 700;">{exit_int.get('satisfaction_score', 'N/A')}/5</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Actionable insights
        st.markdown("### 💡 Key Takeaways")
        
        most_common_reason = reasons.most_common(1)[0] if reasons else ('Unknown', 0)
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #2C3E50; margin-top: 0;">Primary Focus Area: {most_common_reason[0]}</h4>
            <p style="color: #34495E; line-height: 1.6;">
                {most_common_reason[1]} out of {total_exits} recent departures cited <strong>{most_common_reason[0]}</strong> as their primary reason for leaving.
                This represents {(most_common_reason[1]/total_exits*100):.0f}% of exits and should be a strategic priority for retention efforts.
            </p>
            <ul style="color: #34495E; line-height: 1.8; margin-top: 12px;">
                <li>Review and benchmark compensation packages quarterly</li>
                <li>Establish clear career progression frameworks</li>
                <li>Increase manager effectiveness training</li>
                <li>Implement regular work-life balance assessments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("No exit interview data available yet. Exit interviews will appear here as they are conducted.")

# ADD EMPLOYEE PAGE
elif page == "➕ Add Employee":
    st.markdown("<h1>➕ Add New Employee</h1>", unsafe_allow_html=True)
    st.markdown("### Add a new employee to the tracking system")
    st.markdown("---")
    
    with st.form("add_employee_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="e.g., Jane Smith")
            department = st.selectbox("Department*", ["Engineering", "Sales", "Marketing", "Product", "Data Science", "HR", "Finance", "Operations"])
            role = st.text_input("Job Title*", placeholder="e.g., Senior Software Engineer")
        
        with col2:
            tenure_months = st.number_input("Tenure (months)*", min_value=0, max_value=600, value=12)
            last_promotion_months = st.number_input("Months Since Last Promotion*", min_value=0, max_value=120, value=18)
            salary_percentile = st.slider("Salary Percentile*", 0, 100, 50, help="Where they fall in market compensation")
        
        st.markdown("---")
        st.markdown("### Performance & Engagement")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            performance_score = st.slider("Performance Score*", 1.0, 5.0, 3.5, 0.1)
            engagement_score = st.slider("Engagement Score*", 1.0, 5.0, 3.5, 0.1)
        
        with col2:
            peer_review_score = st.slider("Peer Review Score*", 1.0, 5.0, 3.5, 0.1)
            manager_1on1_frequency = st.number_input("1-on-1 Meetings/Month*", min_value=0, max_value=20, value=2)
        
        with col3:
            training_hours = st.number_input("Training Hours (Last 6mo)*", min_value=0, max_value=200, value=10)
            certifications = st.number_input("Certifications*", min_value=0, max_value=20, value=1)
        
        st.markdown("---")
        st.markdown("### Work Patterns & History")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            recent_absences = st.number_input("Recent Absences (Last 3mo)*", min_value=0, max_value=50, value=2)
            overtime_hours = st.number_input("Overtime Hours (Last month)*", min_value=0, max_value=200, value=10)
        
        with col2:
            team_changes = st.number_input("Team Changes*", min_value=0, max_value=10, value=0)
            manager_changes = st.number_input("Manager Changes*", min_value=0, max_value=10, value=0)
        
        with col3:
            projects_completed = st.number_input("Projects Completed*", min_value=0, max_value=200, value=10)
            mentorship_hours = st.number_input("Mentorship Hours (Last 6mo)*", min_value=0, max_value=100, value=0)
        
        feedback_received = st.number_input("Feedback Sessions Received (Last 6mo)*", min_value=0, max_value=50, value=4)
        
        st.markdown("---")
        submitted = st.form_submit_button("Add Employee")
        
        if submitted:
            if name and department and role:
                new_employee = {
                    'id': max([emp['id'] for emp in st.session_state.employees]) + 1 if st.session_state.employees else 1,
                    'name': name,
                    'department': department,
                    'role': role,
                    'tenure_months': tenure_months,
                    'performance_score': performance_score,
                    'engagement_score': engagement_score,
                    'last_promotion_months': last_promotion_months,
                    'salary_percentile': salary_percentile,
                    'manager_1on1_frequency': manager_1on1_frequency,
                    'recent_absences': recent_absences,
                    'peer_review_score': peer_review_score,
                    'training_hours': training_hours,
                    'overtime_hours': overtime_hours,
                    'team_changes': team_changes,
                    'manager_changes': manager_changes,
                    'projects_completed': projects_completed,
                    'certifications': certifications,
                    'mentorship_hours': mentorship_hours,
                    'feedback_received': feedback_received
                }
                
                st.session_state.employees.append(new_employee)
                
                # Calculate risk for the new employee
                risk_score, risk_factors, confidence = calculate_attrition_risk(new_employee)
                risk_level, risk_class, color = get_risk_level(risk_score)
                
                st.success(f"✅ {name} has been added successfully!")
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #2C3E50; margin-top: 0;">Initial Risk Assessment</h3>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px;">
                        <div>
                            <span class="badge badge-{risk_class}">{risk_level} RISK</span>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 3rem; font-weight: 900; color: {color};">{risk_score}</div>
                            <div style="color: #95A5A6; font-size: 13px;">Risk Score</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.error("Please fill in all required fields marked with *")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #95A5A6; font-size: 12px; padding: 20px;">
    <strong>RetentionIQ Pro</strong> - Attrition Intelligence Platform<br>
    Powered by Advanced Predictive Analytics | © 2025
</div>
""", unsafe_allow_html=True)