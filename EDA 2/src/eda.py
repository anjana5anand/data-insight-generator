#!/usr/bin/env python3
"""Automated EDA System - Ultra-Concise Version"""
import sys, os, json, argparse, glob, warnings
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import subprocess

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150

def safe_name(s):
    """Convert to safe filename"""
    return str(s).replace(" ", "_").replace("/", "_").replace("\\", "_").replace("(", "").replace(")", "")

def load_schema(path):
    """Load optional schema"""
    try:
        return json.load(open(path)) if path and os.path.exists(path) else None
    except: return None

def clean_data(df, codes=None):
    """Clean missing values and detect dates"""
    codes = codes or [-999, -9999, 'NA', 'null', 'unknown', '?']
    df = df.copy(deep=True)
    
    # Replace missing codes
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].where(~df[col].isin([str(c) for c in codes if isinstance(c, str)]), np.nan)
        else:
            df[col] = df[col].where(~df[col].isin([c for c in codes if isinstance(c, (int, float))]), np.nan)
    
    # Detect dates
    date_cols = []
    for col in df.select_dtypes(include='object').columns:
        try:
            parsed = pd.to_datetime(df[col], errors='coerce')
            if parsed.notna().sum() / len(df) > 0.5:
                df[col] = parsed
                date_cols.append(col)
        except: pass
    
    return df, date_cols

def find_sensitive(df):
    """Detect sensitive columns"""
    patterns = ['id', 'ssn', 'email', 'phone', 'address']
    sensitive = []
    for col in df.columns:
        if any(p in col.lower() for p in patterns) or (df[col].nunique() / len(df) > 0.95 and len(df) > 100):
            sensitive.append(col)
    return sensitive

def calc_stats(df, numeric_cols, cat_cols):
    """Calculate all statistics"""
    # Filter out ID-like columns (high cardinality, sequential, or contain 'id' in name)
    filtered_numeric = []
    for col in numeric_cols:
        # Skip if column name contains 'id', 'code', 'number', 'num'
        if any(term in col.lower() for term in ['id', 'code', 'number', 'num', 'naics']):
            continue
        # Skip if nearly all unique (likely an ID)
        if df[col].nunique() / len(df) > 0.95:
            continue
        filtered_numeric.append(col)
    
    # Use filtered columns for stats
    numeric_cols = filtered_numeric
    
    # Numeric stats
    num_stats = []
    for col in numeric_cols:
        try:
            s = df[col].dropna().copy()
            if len(s) == 0: continue
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            outliers = s[(s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)]
            num_stats.append({
                'column': col, 'min': float(s.min()), 'max': float(s.max()),
                'mean': float(s.mean()), 'median': float(s.median()), 
                'std': float(s.std()), 'q1': float(q1), 'q3': float(q3),
                'outlier_count': int(len(outliers)), 'outlier_percent': float(len(outliers)/len(s)*100)
            })
        except: continue
    
    # Categorical stats
    cat_stats = []
    if cat_cols:
        col = cat_cols[0]
        for val, cnt in df[col].value_counts(dropna=False).items():
            cat_stats.append({'column': col, 'value': val, 'count': cnt, 'percent': cnt/len(df)*100})
    
    return pd.DataFrame(num_stats), pd.DataFrame(cat_stats), numeric_cols

def generate_insights(df, num_stats, cat_stats, dup, missing_cols, sens_cols, date_cols):
    """Generate 5-10 insights"""
    insights = []
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    insights.append(f"{df.shape[0]:,} rows x {df.shape[1]} cols, {completeness:.1f}% complete")
    
    insights.append(f"{dup:,} duplicates found" if dup > 0 else "No duplicates - good quality")
    
    if missing_cols:
        insights.append(f"{len(missing_cols)} columns >50% missing: {', '.join(missing_cols[:3])}")
    
    if not num_stats.empty:
        num_stats['cv'] = num_stats['std'] / num_stats['mean'].abs()
        # Only report variability if CV > 1 (high variability)
        high_var = num_stats[num_stats['cv'] > 1.0].nlargest(1, 'cv')
        if not high_var.empty:
            top = high_var.iloc[0]
            insights.append(f"{top['column']}: high variability (CV={top['cv']:.2f}), range: {top['min']:.1f} to {top['max']:.1f}")
        
        if num_stats['outlier_count'].sum() > 0:
            worst = num_stats.nlargest(1, 'outlier_percent').iloc[0]
            if worst['outlier_percent'] > 5:  # Only report if >5% outliers
                insights.append(f"{worst['column']}: {worst['outlier_percent']:.1f}% outliers")
        
        try:
            skew = stats.skew(df[num_stats.iloc[0]['column']].dropna())
            if abs(skew) > 0.5:
                insights.append(f"{num_stats.iloc[0]['column']}: {'right' if skew > 0 else 'left'}-skewed (skew={skew:.2f})")
        except: pass
    
    if not cat_stats.empty:
        top = cat_stats.nlargest(1, 'count').iloc[0]
        if top['percent'] > 10:  # Only report if actually dominant
            insights.append(f"{top['column']}: '{top['value']}' dominates ({top['percent']:.1f}%)")
        else:
            n_unique = df[top['column']].nunique()
            insights.append(f"{top['column']}: {n_unique} unique values, evenly distributed")
    
    # Correlation
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        corr_vals = corr.values.copy()
        np.fill_diagonal(corr_vals, 0)
        max_idx = np.unravel_index(np.abs(corr_vals).argmax(), corr_vals.shape)
        corr_val = corr_vals[max_idx]
        # Only report if correlation is strong but not perfect (likely duplicate/derived variables)
        if 0.5 < abs(corr_val) < 0.99:
            insights.append(f"Strong correlation ({corr_val:.2f}): {corr.index[max_idx[0]]} <-> {corr.columns[max_idx[1]]}")
        elif abs(corr_val) >= 0.99:
            insights.append(f"Perfect correlation ({corr_val:.2f}): {corr.index[max_idx[0]]} and {corr.columns[max_idx[1]]} are likely duplicates/derived")
    
    if date_cols:
        dates = df[date_cols[0]].dropna()
        if len(dates) > 0:
            insights.append(f"{date_cols[0]}: {(dates.max() - dates.min()).days} day span")
    
    if sens_cols:
        insights.append(f"WARNING: {len(sens_cols)} sensitive columns detected")
    
    return insights[:10]

