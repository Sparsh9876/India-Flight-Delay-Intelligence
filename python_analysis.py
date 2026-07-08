"""
================================================================
      PYTHON SCRIPT — India Flight Delay Intelligence
================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path
import os 

# ── Colours ───────────
NAVY   = '#1F4E79'
RED    = '#C0392B'
GREEN  = '#1A7A4A'
ORANGE = '#E67E22'
PURPLE = '#8E44AD'
LIGHT  = '#F8F9FA'
MUTED  = '#7F8C8D'

AIRLINE_COLORS = {
    'IndiGo'       : NAVY,
    'Air India'    : RED,
    'Akasa Air'    : GREEN,
    'SpiceJet'     : ORANGE,
    'Vistara'      : PURPLE,
    'AirAsia India': '#1ABC9C',
    'Alliance Air' : MUTED
}

print("=" * 55)
print("  INDIA FLIGHT DELAY — PYTHON ANALYSIS")
print("=" * 55)

# ================================
#  DATA CLEANING
# ================================
print("\n------ DATA CLEANING ---------")

BASE_DIR = Path(__file__).parent

# Create output folders automatically
(BASE_DIR / "clean_data").mkdir(exist_ok=True)
(BASE_DIR / "visuals").mkdir(exist_ok=True)

# ----- File -01 : OTP DATA -------------------------------

df_otp = pd.read_csv(BASE_DIR / "raw_data" / "otp_rawdata.csv")

print(f"\n  OTP raw shape   : {df_otp.shape}")
print(f"  OTP columns     : {df_otp.columns.tolist()}")

# melt() reshapes wide → long
# id_vars    = columns to keep as-is
# value_vars = columns to stack into rows
# var_name   = name for the new "month" column
# value_name = name for the OTP values

otp = df_otp.melt(   
    id_vars=['Sl. No.', 'Airline'],
    value_vars=['January','February','March','April','May'],
    var_name='month_name',
    value_name='otp_pct'
)
 
# Add month number for sorting
otp['month_num'] = otp['month_name'].map(
    {'January':1,'February':2,'March':3,'April':4,'May':5}
)
otp['year'] = 2024
 
# Standardise airline names
otp['airline'] = otp['Airline'].str.strip().replace({
    'Indigo'   : 'IndiGo',
    'Air Asia' : 'AirAsia India',
    'Spice Jet': 'SpiceJet'
})
 
# Add business flag
otp['otp_status'] = otp['otp_pct'].apply(
    lambda x: 'Above 85%' if x >= 85 else
              'Meets 75%' if x >= 75 else 'Below Min'
)
 
otp = otp[['year','month_num','month_name','airline','otp_pct','otp_status']]
otp = otp.sort_values(['airline','month_num']).reset_index(drop=True)
 
print(f"  OTP clean shape : {otp.shape}")
print(f"  Airlines        : {otp['airline'].unique().tolist()}")
print(f"  OTP range       : {otp['otp_pct'].min()}% – {otp['otp_pct'].max()}%")
print(f"  Nulls           : {otp.isnull().sum().sum()}")
otp.to_csv(BASE_DIR / "clean_data" / "clean_otp.csv", index=False)
print("  Saved → clean_data/clean_otp.csv ✓")


# -----File:02 CARRIER DATA -------------------------
df_carrier= pd.read_csv(BASE_DIR / "raw_data" / "raw_carrier.csv")
print(f"\n  Carrier raw shape: {df_carrier.shape}")
 
# Keep only Scheduled Domestic
carrier = df_carrier[df_carrier['Type'] == 'ScheduledDomestic'].copy()
carrier = carrier[~carrier['Airline'].isin(
    ['Total Domestic','Total International','Grand Total']
)]
 
# Keep useful columns only
carrier = carrier[['Airline','Year','Month',
                   'Aircraft Number','Passenger Number',
                   'Passenger Load Factor']].copy()
 
carrier.columns = ['airline','year','month',
                   'aircraft_count','passenger_count','load_factor_pct']
 
# Add month name
carrier['month_name'] = carrier['month'].map({
    1:'January',2:'February',3:'March',4:'April',
    5:'May',6:'June',7:'July',8:'August',
    9:'September',10:'October',11:'November',12:'December'
})
 
# Standardise airline names
carrier['airline'] = carrier['airline'].str.strip().replace({
    'Indigo'     : 'IndiGo',
    'Air Asia'   : 'AirAsia India',
    'AIX Connect': 'AirAsia India',
    'Spice Jet'  : 'SpiceJet'
})
 
# Fix data types
carrier['load_factor_pct'] = pd.to_numeric(
    carrier['load_factor_pct'], errors='coerce')
carrier['passenger_count'] = pd.to_numeric(
    carrier['passenger_count'], errors='coerce')
 
# Fill nulls with median
carrier['load_factor_pct'].fillna(
    carrier['load_factor_pct'].median(), inplace=True)
 
# Remove zero-passenger rows
carrier = carrier[carrier['passenger_count'] > 0].reset_index(drop=True)
 
print(f"  Carrier clean   : {len(carrier):,} rows")
print(f"  Years           : {carrier['year'].min()} – {carrier['year'].max()}")
print(f"  Nulls           : {carrier.isnull().sum().sum()}")

carrier.to_csv(BASE_DIR / "clean_data" / "clean_carrier.csv", index=False)
print("  Saved → clean_data/clean_carrier.csv ✓")

# --- File no:03  CITY / ROUTE DATA --------------------------
df_city= pd.read_csv(BASE_DIR / "raw_data" / "raw_city.csv")
print(f"\n  City raw shape  : {df_city.shape}")
 
df_city['City1'] = df_city['City1'].str.strip().str.title()
df_city['City2'] = df_city['City2'].str.strip().str.title()
df_city['total_pax'] = df_city['PaxToCity2'] + df_city['PaxFromCity2']
 
city = df_city.rename(columns={
    'Year':'year','Month':'month',
    'City1':'origin_city','City2':'dest_city',
    'PaxToCity2':'pax_to','PaxFromCity2':'pax_from'
})[['year','month','origin_city','dest_city',
    'pax_to','pax_from','total_pax']]
 
city = city[city['total_pax'] > 0].reset_index(drop=True)
 
print(f"  City clean      : {len(city):,} rows")
print(f"  Unique cities   : {city['origin_city'].nunique()}")

city.to_csv(BASE_DIR / "clean_data" / "clean_city.csv", index=False)
print("  Saved → clean_data/clean_city.csv ✓")


#-----file :04 Daily OTP Data ----------------------------------------

df_daily= pd.read_csv(BASE_DIR / "raw_data" / "raw_daily.csv")
print(f"\n  Daily raw shape : {df_daily.shape} (166 cols → trimmed to ~15)")
 
df_daily['Date'] = pd.to_datetime(df_daily['Date'])
df_daily['year']  = df_daily['Date'].dt.year
df_daily['month'] = df_daily['Date'].dt.month
 
# Extract only the OTP columns we need
otp_map = {
    'On Time Performance (Indigo)'   : 'otp_indigo',
    'On Time Performance (Air India)': 'otp_airindia',
    'On Time Performance (Spicejet)' : 'otp_spicejet',
    'On Time Performance (Vistara)'  : 'otp_vistara',
    'On Time Performance (Akasa Air)': 'otp_akasa',
}
plf_map = {
    'Passenger Load Factor (Indigo)'   : 'plf_indigo',
    'Passenger Load Factor (Air India)': 'plf_airindia',
}
 
daily = df_daily[['Date','year','month']].copy()
daily = daily.rename(columns={'Date':'date'})
 
for old, new in {**otp_map, **plf_map}.items():
    if old in df_daily.columns:
        daily[new] = pd.to_numeric(
            df_daily[old].astype(str).str.replace('%',''),
            errors='coerce').round(2)
 
daily = daily.dropna(subset=['otp_indigo'], how='all').reset_index(drop=True)
 
print(f"  Daily clean     : {len(daily):,} rows")
print(f"  Date range      : {daily['date'].min().date()} → {daily['date'].max().date()}")
print(f"  Nulls (otp_indigo): {daily['otp_indigo'].isnull().sum()}")

daily.to_csv(BASE_DIR / "clean_data" / "clean_daily.csv", index=False)
print("  Saved → clean_data/clean_daily.csv ✓")

# ===================================================
#                EDA & CHARTS
# ===================================================

print("\n------ EDA & CHARTS ---------------------")
 
# ---- CHART 1: OTP Ranking --------------------------
print("\n  Building Chart 1 — OTP Ranking...")
 
otp_rank = (otp.groupby('airline')['otp_pct']
              .mean()
              .sort_values(ascending=True))
 
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('white')
 
colors = [RED if v < 75 else ORANGE if v < 85 else GREEN
          for v in otp_rank.values]
 
bars = ax.barh(otp_rank.index, otp_rank.values,
               color=colors, edgecolor='white', height=0.6)
 
ax.axvline(75, color=ORANGE, linestyle='--', linewidth=2,
           label='DGCA minimum (75%)')
ax.axvline(85, color=GREEN,  linestyle='--', linewidth=1.5,
           label='Ideal target (85%)')
 
for bar, val in zip(bars, otp_rank.values):
    ax.text(val + 0.4,
            bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center',
            fontsize=10, fontweight='bold', color=NAVY)
 
ax.set_xlabel('Average OTP % (Jan–May 2024)', fontsize=11)
ax.set_title('India Domestic Airline OTP Ranking — 2024\n'
             'Source: DGCA India ',
             fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10)
ax.set_facecolor(LIGHT)
ax.grid(axis='x', alpha=0.4)
ax.set_xlim(0, 100)
 
plt.tight_layout()
plt.savefig(BASE_DIR / "visuals" / "chart1_otp_ranking.png", dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()

print("  ✓ chart1_otp_ranking.png")


# ----- CHART 2: Monthly OTP Trend -------------------------------
print("  Building Chart 2 — Monthly OTP Trend...")
 
fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor('white')
 
for airline in otp['airline'].unique():
    sub = otp[otp['airline'] == airline].sort_values('month_num')
    ax.plot(sub['month_name'], sub['otp_pct'],
            marker='o', markersize=6, linewidth=2,
            label=airline,
            color=AIRLINE_COLORS.get(airline, MUTED))
    for _, row in sub.iterrows():
        ax.annotate(f"{row['otp_pct']:.0f}",
                    (row['month_name'], row['otp_pct']),
                    textcoords='offset points', xytext=(0,8),
                    ha='center', fontsize=7.5,
                    color=AIRLINE_COLORS.get(airline, MUTED))
 
ax.axhline(75, color=ORANGE, linestyle='--',
           linewidth=1.5, label='75% Benchmark')
ax.set_ylim(30, 100)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('OTP %', fontsize=11)
ax.set_title('Monthly OTP Trend — All Airlines (Jan-May 2024)',
             fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=8, bbox_to_anchor=(1.01, 1), loc='upper left')
ax.set_facecolor(LIGHT)
ax.grid(alpha=0.3)
 
plt.tight_layout()
plt.savefig(BASE_DIR/"visuals"/"chart2_monthly_trend.png", dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart2_monthly_trend.png")

# -----CHART 3: IndiGo Deep Dive ------------------------------
print("  Building Chart 3 — IndiGo Deep Dive...")
 
indigo = otp[otp['airline'] == 'IndiGo'].sort_values('month_num')
ind_avg = otp.groupby('month_name')['otp_pct'].mean()
 
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('white')
 
colors3 = [GREEN if v >= 75 else RED for v in indigo['otp_pct']]
bars = ax.bar(indigo['month_name'], indigo['otp_pct'],
              color=colors3, edgecolor='white', width=0.55)
 
# Industry avg line
ax.plot(indigo['month_name'],
        [ind_avg.get(m, np.nan) for m in indigo['month_name']],
        color=MUTED, linewidth=1.5, linestyle='-.', marker='s',
        markersize=5, label='Industry Avg')
 
ax.axhline(75, color=ORANGE, linestyle='--',
           linewidth=2, label='75% minimum')
ax.axhline(85, color=GREEN, linestyle='--',
           linewidth=1.5, label='85% target')
 
for bar, val in zip(bars, indigo['otp_pct']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.8,
            f'{val:.1f}%', ha='center',
            fontsize=11, fontweight='bold', color=NAVY)
 
ax.set_ylim(0, 100)
ax.set_ylabel('OTP %', fontsize=11)
ax.set_title('IndiGo OTP — Jan to May 2024  |  vs Industry Average',
             fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10)
ax.set_facecolor(LIGHT)
ax.grid(axis='y', alpha=0.4)
 
plt.tight_layout()
plt.savefig(BASE_DIR/'visuals'/'chart3_indigo_deepdive.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart3_indigo_deepdive.png")

# ---- CHART 4: OTP Heatmap ------------------------------
print("  Building Chart 4 — OTP Heatmap...")
 
heatmap = otp.pivot(index='airline', columns='month_name', values='otp_pct')
heatmap = heatmap.reindex(
    columns=['January','February','March','April','May'])
 
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('white')
 
sns.heatmap(heatmap, annot=True, fmt='.1f',
            cmap='RdYlGn', vmin=40, vmax=95,
            linewidths=0.5, linecolor='white', ax=ax,
            annot_kws={'size':11,'weight':'bold'})
 
ax.set_title('OTP % Heatmap — Airline × Month (2024)\n'
             'Red = Poor  |  Yellow = Marginal  |  Green = Good',
             fontsize=13, fontweight='bold', color=NAVY)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Airline', fontsize=11)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
 
plt.tight_layout()
plt.savefig(BASE_DIR/'visuals'/'chart4_otp_heatmap.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart4_otp_heatmap.png")
 

#------- CHART 5: Daily OTP Trend ----------------------------------
print("  Building Chart 5 — Daily OTP Trend (2021–2026)...")
 
for col in ['otp_indigo','otp_airindia','otp_spicejet','otp_vistara']:
    if col in daily.columns:
        daily[col] = pd.to_numeric(daily[col], errors='coerce')
 
daily['year_month'] = pd.to_datetime(daily['date']).dt.to_period('M')
monthly = (daily.groupby('year_month')
           [['otp_indigo','otp_airindia','otp_spicejet']]
           .mean().reset_index())
 
fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor('white')
 
ax.plot(range(len(monthly)), monthly['otp_indigo'],
        color=NAVY,   linewidth=2.2, label='IndiGo')
ax.plot(range(len(monthly)), monthly['otp_airindia'],
        color=RED,    linewidth=2,   label='Air India')
ax.plot(range(len(monthly)), monthly['otp_spicejet'],
        color=ORANGE, linewidth=1.8, label='SpiceJet', alpha=0.85)
 
ax.axhline(75, color='gray', linestyle='--',
           linewidth=1, alpha=0.5, label='75% benchmark')
 
# Year labels on x-axis
year_ticks, year_labels = [], []
for i, row in monthly.iterrows():
    ym = str(row['year_month'])
    if ym[5:7] == '01':
        year_ticks.append(i)
        year_labels.append(ym[:4])
 
ax.set_xticks(year_ticks)
ax.set_xticklabels(year_labels, fontsize=10)
ax.set_ylabel('Monthly Avg OTP %', fontsize=11)
ax.set_ylim(0, 110)
ax.set_title('OTP Trend — IndiGo vs Air India vs SpiceJet (2021–2026)\n'
             'Source: DGCA Daily Dashboard',
             fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10)
ax.set_facecolor(LIGHT)
ax.grid(alpha=0.3)
 
plt.tight_layout()
plt.savefig(BASE_DIR/'visuals'/'chart5_daily_trend.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart5_daily_trend.png")

 
# ----CHART 6: Top 10 Busiest Routes ---------------------------
print("  Building Chart 6 — Top 10 Busiest Routes...")
 
city_2024 = city[city['year'] == 2024]
top10 = (city_2024.groupby(['origin_city','dest_city'])['total_pax']
         .sum().reset_index()
         .nlargest(10,'total_pax').reset_index(drop=True))
top10['route'] = (top10['origin_city'].str.title() + ' ↔ ' +
                  top10['dest_city'].str.title())
 
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor('white')
 
colors6 = [NAVY if i < 3 else '#5B8DB8' for i in range(len(top10))]
bars = ax.barh(top10['route'][::-1],
               top10['total_pax'][::-1] / 1_000_000,
               color=colors6[::-1], edgecolor='white', height=0.6)
 
for bar, val in zip(bars, top10['total_pax'][::-1]):
    ax.text(val/1_000_000 + 0.03,
            bar.get_y() + bar.get_height()/2,
            f'{val/1_000_000:.2f}M', va='center',
            fontsize=9.5, fontweight='bold', color=NAVY)
 
ax.set_xlabel('Total Passengers (Millions) — 2024', fontsize=11)
ax.set_title('Top 10 Busiest Domestic Routes — India 2024\n'
             'Source: DGCA City-Pair Traffic Data',
             fontsize=13, fontweight='bold', color=NAVY)
ax.set_facecolor(LIGHT)
ax.grid(axis='x', alpha=0.4)
 
plt.tight_layout()
plt.savefig(BASE_DIR/'visuals'/'chart6_busiest_routes.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart6_busiest_routes.png")
 
#-------- CHART 7: IndiGo Load Factor Trend --------------------
print("  Building Chart 7 — IndiGo Load Factor Trend...")
 
indigo_lf = (carrier[carrier['airline'] == 'IndiGo']
             .groupby('year')['load_factor_pct']
             .mean().reset_index())
indigo_lf = indigo_lf[indigo_lf['year'] <= 2024]
 
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('white')
 
ax.plot(indigo_lf['year'], indigo_lf['load_factor_pct'],
        color=NAVY, linewidth=2.5, marker='o', markersize=7)
ax.fill_between(indigo_lf['year'], indigo_lf['load_factor_pct'],
                alpha=0.1, color=NAVY)
 
covid = indigo_lf[indigo_lf['year'] == 2020]
if not covid.empty:
    ax.annotate('COVID-19', xy=(2020, covid['load_factor_pct'].values[0]),
                xytext=(2021.2, 50),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
                fontsize=9, color=RED, fontweight='bold')
 
for _, row in indigo_lf.iterrows():
    ax.annotate(f"{row['load_factor_pct']:.1f}%",
                (row['year'], row['load_factor_pct']),
                textcoords='offset points', xytext=(0,10),
                ha='center', fontsize=9, color=NAVY)
 
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Passenger Load Factor (%)', fontsize=11)
ax.set_ylim(40, 100)
ax.set_title('IndiGo Load Factor Trend (2015–2024)\n'
             'Source: DGCA Carrier Data',
             fontsize=13, fontweight='bold', color=NAVY)
ax.set_facecolor(LIGHT)
ax.grid(alpha=0.3)
 
plt.tight_layout()
plt.savefig(BASE_DIR/'visuals'/'chart7_indigo_lf.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ chart7_indigo_lf.png")
 
 #----------------------------------
 #    END EDA & CLEANING
 #----------------------------------

print("\n" + "=" * 55)
print("  PYTHON SCRIPT COMPLETE")
print("  7 charts → visuals/  |  4 CSVs → clean_data/")
print("  Next: sql analysis ")
print("=" * 55)