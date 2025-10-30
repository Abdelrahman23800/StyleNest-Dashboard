# sales_dashboard_pro.py
# Client-ready Sales Performance Dashboard — E-commerce Growth Theme
# Features: polished KPI cards, Sales Rep effectiveness, Channel/Campaign funnel, Time-of-day analysis,
# downloadable PDF executive summary, professional layout and recommendations.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="E-commerce Growth Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling (E-commerce Growth Theme) ----------
STYLE = """
<style>
/* page background */
[data-testid="stAppViewContainer"] {background: linear-gradient(180deg, #fff 0%, #f7fbff 100%);}
h1 {color:#0b3b5c;}
h2 {color:#0b3b5c;}
.stButton>button {background-color:#ff6b6b; color:white; border-radius:8px;}
.css-1aumxhk {padding-top:0.5rem;} /* small spacing fix */
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ---------- Helpers ----------
@st.cache_data
def load_data(uploaded):
    if uploaded is None:
        return None
    try:
        if str(uploaded).lower().endswith(('.xls','.xlsx')):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None
    df.columns = [c.strip() for c in df.columns]
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

def safe_sum(series):
    try:
        return float(series.astype(float).sum())
    except:
        return 0.0

def compute_metrics(df):
    rev = safe_sum(df['Revenue']) if 'Revenue' in df.columns else 0.0
    conversions = safe_sum(df['Conversions']) if 'Conversions' in df.columns else 0.0
    # Orders: use conversions if present, else count rows
    orders = conversions if conversions > 0 else len(df)
    aov = (rev / orders) if orders > 0 else (df['Average Order Size'].mean() if 'Average Order Size' in df.columns else 0.0)
    conv_rate = (conversions / len(df)) if (len(df) > 0 and 'Conversions' in df.columns) else np.nan
    return {'revenue':rev, 'orders':orders, 'aov':aov, 'conv_rate':conv_rate, 'rows':len(df)}

def make_recommendations(df):
    recs = []
    # channel-level insight
    if 'Channel' in df.columns and 'Revenue' in df.columns:
        ch = df.groupby('Channel').agg(Revenue=('Revenue','sum'),
                                       Conversions=('Conversions','sum') if 'Conversions' in df.columns else ('Revenue','count'),
                                       AOV=('Average Order Size','mean') if 'Average Order Size' in df.columns else ('Revenue','mean')).reset_index()
        ch['Rev_per_Conv'] = ch['Revenue'] / ch['Conversions'].replace(0, np.nan)
        best = ch.sort_values('Rev_per_Conv', ascending=False).iloc[0]
        worst = ch.sort_values('Rev_per_Conv').iloc[0]
        recs.append(f"Focus investment on {best['Channel']} - highest revenue per conversion (~{best['Rev_per_Conv']:.2f}).")
        recs.append(f"Review or optimize {worst['Channel']} - low revenue efficiency (~{worst['Rev_per_Conv']:.2f}).")
    # time of day insight
    if 'Time of Day' in df.columns and 'Revenue' in df.columns:
        tod = df.groupby('Time of Day')['Revenue'].sum().sort_values(ascending=False)
        top_tod = tod.index[0]
        recs.append(f"Peak selling window: {top_tod}. Schedule paid promotions or flash deals in this window.")
    # Sales rep coaching
    if 'Sales Rep' in df.columns and 'Revenue' in df.columns:
        rep = df.groupby('Sales Rep').agg(Revenue=('Revenue','sum'), Conversions=('Conversions','sum') if 'Conversions' in df.columns else ('Revenue','count')).reset_index()
        low = rep[rep['Revenue'] < rep['Revenue'].quantile(0.25)]
        if not low.empty:
            small = ', '.join(low.sort_values('Revenue').head(3)['Sales Rep'].tolist())
            recs.append(f"Consider targeted coaching for lower performers: {small}.")
    # Inventory/returns reminder (polished)
    if not any(c.lower() in ['stock','inventory','return','returns','return_flag','return_quantity'] for c in df.columns):
        recs.append("Inventory & Returns data not present. For full campaign ROI and stock risk analysis, include product-stock & returns fields.")
    return recs

def create_pdf_report(metrics, top_channels, top_reps, recs, meta):
    """Simplified PDF generation with minimal formatting"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Executive Summary", ln=True, align="C")
    pdf.ln(5)
    
    # Date
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, datetime.utcnow().strftime('%Y-%m-%d'), ln=True)
    pdf.ln(5)
    
    # KPIs
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Key Metrics", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f"Revenue: ${metrics['revenue']:,.0f}", ln=True)
    pdf.cell(0, 5, f"Orders: {int(metrics['orders']):,}", ln=True)
    pdf.cell(0, 5, f"Avg Order: ${metrics['aov']:,.0f}", ln=True)
    conv = f"{metrics['conv_rate']*100:.1f}%" if not np.isnan(metrics['conv_rate']) else "N/A"
    pdf.cell(0, 5, f"Conv Rate: {conv}", ln=True)
    pdf.ln(5)
    
    # Top Channels
    if len(top_channels) > 0:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 7, "Top Channels", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for idx, row in top_channels.head(5).iterrows():
            try:
                ch = str(row['Channel'])[:40]  # Truncate long names
                rev = float(row['Revenue'])
                pdf.cell(0, 5, f"{ch}: ${rev:,.0f}", ln=True)
            except:
                pass
        pdf.ln(5)
    
    # Top Reps
    if len(top_reps) > 0:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 7, "Top Sales Reps", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for idx, row in top_reps.head(5).iterrows():
            try:
                rep = str(row['Sales Rep'])[:40]  # Truncate long names
                rev = float(row['Revenue'])
                pdf.cell(0, 5, f"{rep}: ${rev:,.0f}", ln=True)
            except:
                pass
        pdf.ln(5)
    
    # Recommendations
    if len(recs) > 0:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 7, "Recommendations", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for i, r in enumerate(recs[:5], 1):  # Limit to 5
            try:
                # Clean text: remove special chars and truncate
                clean = str(r).encode('ascii', 'ignore').decode('ascii')[:100]
                pdf.cell(0, 5, f"{i}. {clean}", ln=True)
            except:
                pass
    
    return pdf.output(dest='S')

