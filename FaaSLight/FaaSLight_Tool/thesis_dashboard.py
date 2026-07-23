import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="FaaSLight Gap 2 — Thesis Dashboard",
    page_icon="",
    layout="wide"
)

st.title("FaaSLight - Improvement to Optional Functions")

# ── Load results dynamically from JSON files ──────────
result_files = sorted([
    f for f in os.listdir('.')
    if f.endswith('_result.json')
])

records = []
for rf in result_files:
    try:
        with open(rf, 'r') as f:
            r = json.load(f)
        app_name = r.get('app', rf.replace('_result.json', ''))
        if app_name == 'realApp':
            library = 'arrow'
        else:
            library = app_name.replace('app_', '')
        records.append({
            'Application': app_name,
            'Library': library,
            'Optional Functions': r.get('optional_functions', 0),
            'Used Functions': r.get('indispensable', 0),
            'Hybrid Groups': r.get('hybrid_groups', 0),
            'Original (ms)': r.get('original_ms', 0),
            'Hybrid (ms)': r.get('hybrid_ms', 0),
            'Improvement (%)': r.get('improvement_pct', 0)
        })
    except Exception as e:
        st.warning("Could not load {}: {}".format(rf, e))

if not records:
    st.error("No result JSON files found. Run the pipeline first.")
    st.stop()

df = pd.DataFrame(records)

# ── KPI Cards ─────────────────────────────────────────
st.subheader("Summary")
total_apps = len(df)
total_optional = int(df["Optional Functions"].sum())
best_improvement = df["Improvement (%)"].max()
avg_improvement = df[
    df["Improvement (%)"] > 0]["Improvement (%)"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Applications Tested", total_apps)
col2.metric("Total Optional Functions", total_optional)
col3.metric("Best Improvement", f"{best_improvement:.1f}%")
col4.metric("Average Improvement", f"{avg_improvement:.1f}%")

st.divider()

# ── Filter valid apps only ────────────────────────────
df_valid = df[df["Optional Functions"] > 0].copy()
apps = df_valid["Library"].tolist()
orig = df_valid["Original (ms)"].tolist()
hyb = df_valid["Hybrid (ms)"].tolist()
impr = df_valid["Improvement (%)"].tolist()

# ── Charts ────────────────────────────────────────────
st.subheader("Loading Time Comparison")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(apps))
    width = 0.35
    b1 = ax.bar(x - width/2, orig, width,
                label='Original FaaSLight', color='#5DADE2')
    b2 = ax.bar(x + width/2, hyb, width,
                label='Hybrid Improvement', color='#1F4E79')
    ax.set_ylabel('Loading Time (ms)')
    ax.set_title('Original vs Hybrid Loading Time')
    ax.set_xticks(x)
    ax.set_xticklabels(apps, rotation=45,
                       ha='right', fontsize=8)
    ax.legend()
    ax.bar_label(b1, fmt='%.3f', padding=2, fontsize=7)
    ax.bar_label(b2, fmt='%.3f', padding=2, fontsize=7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['#FFD580'] * len(impr)
    bars = ax.bar(apps, impr, color=colors, width=0.4)
    ax.set_ylabel('Improvement (%)')
    ax.set_title('Percentage Improvement per Application')
    ax.set_ylim(0, 105)
    ax.set_xticks(range(len(apps)))
    ax.set_xticklabels(apps, rotation=45,
                       ha='right', fontsize=8)
    ax.bar_label(bars, fmt='%.1f%%', padding=3,
                 fontsize=9, fontweight='bold')
    avg = sum(impr) / len(impr)
    ax.axhline(y=avg, color='red', linestyle='--',
               alpha=0.7,
               label=f'Average: {avg:.1f}%')
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Results Table ─────────────────────────────────────
st.subheader("Detailed Results")
st.dataframe(
    df.style.format({
        'Original (ms)': '{:.4f}',
        'Hybrid (ms)': '{:.4f}',
        'Improvement (%)': '{:.1f}%'
    }),
    width='stretch'
)

st.divider()
st.caption("Results loaded from: {}".format(
    ", ".join(result_files)))