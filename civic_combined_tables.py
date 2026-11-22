"""
CivicGuide AI - Combined Small Schemes & Services Tables Generator (Python)
--------------------------------------------------------------------------
Generates clean, compact, combined tables for:
  1. Central Government Schemes (10 schemes)
  2. State Government Schemes (Karnataka and other states)
  3. All Combined Government Schemes (47 schemes)
  4. Public Service Centers Directory (56 centers)

Usage:
  python civic_combined_tables.py                 # Display all 3 small combined tables
  python civic_combined_tables.py --scope central # Display Central Government table
  python civic_combined_tables.py --scope state   # Display State Government table (Karnataka)
  python civic_combined_tables.py --scope all     # Display All Combined schemes table
  python civic_combined_tables.py --export        # Export all tables to CSV & HTML
"""

import os
import sys
import argparse
import importlib.util
import pandas as pd

def load_data():
    """Load verified schemes and services data from git-tracked modules."""
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load Schemes
    schemes_path = os.path.join(curr_dir, "backend", "app", "utils", "all_india_schemes_data.py")
    spec = importlib.util.spec_from_file_location("all_india_schemes_data", schemes_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    schemes = mod.ALL_INDIA_SCHEMES

    # 2. Load Services
    services_path = os.path.join(curr_dir, "backend", "app", "utils", "all_india_services_data.py")
    spec2 = importlib.util.spec_from_file_location("all_india_services_data", services_path)
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    services = mod2.ALL_PUBLIC_SERVICES

    return schemes, services

def get_central_schemes_table(schemes, compact=True):
    """Table 1: Central Government Schemes (10 schemes)"""
    central = [s for s in schemes if "central" in (s.get("government_level") or "").lower()]
    rows = []
    for idx, s in enumerate(central, 1):
        rows.append({
            "#": idx,
            "Scheme Name": s.get("name"),
            "Sector": s.get("category"),
            "Government Level": "🏛️ Central Government",
            "Key Direct Benefit": (s.get("benefits")[:75] + "...") if compact else s.get("benefits"),
            "Official Portal": s.get("official_url")
        })
    return pd.DataFrame(rows)

def get_state_schemes_table(schemes, state="Karnataka", compact=True):
    """Table 2: State Government Schemes (Filtered by State)"""
    state_schemes = [
        s for s in schemes
        if "central" not in (s.get("government_level") or "").lower() and
           (state.lower() in (s.get("state") or "").lower() or state.lower() in (s.get("government_level") or "").lower())
    ]
    rows = []
    for idx, s in enumerate(state_schemes, 1):
        rows.append({
            "#": idx,
            "Scheme Name": s.get("name"),
            "Sector": s.get("category"),
            "State / Region": f"📍 {s.get('state', state)}",
            "Key Direct Benefit": (s.get("benefits")[:75] + "...") if compact else s.get("benefits"),
            "Official Portal": s.get("official_url")
        })
    return pd.DataFrame(rows)

def get_all_combined_table(schemes, compact=True):
    """Table 3: All Combined Government Schemes (47 schemes)"""
    rows = []
    for idx, s in enumerate(schemes, 1):
        is_central = "central" in (s.get("government_level") or "").lower()
        level_str = "🏛️ Central" if is_central else f"📍 {s.get('state', 'State')}"
        rows.append({
            "#": idx,
            "Scheme Name": s.get("name"),
            "Sector": s.get("category"),
            "Level / State": level_str,
            "Key Direct Benefit": (s.get("benefits")[:75] + "...") if compact else s.get("benefits"),
            "Official Portal": s.get("official_url")
        })
    return pd.DataFrame(rows)

def print_table(title, df):
    """Print compact, beautiful ASCII table to console."""
    print("\n" + "=" * 80)
    print(f" {title} (Total: {len(df)})")
    print("=" * 80)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 60)
    print(df.to_string(index=False))
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="CivicGuide AI - Small Combined Tables")
    parser.add_argument("--scope", choices=["central", "state", "all", "every"], default="every",
                        help="Which table to generate (central, state, all, or every)")
    parser.add_argument("--state", default="Karnataka", help="State for state-specific schemes table")
    parser.add_argument("--export", action="store_true", help="Export tables to CSV and HTML files")
    args = parser.parse_args()

    schemes, services = load_data()

    df_central = get_central_schemes_table(schemes)
    df_state = get_state_schemes_table(schemes, state=args.state)
    df_all = get_all_combined_table(schemes)

    if args.scope in ["central", "every"]:
        print_table("TABLE 1: 🏛️ CENTRAL GOVERNMENT SCHEMES", df_central)

    if args.scope in ["state", "every"]:
        print_table(f"TABLE 2: 📍 STATE GOVERNMENT SCHEMES ({args.state.upper()})", df_state)

    if args.scope in ["all", "every"]:
        print_table("TABLE 3: 🇮🇳 ALL COMBINED GOVERNMENT SCHEMES (CENTRAL + STATES)", df_all)

    if args.export:
        out_csv = "combined_schemes_small_table.csv"
        out_html = "combined_schemes_small_table.html"
        df_all.to_csv(out_csv, index=False)
        
        # Build clean compact HTML table
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>CivicGuide AI • Small Combined Government Schemes Tables</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 20px; background: #f8fafc; color: #0f172a; }}
        h1 {{ color: #064e3b; margin-bottom: 5px; }}
        h2 {{ color: #047857; margin-top: 30px; font-size: 1.25rem; border-bottom: 2px solid #a7f3d0; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; }}
        th {{ background: #064e3b; color: #fff; text-align: left; padding: 8px 10px; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
        td {{ padding: 7px 10px; border-bottom: 1px solid #e2e8f0; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        tr:hover {{ background-color: #ecfdf5; }}
        a {{ color: #059669; font-weight: bold; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; }}
        .badge-central {{ background: #eff6ff; color: #1e3a8a; border: 1px solid #bfdbfe; }}
        .badge-state {{ background: #fef3c7; color: #78350f; border: 1px solid #fde68a; }}
    </style>
</head>
<body>
    <h1>🏛️ CivicGuide AI — Combined Government Schemes Directory</h1>
    <p>Compact All-India Verified Schemes Tables for Central & State Governments.</p>
    
    <h2>1. 🏛️ Central Government Schemes ({len(df_central)} Schemes)</h2>
    {df_central.to_html(index=False, render_links=True, escape=False)}

    <h2>2. 📍 {args.state} State Government Schemes ({len(df_state)} Schemes)</h2>
    {df_state.to_html(index=False, render_links=True, escape=False)}

    <h2>3. 🇮🇳 All Combined Government Schemes ({len(df_all)} Schemes)</h2>
    {df_all.to_html(index=False, render_links=True, escape=False)}
</body>
</html>"""
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"\n✅ Exported compact tables successfully to:")
        print(f"   - CSV:  {out_csv}")
        print(f"   - HTML: {out_html}")

if __name__ == "__main__":
    main()