# ---------- UI ----------
st.title("StyleNest Boutique — Sales Dashboard")
st.markdown("Professional dashboard focused on growth: funnel efficiency, channel ROI, and action-oriented recommendations.")

# Sidebar: upload & filters
st.sidebar.markdown("## Data")
uploaded = st.sidebar.file_uploader("Upload sales file (XLSX / CSV)", type=['xlsx','xls','csv'])
df = load_data(uploaded)
if df is None:
    st.sidebar.info("Upload your sales file to run the dashboard. Expected columns (if present): Date, Time of Day, Channel, Revenue, Average Order Size, Conversions, Customer Type, Sales Rep, Business.")
    st.stop()

# Filters
st.sidebar.markdown("## Filters")
if 'Date' in df.columns:
    lo, hi = df['Date'].min().date(), df['Date'].max().date()
    dr = st.sidebar.date_input("Date range", value=[lo, hi], min_value=lo, max_value=hi)
    if len(dr) == 2:
        df = df[(df['Date'] >= pd.to_datetime(dr[0])) & (df['Date'] <= pd.to_datetime(dr[1]))]
channels = df['Channel'].unique().tolist() if 'Channel' in df.columns else []
sel_channels = st.sidebar.multiselect("Channel", options=channels, default=channels)
if sel_channels:
    df = df[df['Channel'].isin(sel_channels)]
cust_types = df['Customer Type'].unique().tolist() if 'Customer Type' in df.columns else []
sel_cust = st.sidebar.multiselect("Customer Type", options=cust_types, default=cust_types)
if sel_cust:
    df = df[df['Customer Type'].isin(sel_cust)]
# Business (branch)
if 'Business' in df.columns:
    bizs = df['Business'].unique().tolist()
    sel_biz = st.sidebar.multiselect("Business / Branch", options=bizs, default=bizs)
    if sel_biz:
        df = df[df['Business'].isin(sel_biz)]