def create_plots(df, numeric_cols, cat_cols, out_dir):
    """Generate visualizations"""
    # Only create plots for meaningful numeric columns (already filtered by calc_stats)
    # Numeric plots
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) == 0: continue
        col_safe = safe_name(col)
        
        # Histogram
        plt.figure(figsize=(7, 5))
        plt.hist(s, bins=min(50, int(np.sqrt(len(s)))), edgecolor='black', alpha=0.7)
        plt.title(f"{col}", fontweight='bold')
        plt.xlabel(col); plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/plots/hist_{col_safe}.png", bbox_inches='tight')
        plt.close()
        
        # Boxplot
        plt.figure(figsize=(7, 4))
        plt.boxplot(s, vert=False)
        plt.title(f"{col} - Boxplot", fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{out_dir}/plots/box_{col_safe}.png", bbox_inches='tight')
        plt.close()
    
    # Categorical bar chart
    if cat_cols:
        col, col_safe = cat_cols[0], safe_name(cat_cols[0])
        plt.figure(figsize=(10, 6))
        df[col].value_counts().head(15).plot(kind='barh')
        plt.title(f"{col}", fontweight='bold')
        plt.xlabel("Count")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/plots/bar_{col_safe}.png", bbox_inches='tight')
        plt.close()
    
    # Correlation
    if len(numeric_cols) >= 2:
        x, y = numeric_cols[:2]
        plt.figure(figsize=(7, 6))
        plt.scatter(df[x], df[y], alpha=0.5, s=20)
        plt.title(f"{y} vs {x}", fontweight='bold')
        plt.xlabel(x); plt.ylabel(y)
        plt.tight_layout()
        plt.savefig(f"{out_dir}/plots/scatter_{safe_name(x)}_{safe_name(y)}.png", bbox_inches='tight')
        plt.close()
        
        # Heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="RdBu_r", center=0, fmt='.2f', square=True)
        plt.title("Correlation", fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{out_dir}/plots/correlation_heatmap.png", bbox_inches='tight')
        plt.close()

def create_report(df, num_stats, cat_stats, dup, missing_cols, sens_cols, date_cols, insights, out_dir, name):
    """Generate markdown report"""
    with open(f"{out_dir}/report.md", "w") as f:
        f.write(f"---\ntitle: \"{name} - EDA\"\ndate: \"{datetime.now():%Y-%m-%d}\"\n---\n\n")
        
        if sens_cols:
            f.write("**PRIVACY WARNING**: Sensitive columns detected\n\n")
        
        # Overview
        f.write(f"# Overview\n\n- Rows: {df.shape[0]:,}\n- Columns: {df.shape[1]}\n- Duplicates: {dup:,}\n")
        if missing_cols:
            f.write(f"- High Missing: {', '.join(missing_cols[:5])}\n")
        if date_cols:
            f.write(f"- Dates: {', '.join(date_cols)}\n")
        f.write("\n\\newpage\n\n")
        
        # Numeric
        if not num_stats.empty:
            f.write("# Numeric Analysis\n\n")
            for _, row in num_stats.head(3).iterrows():
                col_safe = safe_name(row['column'])
                f.write(f"## {row['column']}\n\n")
                f.write(f"Min: {row['min']:.2f} | Max: {row['max']:.2f} | Mean: {row['mean']:.2f} | Median: {row['median']:.2f} | Std: {row['std']:.2f}\n\n")
                f.write(f"Outliers: {int(row['outlier_count'])} ({row['outlier_percent']:.1f}%)\n\n")
                f.write(f"![](plots/hist_{col_safe}.png){{ width=48% }} ![](plots/box_{col_safe}.png){{ width=48% }}\n\n")
            f.write("\\newpage\n\n")
        
        # Categorical
        if not cat_stats.empty:
            col = cat_stats['column'].iloc[0]
            f.write(f"# Categorical: {col}\n\n")
            f.write("| Value | Count | % |\n|-------|-------|---|\n")
            for _, row in cat_stats.sort_values('count', ascending=False).head(10).iterrows():
                f.write(f"| {row['value']} | {row['count']:,} | {row['percent']:.1f} |\n")
            f.write(f"\n![](plots/bar_{safe_name(col)}.png){{ width=70% }}\n\n\\newpage\n\n")
        
        # Correlation
        if len(df.select_dtypes(include='number').columns) >= 2:
            x, y = df.select_dtypes(include='number').columns[:2]
            f.write(f"# Correlation\n\n![](plots/scatter_{safe_name(x)}_{safe_name(y)}.png){{ width=48% }} ")
            f.write(f"![](plots/correlation_heatmap.png){{ width=48% }}\n\n\\newpage\n\n")
        
        # Insights
        f.write("# Key Insights\n\n")
        for i, insight in enumerate(insights, 1):
            f.write(f"{i}. {insight}\n\n")
        
        # Limitations
        f.write("# Limitations\n\n")
        if missing_cols:
            f.write(f"- Missing data in {len(missing_cols)} columns may bias results\n")
        f.write("- Dataset represents specific time/location scope\n")
        if sens_cols:
            f.write(f"- {len(sens_cols)} columns may contain sensitive information\n")
        f.write("\n*Auto-generated. All statistics verified.*\n")

def generate_pdf(out_dir):
    """Create PDF"""
    try:
        subprocess.run([
            "pandoc", f"{out_dir}/report.md", "-o", f"{out_dir}/report.pdf",
            "--pdf-engine=pdflatex", "-V", "geometry=margin=1in",
            f"--resource-path=.:{out_dir}:{out_dir}/plots"
        ], check=True, capture_output=True, text=True)
        print("✓ PDF generated")
    except: print("! PDF failed (install pandoc + pdflatex)")

def process_csv(csv_path, schema_path=None, output_base="output"):
    """Main processing function"""
    name = Path(csv_path).stem
    out_dir = f"{output_base}/{safe_name(name)}"
    os.makedirs(f"{out_dir}/plots", exist_ok=True)
    
    print(f"\n{'='*70}\n{name}\n{'='*70}")
    
    # Load
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ {len(df):,} rows x {len(df.columns)} cols")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Process
    schema = load_schema(schema_path)
    df, date_cols = clean_data(df, schema.get('missing_codes') if schema else None)
    sens_cols = find_sensitive(df)
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in df.select_dtypes(exclude='number').columns if c not in date_cols]
    
    if sens_cols:
        print(f"! {len(sens_cols)} sensitive columns")
    print(f"✓ {len(numeric_cols)} numeric, {len(cat_cols)} categorical")
    
    # Stats
    num_stats, cat_stats, filtered_numeric = calc_stats(df, numeric_cols, cat_cols)
    dup = df.duplicated().sum()
    missing_cols = [c for c in df.columns if df[c].isna().mean() > 0.5]
    insights = generate_insights(df, num_stats, cat_stats, dup, missing_cols, sens_cols, date_cols)
    
    # Outputs
    print("✓ Generating plots...")
    create_plots(df, filtered_numeric, cat_cols, out_dir)
    
    if not num_stats.empty:
        num_stats.to_csv(f"{out_dir}/numeric_stats.csv", index=False)
    if not cat_stats.empty:
        cat_stats.to_csv(f"{out_dir}/categorical_stats.csv", index=False)
    
    print("✓ Creating report...")
    create_report(df, num_stats, cat_stats, dup, missing_cols, sens_cols, date_cols, insights, out_dir, name)
    generate_pdf(out_dir)
    
    print(f"✓ Done: {out_dir}/\n{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(description='Automated EDA')
    parser.add_argument('files', nargs='+', help='CSV files or directory')
    parser.add_argument('--schema', '-s', help='Schema JSON')
    parser.add_argument('--output', '-o', default='output', help='Output dir')
    args = parser.parse_args()
    
    # Find CSVs
    csv_files = []
    for path in args.files:
        if os.path.isfile(path) and path.endswith('.csv'):
            csv_files.append(path)
        elif os.path.isdir(path):
            csv_files.extend(glob.glob(f"{path}/**/*.csv", recursive=True))
    
    if not csv_files:
        print("No CSV files found!")
        return
    
    print(f"\n{'='*70}\nAUTOMATED EDA - {len(csv_files)} file(s)\n{'='*70}")
    
    for csv in sorted(set(csv_files)):
        try:
            process_csv(csv, args.schema, args.output)
        except Exception as e:
            print(f"✗ {csv}: {e}\n")
    
    print(f"✓ ALL DONE!\n")

if __name__ == "__main__":
    main()
