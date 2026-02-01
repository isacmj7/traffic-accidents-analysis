"""
Visualizations for traffic accidents analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']


def save_fig(fig, filename, output_dir=None):
    """Save figure."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "visualizations"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    fig.savefig(output_dir / filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_year_trend(df, year_cols, title="Yearly Trend", output_dir=None):
    """Plot yearly trend."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    totals = [df[col].sum() for col in year_cols]
    
    ax.plot(year_cols, totals, marker='o', linewidth=2, markersize=8, color=COLORS[0])
    ax.fill_between(year_cols, totals, alpha=0.3, color=COLORS[0])
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Count')
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for i, (year, val) in enumerate(zip(year_cols, totals)):
        ax.annotate(f'{val:,.0f}', (year, val), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=9)
    
    plt.tight_layout()
    save_fig(fig, '01_yearly_trend.png', output_dir)


def plot_top_states(df, year_col, title="Top 10 States", output_dir=None, filename='02_top_states.png'):
    """Plot top states bar chart."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top10 = df.nlargest(10, year_col)[['State/UT', year_col]]
    
    bars = ax.barh(range(len(top10)), top10[year_col].values, color=COLORS[0])
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10['State/UT'].values)
    ax.invert_yaxis()
    
    ax.set_xlabel('Number of Accidents/Fatalities')
    ax.set_title(title, fontweight='bold')
    
    # Add value labels
    for bar, val in zip(bars, top10[year_col].values):
        ax.text(val + 500, bar.get_y() + bar.get_height()/2, f'{val:,.0f}', 
               va='center', fontsize=9)
    
    plt.tight_layout()
    save_fig(fig, filename, output_dir)


def plot_collision_types(df, output_dir=None):
    """Plot collision types analysis."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Assuming columns for accidents and fatalities
    accident_col = [c for c in df.columns if 'accident' in c.lower() or 'number' in c.lower()]
    type_col = [c for c in df.columns if 'type' in c.lower() or 'collision' in c.lower()]
    
    if accident_col and type_col:
        data = df[[type_col[0], accident_col[0]]].head(10)
        
        axes[0].barh(range(len(data)), data[accident_col[0]].values, color=COLORS[0])
        axes[0].set_yticks(range(len(data)))
        axes[0].set_yticklabels(data[type_col[0]].values)
        axes[0].set_title('Accidents by Collision Type')
        axes[0].invert_yaxis()
    
    axes[1].text(0.5, 0.5, 'Fatalities by Collision Type', ha='center', va='center', fontsize=12)
    axes[1].axis('off')
    
    plt.suptitle('Collision Type Analysis', fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '03_collision_types.png', output_dir)


def plot_violations(df, output_dir=None):
    """Plot violations analysis."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Find relevant columns
    cols = df.columns.tolist()
    if len(cols) >= 2:
        type_col = cols[0]
        value_col = cols[1]
        
        data = df[[type_col, value_col]].dropna().head(15)
        
        colors = [COLORS[i % len(COLORS)] for i in range(len(data))]
        ax.barh(range(len(data)), data[value_col].values, color=colors)
        ax.set_yticks(range(len(data)))
        ax.set_yticklabels(data[type_col].values)
        ax.invert_yaxis()
    
    ax.set_title('Accidents by Traffic Violation Type', fontweight='bold')
    ax.set_xlabel('Number of Accidents')
    
    plt.tight_layout()
    save_fig(fig, '04_violations.png', output_dir)


def plot_safety_devices(df, output_dir=None):
    """Plot safety devices analysis."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    cols = df.columns.tolist()
    
    # Pie chart for overall
    if len(cols) >= 2:
        data = df[cols[1]].head(5)
        labels = df[cols[0]].head(5)
        
        axes[0].pie(data, labels=labels, autopct='%1.1f%%', colors=COLORS)
        axes[0].set_title('Safety Device Absence Distribution')
    
    # Bar chart
    if len(cols) >= 2:
        data = df[[cols[0], cols[1]]].head(10)
        axes[1].barh(range(len(data)), data[cols[1]].values, color=COLORS[1])
        axes[1].set_yticks(range(len(data)))
        axes[1].set_yticklabels(data[cols[0]].values)
        axes[1].set_title('Accidents by Safety Device Type')
        axes[1].invert_yaxis()
    
    plt.suptitle('Safety Device Analysis', fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '05_safety_devices.png', output_dir)


def plot_road_users(df, output_dir=None):
    """Plot road users fatalities."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    cols = df.columns.tolist()
    
    if len(cols) >= 2:
        type_col = cols[0]
        value_col = cols[1]
        
        data = df[[type_col, value_col]].dropna()
        
        colors = [COLORS[i % len(COLORS)] for i in range(len(data))]
        wedges, texts, autotexts = ax.pie(data[value_col], labels=data[type_col], 
                                          autopct='%1.1f%%', colors=colors, explode=[0.02]*len(data))
        
        for autotext in autotexts:
            autotext.set_fontsize(9)
    
    ax.set_title('Fatalities by Road User Type', fontweight='bold')
    
    plt.tight_layout()
    save_fig(fig, '06_road_users.png', output_dir)


def plot_state_comparison(accidents_df, fatalities_df, year_col, output_dir=None):
    """Plot state comparison for accidents and fatalities."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Top 10 by accidents
    if 'State/UT' in accidents_df.columns:
        top_accidents = accidents_df.nlargest(10, year_col)
        axes[0].barh(range(len(top_accidents)), top_accidents[year_col].values, color=COLORS[0])
        axes[0].set_yticks(range(len(top_accidents)))
        axes[0].set_yticklabels(top_accidents['State/UT'].values)
        axes[0].invert_yaxis()
        axes[0].set_title('Top 10 States by Accidents')
        axes[0].set_xlabel('Number of Accidents')
    
    # Top 10 by fatalities
    if 'State/UT' in fatalities_df.columns:
        top_fatalities = fatalities_df.nlargest(10, year_col)
        axes[1].barh(range(len(top_fatalities)), top_fatalities[year_col].values, color=COLORS[1])
        axes[1].set_yticks(range(len(top_fatalities)))
        axes[1].set_yticklabels(top_fatalities['State/UT'].values)
        axes[1].invert_yaxis()
        axes[1].set_title('Top 10 States by Fatalities')
        axes[1].set_xlabel('Number of Fatalities')
    
    plt.suptitle(f'State-wise Comparison ({year_col})', fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '07_state_comparison.png', output_dir)


def create_all_visualizations(accidents_df, fatalities_df, year_cols, output_dir=None):
    """Create all charts."""
    print("Creating visualizations...")
    
    plot_year_trend(accidents_df, year_cols, title="Road Accidents Trend (2019-2023)", output_dir=output_dir)
    
    if year_cols:
        latest = year_cols[-1]
        plot_top_states(accidents_df, latest, title=f"Top 10 States by Accidents ({latest})", output_dir=output_dir)
        plot_state_comparison(accidents_df, fatalities_df, latest, output_dir=output_dir)
    
    print("Done!")


if __name__ == "__main__":
    from data_processing import load_state_accidents, load_state_fatalities, clean_state_data
    
    accidents = load_state_accidents()
    fatalities = load_state_fatalities()
    
    accidents_clean = clean_state_data(accidents)
    fatalities_clean = clean_state_data(fatalities)
    
    year_cols = ['2019', '2020', '2021', '2022', '2023']
    create_all_visualizations(accidents_clean, fatalities_clean, year_cols)