# Compute metrics
metrics = compute_metrics(df)

# KPI Cards (top row)
col1, col2, col3, col4 = st.columns([1.7,1,1,1])
with col1:
    st.metric("Total Revenue", f"${metrics['revenue']:,.2f}")
with col2:
    st.metric("Total Orders (est.)", f"{int(metrics['orders']):,}")
with col3:
    st.metric("Average Order Value", f"${metrics['aov']:,.2f}")
with col4:
    conv_display = f"{metrics['conv_rate']*100:.2f}%" if not np.isnan(metrics['conv_rate']) else "N/A"
    st.metric("Conversion Rate", conv_display)

st.markdown("---")

# Funnel / Channel Efficiency (marketing focus)
st.subheader("Channel Funnel & Efficiency")
if 'Channel' in df.columns:
    chan = df.groupby('Channel').agg(Revenue=('Revenue','sum'),
                                     Conversions=('Conversions','sum') if 'Conversions' in df.columns else ('Revenue','count'),
                                     Avg_Order=('Average Order Size','mean') if 'Average Order Size' in df.columns else ('Revenue','mean')).reset_index()
    chan['Revenue_per_Conv'] = chan['Revenue'] / chan['Conversions'].replace(0, np.nan)
    chan = chan.sort_values('Revenue', ascending=False)
    fig_chan = px.bar(chan, x='Channel', y='Revenue', hover_data=['Conversions','Revenue_per_Conv'], title='Revenue by Channel (hover for conversions & efficiency)')
    st.plotly_chart(fig_chan, use_container_width=True)
    st.dataframe(chan.round(2))
else:
    st.info("Channel data not available.")

st.markdown("---")

# Time-of-day & Trend
left, right = st.columns([2,1])
with left:
    st.subheader("Revenue Trend (weekly)")
    if 'Date' in df.columns:
        df_week = df.set_index('Date').resample('W')['Revenue'].sum().reset_index()
        fig_time = px.line(df_week, x='Date', y='Revenue', title='Weekly Revenue Trend', markers=True)
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("Date column not present.")

with right:
    st.subheader("Revenue by Time of Day")
    if 'Time of Day' in df.columns:
        tod = df.groupby('Time of Day')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
        fig_tod = px.pie(tod, names='Time of Day', values='Revenue', title='Revenue by Time of Day', hole=0.4)
        st.plotly_chart(fig_tod, use_container_width=True)
    else:
        st.info("Time of Day column not present.")

st.markdown("---")

# Sales Rep section (detailed)
st.subheader("Sales Rep Performance")
if 'Sales Rep' in df.columns and 'Revenue' in df.columns:
    rep = df.groupby('Sales Rep').agg(Revenue=('Revenue','sum'),
                                      Conversions=('Conversions','sum') if 'Conversions' in df.columns else ('Revenue','count'),
                                      Avg_Order=('Average Order Size','mean') if 'Average Order Size' in df.columns else ('Revenue','mean')).reset_index()
    rep['Revenue_per_Conv'] = rep['Revenue'] / rep['Conversions'].replace(0, np.nan)
    rep = rep.sort_values('Revenue', ascending=False)
    st.dataframe(rep.rename(columns={'Avg_Order':'Avg Order Size','Revenue_per_Conv':'Revenue per Conv'}).round(2).head(50))
    fig_rep = px.bar(rep.head(10), x='Sales Rep', y='Revenue', title='Top 10 Sales Reps by Revenue', text='Revenue')
    st.plotly_chart(fig_rep, use_container_width=True)
else:
    st.info("Sales Rep analysis requires Sales Rep & Revenue columns.")

st.markdown("---")

# Customer segmentation
st.subheader("Customer Segmentation")
if 'Customer Type' in df.columns:
    cust = df.groupby('Customer Type').agg(Revenue=('Revenue','sum'), Conversions=('Conversions','sum') if 'Conversions' in df.columns else ('Revenue','count')).reset_index()
    fig_cust = px.bar(cust, x='Customer Type', y='Revenue', title='Revenue by Customer Type', text='Revenue')
    st.plotly_chart(fig_cust, use_container_width=True)
    st.dataframe(cust.round(2))
