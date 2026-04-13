# -*- coding: utf-8 -*-
"""
Venezuela Economic Dashboard
Interactive dashboard built with Streamlit + Plotly
Data: World Bank WDI, IMF, WEO, OPEC/IEA
Author: Vilma Windevoxchel | github.com/VWinde
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

#------- Page config -----------
st.set_page_config(
    page_title="Venezuela Economic Dashboard",
    page_icon="ve",
    layout="wide",
    initial_sidebar_state="expanded",
    )

#------- Custom CSS -----------
st.markdown(""" 
            <style>
            .main{background-color: #F8F9FA;}
                 .metric-card{
                      background: white;
                      border-radius: 10px;
                      padding: 16px 20px;
                      box-shadow: 0 2px 8px rgba(0, 0, 0,0.08);
                      border-left: 4px solid #1A3A5C;
                      }
                  .metric-value {font-size: 29px; font-weight: 700; color: #1A3A5C;}
                                 .metric-label{font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }
                                               .metric-delta-pos{font-size: 13px; color: #27AE60;}
                                                                 .metric-delta-neg{font-size: 13px; color=#C0392B;}
                                                                                   .insight-box{
                                                                                       background: #EBF5FB;
                                                                                       border-left: 4px solid #2E86AB;
                                                                                       border-radius: 6px;
                                                                                       padding: 12px 16px;
                                                                                       margin: 8px 0;
                                                                                       font-size: 14px;
                                                                                       }
                                                                                   .warning-box{
                                                                                       background: #FEF9E7;
                                                                                       border-left: 4px solid #E8A838;
                                                                                       border-radius: 6px;
                                                                                       padding: 12px 6px;
                                                                                       margin: 8px 0;
                                                                                       font-size: 14px;
                                                                                       }
                                                                                   h1{color: #1A3A5C !important;}
                                                                                      h2{color: #1A3A5C !important; font-size: 18px !important;}
                                                                                         </style>
""", unsafe_allow_html=True)

#----------- Colors ----------------------
NAVY   = "#1A3A5C"
BLUE   = "#2E86AB"
ORANGE = "#E8A838"
RED    = "#C0392B"
GREEN  = "#27AE60"
GRAY   = "#95A5A6"

#---------- Load data --------------------

@st.cache_data
def load_data():
    data = {
        'year': list(range(1990, 2025)),
        'gdp_growth': [6.5,9.7,6.1,0.3,-2.3,4.0,-0.2,6.4,0.3,-6.0,
                       3.7,3.4,-8.9,-7.8,18.3,10.3,9.9,8.8,5.3,-3.2,
                       -1.5,4.2,5.6,1.3,-3.9,-6.2,-17.0,-15.7,-19.6,-27.7,
                       -30.0,0.5,12.0,5.0,5.3],
    'inflation': [40.7,34.2,31.9,45.9,60.8,59.9,99.9,50.0,35.8,23.6,
                  16.2,12.5,22.4,31.1,21.7,16.0,13.7,18.7,30.4,27.1,
                  28.2,26.1,21.1,40.6,62.2,121.7,254.9,438.1,65374.1,19906.0,
                  2355.1,1588.5,222.3,360.0,254.9],
    'oil_rents_pct_gdp': [22.8,20.1,17.5,13.9,12.7,17.4,24.1,26.2,10.0,19.1,
                          25.3,16.2,21.8,31.1,37.6,34.1,21.2,18.1,12.2,11.8,
                          13.1,17.1,15.4,12.8,10.2,5.8,1.8,2.3,1.5,2.1,
                          1.0,2.8,4.5,5.2,4.8],
    'gdp_per_capita_usd': [4420,4789,5013,4958,4757,4917,4832,5136,5077,4738,
                           4791,4861,4396,4052,4760,5182,5590,5983,6244,5969,
                           5830,6023,6322,6369,6031,5547,4523,3734,2917,2103,
                           1451,1451,1581,1625,1680],
    'unemployment_rate': [10.4,9.5,7.8,6.6,8.7,10.2,11.8,11.4,11.3,15.0,
                               13.9,13.3,15.8,18.0,15.3,12.4,10.0,8.5,7.4,7.8,
                               8.5,8.3,7.8,7.5,7.2,7.4,21.2,26.4,34.9,44.3,
                               50.3,48.1,40.5,35.2,30.1],
    'oil_production_kbd': [2260,2500,2370,2390,2580,2730,3120,3160,3000,3100,
                                3240,3200,2890,2540,3060,3250,3200,3150,3200,2900,
                                2840,2820,2880,2780,2670,2620,2370,2030,1550,870,
                                570,600,720,780,820],
    'poverty_rate': [None,None,None,None,62.0,None,69.4,None,49.0,49.4,
                     None,48.6,48.6,55.1,53.1,37.9,30.2,28.5,27.5,24.0,
                     25.4,24.8,21.2,19.7,25.4,33.1,None,None,None,None,
                     94.5,93.3,81.5,82.8,83.0],
    'latam_gdp_growth': [0.5,3.7,2.8,3.4,4.8,0.9,3.5,5.2,2.0,0.5,
                              3.9,0.4,-0.6,2.1,6.0,4.7,5.7,5.8,4.2,-1.5,
                              5.8,4.5,2.9,2.8,1.3,0.3,-0.6,1.3,1.0,-0.1,
                              -6.8,6.9,3.9,2.1,2.2],
    }
    df= pd.DataFrame(data).set_index('year')
    return df

df=load_data()

#--------- Sidebar ---------------
with st.sidebar:
    st.markdown("## ve Venezuela Economic Dashboard")
    st.markdown("---")
    st.markdown("### Data Source")
    st.markdown("""
    - 🌐 **World Bank WDI** (primary)
    - 📊 **IMF WEO** Oct 2025
    - 🛢️ **OPEC / EIA** (oil production)
    - 🏛️ **CEPAL** (regional comparisons))
    """)
    st.markdown("---")
    st.markdown("### Year Range")
    year_range=st.slider("Select period", 1990, 2024,(1990,2024))
    df_filtered= df.loc[year_range[0]: year_range[1]]
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
                Built by **Vilma Windevoxchel**
                Data Analyst & BI Specialist
                [LinkedIn](https://www.linkedin.com/in/vilma-windevoxchel/)· [Github](https://github.com/VWinde)
                """)
                
#---------- Header ---------------------
st.markdown("# ve Venezuela Economic Indicators Dashboard")
st.markdown(f"**Period shown:** {year_range[0]} - {year_range[1]} · Data: World Bank WDI, IMF WEO 2025")
st.markdown("---")

#---------- KPI Cards ------------------

st.markdown("### 📌 Key Indicators - Latest Available Data (2024)")
col1, col2, col3, col4, col5= st.columns(5)

latest=df.loc[2024]
prev=df.loc[2023]

with col1:
    delta= latest['gdp_growth']-prev['gdp_growth']
    st.metric("GDP Growth", f"{latest['gdp_growth']:.1f}%",
              f"{delta:+.1f}pp vs 2023")
    
with col2:
    st.metric("Inflation (CPI)", f"{latest['inflation']:.1f}%",
              f"{latest['inflation']-prev['inflation']:+.1f}pp vs 2023",
              delta_color="inverse")

with col3:
    st.metric("Unemployment", f"{latest['unemployment_rate']:.1f}%",
              f"{latest['unemployment_rate'] - prev['unemployment_rate']:+.1f}pp vs 2023",
             delta_color="inverse")
    
with col4:
    st.metric("Oil Production", f"{latest['oil_production_kbd']:,.0f} kbd",
              f"{latest['oil_production_kbd']-prev['oil_production_kbd']:+.0f} kbd vs 2023")

with col5:
    st.metric("GDP per Capita", f"${latest['gdp_per_capita_usd']:,.0f}",
              f"${latest['gdp_per_capita_usd']-prev['gdp_per_capita_usd']:+.0f} vs 2023")
    
st.markdown("---")

#---------- Key Insights ----------------
st.markdown("### 💡 Key Insights")
col_a, col_b, col_c =st.columns(3)

with col_a:
    peak_gdp= df['gdp_per_capita_usd'].max()
    decline= (peak_gdp-latest['gdp_per_capita_usd'])/peak_gdp *100
    st.markdown(f"""
                <div class="insight-box">
                <b> Economic Contraction </b><br>
                GDP per capita collapsed <b>{decline: .0f}%</b> from its 2013 peak of
                <b>${peak_gdp:,.0f}</b> to <b>${latest['gdp_per_capita_usd']:,.0f}</b> in 2024 -
                one of the largest contractions in Latin American history outside war contexts.
    </div>
    """, unsafe_allow_html=True)
    
with col_b:
    st.markdown(f"""
                <div class="warning-box">
                <b>🔥 Hyperinflation Legacy</b><br>
                Venezuela reached <b>65,374%</b> inflation in 2018 - among the most severe
                hyperinflationary episodes globally since WWII. Despite declining to
                <b>{latest['inflation']:.0f}% in 2024, inflation remains critically high.
                </div>
                """, unsafe_allow_html=True)
                
with col_c:
    oil_peak= df['oil_production_kbd'].max()
    oil_decline = (oil_peak - latest['oil_production_kbd'])/oil_peak*100
    st.markdown(f"""
                <div class = "insight-box">
                <b>🛢️ Oil Production</b><br>
                Production fell <b>{oil_decline:.0f}%</b> from peak levels (~{oil_peak:,}kbd)
                to <b>{latest['oil_production_kbd']:,} kbd</b> - driven by PDVSA underinvestment,
                sanctions, and technical deterioration.
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")

#------------- Chart 1: GDP Growth --------------------------

st.markdown("### GDP Growth: Venezuela vs Latin America")

fig1= go.Figure()

# Recession shading
for start, end, label in [(1994, 1996, "Banking crisis"), (1999, 2003, "Chávez Period I"), (2013, 2020, "Economic Collapse"), 
                          (2020,2020, "COVID - 19")]:
    fig1.add_vrect(x0=start-0.5, x1= end+0.5, fillcolor=RED, opacity=0.8,
                   layer='below', line_width=0,
                   annotation_text= label, annotation_position="top left",
                   annotation_font_size=9, annotation_font_color=RED)
    
# Fill positive/negative areas
pos = df_filtered['gdp_growth'].copy(); pos[pos<0] =0
neg = df_filtered['gdp_growth'].copy(); neg[neg>0] =0

fig1.add_trace(go.Scatter(x=df_filtered.index, y=pos, fill='tozeroy',
    fillcolor='rgba(39,174,96,0.2)', line=dict(color='rgba(0,0,0,0)'), showlegend=False))
fig1.add_trace(go.Scatter(x=df_filtered.index, y=neg, fill='tozeroy',
    fillcolor='rgba(192,57,43,0.2)', line=dict(color='rgba(0,0,0,0)'), showlegend=False))

fig1.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['gdp_growth'],
    name="Venezuela", line=dict(color=NAVY, width=2.5),
    hovertemplate="<b>%{x}</b><br>GDP Growth: %{y:.1f}%<extra></extra>"))

latam_data=df_filtered['latam_gdp_growth'].dropna()
fig1.add_trace(go.Scatter(x=latam_data.index, y=latam_data,
                          name="Latin America avg.", line=dict(color=ORANGE, width=2, dash='dash'),
                          hovertemplate= "<b>%{x}</b><br>LatAm GDP Growth: %{y: 1.f}%<extra></extra>"))

fig1.add_hline(y=0, line_dash="dash", line_color=GRAY, line_width=1, opacity=0.6)
fig1.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
    yaxis_title="Annual GDP Growth (%)", xaxis_title="",
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'),
    hovermode='x unified')
fig1.update_xaxes(showgrid=False); fig1.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
st.plotly_chart(fig1, use_container_width=True)


#----- Chart 2: Inflation --------------------------------------
st.markdown("### 🔥 Inflation: The Hyperinflation Episode")
col_inf1, col_inf2= st.columns(2)

with col_inf1:
    fig2a= go.Figure()
    fig2a.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['inflation'],
                               fill='tozeroy', fillcolor='rgba(192,57,43,0.1)',
                               line=dict(color=RED, width=2.5), name="CPI Inflation",
                               hovertemplate="<b>%{x}</b><br>Inflation: %{y.,.0f}%<extra></extra>"))
    fig2a.add_hline(y=100, line_dash="dot", line_color=ORANGE, line_width=1.5,
                    annotation_text="100% threshold", annotation_position="right")
    fig2a.update_xaxes(showgrid=False); fig2a.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
    st.plotly_chart(fig2a, use_container_width=True)
    
with col_inf2:
    fig2b=go.Figure()
    fig2b.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['inflation'],
                               line=dict(color=RED, width=2.5), name="CPI Inflation (log)",
                               hovertemplate= "<b>%{x}</b><br>Inflation: %{y:.0f}%<extra></extra>"))
    fig2b.update_layout(height=360, plot_bgcolor='white', paper_bgcolor='white',
                        title="Inflation 1990-2024 (log scale)", yaxis_title="CPI Annual % (log)",
                        yaxis_type="log", showlegend=False)
    fig2b.update_xaxes(showgrid=False); fig2b.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
    st.plotly_chart(fig2b, use_container_width=True)
    
#--------cChart 3: Oil Dependency --------------------------
st.markdown("### 🛢️ Oil Dependency: The Resource Curse")
col_oil1, col_oil2 = st.columns(2)

with col_oil1:
    fig3a = make_subplots(specs=[[{"secondary_y": True}]])
    fig3a.add_trace(go.Bar(x=df_filtered.index, y=df_filtered['oil_production_kbd'],
                           name="Oil Production (kbd)", marker_color=ORANGE, opacity=0.75,
                           hovertemplate="<b>%{x}</b><br>Production: %{y:,.0f} kbd<extra></extra>"),
                    secondary_y=False)
    fig3a.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['oil_rents_pct_gdp'],
                               name="Oil Rents (% GDP)", line=dict(color=NAVY, width=2.5),
                               hovertemplate="<b>%{x}</b><br>Oil Rents: %{y:.1f}%<extra></extra>"),
                    secondary_y=True)
    fig3a.update_layout(height=360, plot_bgcolor='white', paper_bgcolor='white',
                        title="Oil Production vs Oil Rents % GDP",
                        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'))
    fig3a.update_yaxes(title_text="Production (kbd)", secondary_y=False)
    fig3a.update_yaxes(title_text="Oil Rents (% GDP)", secondary_y=True)
    st.plotly_chart(fig3a, use_container_width=True)

with col_oil2:
    scatter_df=df_filtered[['oil_rents_pct_gdp','gdp_growth']].dropna()
    colors_sc=[GREEN if g > 0 else RED for g in scatter_df['gdp_growth']]
    fig3b=go.Figure()
    fig3b.add_trace(go.Scatter(x=scatter_df['oil_rents_pct_gdp'],
                               y=scatter_df['gdp_growth'], mode='markers+text',
                               marker=dict(color=colors_sc, size=9, opacity=0.8,
                                           line=dict(color='white', width=1)),
                               text=scatter_df.index.astype(str),
                               textposition='top center', textfont=dict(size=7),
                               hovertemplate="<b>%{text}</b><br>Oil Rents: %{x:.1f}%<br>GDP Growth: %{y:.1f}%<extra></extra>"))
    z= np.polyfit(scatter_df['oil_rents_pct_gdp'], scatter_df['gdp_growth'], 1)
    xline= np.linspace(scatter_df['oil_rents_pct_gdp'].min(), scatter_df['oil_rents_pct_gdp'].max(),100)
    corr_r=scatter_df.corr().iloc[0,1]
    fig3b.add_trace(go.Scatter(x=xline, y=np.poly1d(z)(xline),
                               mode='lines', line=dict(color=NAVY, width=1.5, dash='dash'),
                               name=f"Trend (r={corr_r:.2f})", showlegend=True))
    fig3b.add_hline(y=0, line_dash="dash", line_color=GRAY, line_width=1, opacity=0.5)
    fig3b.update_layout(height=360, plot_bgcolor='white', paper_bgcolor='white',
                        title=f"Oil Rents vs GDP Growth (Pearson r= {corr_r:.2f})",
                        xaxis_title="Oil Rents (% of GDP)", yaxis_title="GDP Growth (%)")
    st.plotly_chart(fig3b, use_container_width=True)
    
#----- Chart 4: Social Indicators -----------------------------
st.markdown("### 👥 Social Impact: Unemployment & Poverty")
col_soc1, col_soc2 = st.columns(2)

with col_soc1:
    fig4a=go.Figure()
    fig4a.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['unemployment_rate'],
                               fill='tozeroy', fillcolor='rgba(232,168,56,0.2)',
                               line=dict(color=ORANGE, width=2.5),
                               hovertemplate="<b>%{x}</b>Unemployment: %{y:.1f}%<extra></extra>"))
    fig4a.update_layout(height=340, plot_bgcolor='white', paper_bgcolor='white',
                  title="Unemployment Rate (%')", yaxis_title="% of Labor Force",
                  showlegend=False)
    fig4a.update_xaxes(showgrid=False); fig4a.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
    st.plotly_chart(fig4a, use_container_width=True)
    
with col_soc2:
    poverty_data = df_filtered['poverty_rate'].dropna()
    fig4b = go.Figure()
    fig4b.add_trace(go.Scatter(x=poverty_data.index, y=poverty_data,
        mode='lines+markers', line=dict(color=RED, width=2.5),
        marker=dict(size=8, color=RED),
        hovertemplate="<b>%{x}</b><br>Poverty Rate: %{y:.1f}%<extra></extra>"))
    fig4b.update_layout(height=340, plot_bgcolor='white', paper_bgcolor='white',
        title="Poverty Rate (% at $6.85/day)", yaxis_title="% Population",
        showlegend=False)
    fig4b.update_xaxes(showgrid=False); fig4b.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
    st.plotly_chart(fig4b, use_container_width=True)

# ── Correlation Heatmap ───────────────────────────────────────────────────────
st.markdown("### 🔗 Correlation Analysis")
with st.expander("View correlation heatmap between indicators", expanded=True):
    numeric_cols = ['gdp_growth','inflation','oil_rents_pct_gdp',
                    'gdp_per_capita_usd','unemployment_rate','oil_production_kbd']
    labels = ['GDP Growth','Inflation','Oil Rents %','GDP per Capita','Unemployment','Oil Production']
    corr_m = df_filtered[numeric_cols].corr()

    fig_corr = px.imshow(corr_m,
        labels=dict(x="Indicator", y="Indicator", color="Correlation"),
        x=labels, y=labels,
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        text_auto=".2f")
    fig_corr.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
        title="Pearson Correlation Matrix — Venezuela Economic Indicators")
    st.plotly_chart(fig_corr, use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        r1 = corr_m.loc['oil_rents_pct_gdp','gdp_growth']
        st.markdown(f"""<div class="insight-box">
        <b>Oil Rents ↔ GDP Growth</b><br>r = <b>{r1:.3f}</b><br>
        Strong positive correlation — Venezuela's growth cycles tightly follow oil revenue.</div>""",
        unsafe_allow_html=True)
    with col_c2:
        r2 = corr_m.loc['gdp_per_capita_usd','oil_production_kbd']
        st.markdown(f"""<div class="insight-box">
        <b>GDP per Capita ↔ Oil Production</b><br>r = <b>{r2:.3f}</b><br>
        GDP per capita tracks oil production — confirming structural resource dependency.</div>""",
        unsafe_allow_html=True)
    with col_c3:
        r3 = corr_m.loc['unemployment_rate','gdp_growth']
        st.markdown(f"""<div class="warning-box">
        <b>Unemployment ↔ GDP Growth</b><br>r = <b>{r3:.3f}</b><br>
        Negative correlation — GDP contraction directly translates to rising unemployment.</div>""",
        unsafe_allow_html=True)

# ── Summary Table ─────────────────────────────────────────────────────────────
st.markdown("### 📋 Data Table")
with st.expander("View raw data"):
    display_df = df_filtered[['gdp_growth','inflation','unemployment_rate',
                               'oil_production_kbd','gdp_per_capita_usd','oil_rents_pct_gdp']].copy()
    display_df.columns = ['GDP Growth (%)', 'Inflation (%)', 'Unemployment (%)',
                          'Oil Prod. (kbd)', 'GDP/Capita (USD)', 'Oil Rents (% GDP)']
    st.dataframe(display_df.round(1).style.background_gradient(
        subset=['GDP Growth (%)'], cmap='RdYlGn')
        .background_gradient(subset=['Inflation (%)'], cmap='YlOrRd'),
        use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 13px; padding: 12px;'>
Built by <b>Vilma Windevoxchel</b> · Data: World Bank WDI, IMF WEO Oct 2025, OPEC/EIA, CEPAL · 
<a href='https://www.linkedin.com/in/vilma-windevoxchel/' target='_blank'>LinkedIn</a> · 
<a href='https://github.com/VWinde' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
