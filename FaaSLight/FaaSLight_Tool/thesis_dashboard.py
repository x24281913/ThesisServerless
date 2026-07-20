import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="FaaSLight Gap 2 — Thesis Dashboard",
    page_icon="",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────
st.title("Faaslight - Improvement to optional functions")
# ── Data ──────────────────────────────────────────────
data = {
    'Application': ['realApp (arrow)', 'app_requests', 'app_dateutil', 'app_boto3'],
    'Library': ['arrow', 'requests', 'dateutil', 'boto3'],
    'Optional Functions': [44, 129, 29, 0],
    'Used Functions': [123, 885, 484, 1416],
    'Hybrid Groups': [5, 11, 4, 0],
    'Original (ms)': [0.4301, 2.025, 0.4015, 0],
    'Hybrid (ms)': [0.0505, 0.0845, 0.071, 0],
    'Improvement (%)': [88.3, 95.8, 82.3, 0]
}
df = pd.DataFrame(data)

# ── KPI Cards ─────────────────────────────────────────
st.subheader("Summary")

# Dynamic calculations
total_apps = df["Application"].nunique()
total_optional = df["Optional Functions"].sum()
best_improvement = df["Improvement (%)"].max()
best_app = df.loc[df["Improvement (%)"].idxmax(), "Application"]
avg_improvement = df[df["Improvement (%)"] > 0]["Improvement (%)"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Applications Tested", total_apps)
col2.metric("Total Optional Functions", total_optional)
col3.metric("Best Improvement", f"{best_improvement:.1f}%")
col4.metric("Average Improvement", f"{avg_improvement:.1f}%")

st.divider()

# ── Charts ────────────────────────────────────────────
st.subheader("Loading Time Comparison")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    apps = ['realApp', 'app_requests', 'app_dateutil']
    orig = [0.4301, 2.025, 0.4015]
    hyb  = [0.0505, 0.0845, 0.071]
    x = np.arange(len(apps))
    width = 0.35
    b1 = ax.bar(x - width/2, orig, width, label='Original FaaSLight', color='#5DADE2')
    b2 = ax.bar(x + width/2, hyb,  width, label='Hybrid Improvement',  color='#1F4E79')
    ax.set_ylabel('Loading Time (ms)')
    ax.set_title('Original vs Hybrid Loading Time')
    ax.set_xticks(x)
    ax.set_xticklabels(apps)
    ax.legend()
    ax.bar_label(b1, fmt='%.4f', padding=2, fontsize=8)
    ax.bar_label(b2, fmt='%.4f', padding=2, fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    impr = [88.3, 95.8, 82.3]
    colors = ['#FFD580', '#FFD580', '#FFD580']
    bars = ax.bar(apps, impr, color=colors, width=0.4)
    ax.set_ylabel('Improvement (%)')
    ax.set_title('Percentage Improvement per Application')
    ax.set_ylim(0, 105)
    ax.bar_label(bars, fmt='%.1f%%', padding=5, fontsize=12, fontweight='bold')
    avg = sum(impr) / len(impr)
    ax.axhline(y=avg, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg:.1f}%')
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
    use_container_width=True
)

st.divider()