else:
    st.info("Customer Type column not present.")

st.markdown("---")

# Inventory & Returns professional note (non-distracting)
st.subheader("Inventory & Returns (Recommended Integration)")
st.markdown("To complete campaign ROI and stock risk analysis, integrate:\n- `Product_ID`, `Stock_Quantity`, `Return_Flag`/`Return_Quantity`, `Return_Reason`.\nOnce added, the dashboard will show low-stock alerts, return % by product, and root-cause charts.")

st.markdown("---")

# Recommendations & PDF export
st.subheader("Executive Recommendations")
recs = make_recommendations(df)
for r in recs:
    st.write("•", r)

# Prepare tables for PDF
top_channels = df.groupby('Channel').agg(Revenue=('Revenue','sum')).reset_index().sort_values('Revenue', ascending=False) if 'Channel' in df.columns else pd.DataFrame(columns=['Channel','Revenue'])
top_reps = df.groupby('Sales Rep').agg(Revenue=('Revenue','sum')).reset_index().sort_values('Revenue', ascending=False) if 'Sales Rep' in df.columns else pd.DataFrame(columns=['Sales Rep','Revenue'])
meta = f"Rows: {len(df)} | Period: {df['Date'].min().date() if 'Date' in df.columns else 'N/A'} to {df['Date'].max().date() if 'Date' in df.columns else 'N/A'}"

# Alternative: Download as Text Report (more reliable than PDF)
def create_text_report(metrics, top_channels, top_reps, recs, meta):
    report = []
    report.append("=" * 70)
    report.append("E-COMMERCE GROWTH DASHBOARD - EXECUTIVE SUMMARY")
    report.append("=" * 70)
    report.append(f"\nGenerated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
    
    # KPIs
    report.append("\nKEY PERFORMANCE INDICATORS")
    report.append("-" * 70)
    report.append(f"Total Revenue:        ${metrics['revenue']:,.2f}")
    report.append(f"Total Orders (est):   {int(metrics['orders']):,}")
    report.append(f"Average Order Value:  ${metrics['aov']:,.2f}")
    conv_text = f"{metrics['conv_rate']*100:.2f}%" if not np.isnan(metrics['conv_rate']) else "N/A"
    report.append(f"Conversion Rate:      {conv_text}")
    
    # Top Channels
    if not top_channels.empty:
        report.append("\n\nTOP CHANNELS BY REVENUE")
        report.append("-" * 70)
        for idx, row in top_channels.head(5).iterrows():
            report.append(f"  - {row['Channel']}: ${row['Revenue']:,.2f}")
    
    # Top Reps
    if not top_reps.empty:
        report.append("\n\nTOP SALES REPRESENTATIVES")
        report.append("-" * 70)
        for idx, row in top_reps.head(5).iterrows():
            report.append(f"  - {row['Sales Rep']}: ${row['Revenue']:,.2f}")
    
    # Recommendations
    if recs:
        report.append("\n\nEXECUTIVE RECOMMENDATIONS")
        report.append("-" * 70)
        for i, r in enumerate(recs, 1):
            report.append(f"{i}. {r}")
    
    report.append(f"\n\n{'-' * 70}")
    report.append(f"Data Source: {meta}")
    report.append("=" * 70)
    
    return "\n".join(report)

# Create text report
text_report = create_text_report(metrics, top_channels, top_reps, recs, meta)

col_a, col_b = st.columns(2)
with col_a:
    st.download_button(
        label="📄 Download Text Report (.txt)",
        data=text_report,
        file_name="executive_summary.txt",
        mime="text/plain",
        type="primary"
    )

with col_b:
    # Try PDF generation but don't break if it fails
    try:
        pdf_bytes = create_pdf_report(metrics, top_channels, top_reps, recs, meta)
        st.download_button(
            label="📥 Download PDF Report (Beta)",
            data=BytesIO(pdf_bytes),
            file_name="executive_summary.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.button("📥 PDF Unavailable", disabled=True, help=f"Error: {str(e)}")
