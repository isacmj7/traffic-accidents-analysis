"""
Data processing for traffic accidents analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_state_accidents(filepath=None):
    """Load state-wise accidents data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "state_wise_accidents.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded state accidents: {len(df)} rows")
    return df


def load_state_fatalities(filepath=None):
    """Load state-wise fatalities data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "state_wise_fatalities.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded state fatalities: {len(df)} rows")
    return df


def load_collision_types(filepath=None):
    """Load collision types data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "collision_types.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded collision types: {len(df)} rows")
    return df


def load_violations(filepath=None):
    """Load violations data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "violations.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded violations: {len(df)} rows")
    return df


def load_safety_devices(filepath=None):
    """Load safety devices data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "safety_devices.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded safety devices: {len(df)} rows")
    return df


def load_road_users(filepath=None):
    """Load road users fatalities data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "road_users_fatalities.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded road users: {len(df)} rows")
    return df


def clean_state_data(df):
    """Clean state-wise data."""
    df_clean = df.copy()
    
    # Remove total rows if present
    if 'State/UT' in df_clean.columns:
        df_clean = df_clean[~df_clean['State/UT'].str.contains('Total|All India', case=False, na=False)]
    
    # Fill missing values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    
    print(f"Cleaned: {len(df_clean)} rows")
    return df_clean


def get_accident_stats(df):
    """Get accident statistics."""
    # Find year columns
    year_cols = [c for c in df.columns if c.isdigit() or (isinstance(c, str) and c.replace('.', '').isdigit())]
    
    if not year_cols:
        return {"error": "No year columns found"}
    
    total_by_year = {col: df[col].sum() for col in year_cols}
    
    return {
        'total_by_year': total_by_year,
        'num_states': len(df),
        'latest_year': max(year_cols),
        'latest_total': total_by_year[max(year_cols)]
    }


def get_top_states(df, year_col, n=10):
    """Get top states by accidents/fatalities."""
    if 'State/UT' not in df.columns:
        return None
    
    top = df.nlargest(n, year_col)[['State/UT', year_col]]
    return top


def calculate_growth_rate(df, start_year, end_year):
    """Calculate growth rate between years."""
    if start_year not in df.columns or end_year not in df.columns:
        return None
    
    df_clean = df.copy()
    df_clean['Growth_Rate'] = ((df_clean[end_year] - df_clean[start_year]) / df_clean[start_year]) * 100
    df_clean['Growth_Rate'] = df_clean['Growth_Rate'].replace([np.inf, -np.inf], np.nan)
    
    return df_clean


def export_for_tableau(accidents_df, fatalities_df, output_dir=None):
    """Export data for Tableau."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "tableau"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # State-wise summary
    if accidents_df is not None:
        accidents_df.to_csv(output_dir / "state_accidents_tableau.csv", index=False)
    
    if fatalities_df is not None:
        fatalities_df.to_csv(output_dir / "state_fatalities_tableau.csv", index=False)
    
    print(f"Exported to {output_dir}")


if __name__ == "__main__":
    accidents = load_state_accidents()
    accidents_clean = clean_state_data(accidents)
    
    stats = get_accident_stats(accidents_clean)
    print(f"\nStats: {stats}")
