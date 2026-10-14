"""
Smart Campus Analytics & Student Success Platform
Layout & Design System Component — Injects brand styling, typography, cards, and badges.
"""

import streamlit as st


def inject_custom_styles() -> None:
    """Injects global CSS design tokens and component styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        :root {
            --color-bg: #F5F7FB;
            --color-surface: #FFFFFF;
            --color-text: #172033;
            --color-muted: #667085;
            --color-border: #E4E7EC;
            --color-primary: #3B5BDB;
            --color-primary-soft: #EEF2FF;
            --color-success: #16803C;
            --color-success-soft: #EAF7EE;
            --color-warning: #B54708;
            --color-warning-soft: #FFF4E5;
            --color-danger: #B42318;
            --color-danger-soft: #FEECEB;
            --radius-card: 14px;
            --radius-control: 9px;
            --shadow-card: 0 2px 10px rgba(16, 24, 40, 0.05);
            --space-page: 24px;
            --space-card: 18px;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: var(--color-text);
        }

        .stApp {
            background-color: var(--color-bg);
        }

        /* Top Banner & Header */
        .app-header {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            color: white;
            padding: 24px 28px;
            border-radius: var(--radius-card);
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
        }

        .app-header h1 {
            color: #FFFFFF !important;
            font-size: 26px !important;
            font-weight: 700 !important;
            margin: 0 0 6px 0 !important;
            padding: 0 !important;
            letter-spacing: -0.5px;
        }

        .app-header p {
            color: #94A3B8 !important;
            font-size: 14px !important;
            margin: 0 !important;
        }

        .demo-notice {
            display: inline-block;
            background-color: #FEF3C7;
            color: #92400E;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 8px;
        }

        /* Metric Cards */
        .kpi-container {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }

        .kpi-card {
            background: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-card);
            padding: 20px 22px;
            box-shadow: var(--shadow-card);
            flex: 1;
            min-width: 200px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .kpi-card:hover {
            box-shadow: 0 6px 16px rgba(16, 24, 40, 0.08);
        }

        .kpi-title {
            color: var(--color-muted);
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        .kpi-value {
            color: var(--color-text);
            font-size: 28px;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 6px;
        }

        .kpi-subtitle {
            color: var(--color-muted);
            font-size: 12px;
            font-weight: 500;
        }

        /* Content Surfaces / Sections */
        .analytics-card {
            background: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-card);
            padding: var(--space-card);
            box-shadow: var(--shadow-card);
            margin-bottom: 20px;
        }

        .section-title {
            color: var(--color-text);
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
        }

        .badge-success { background-color: var(--color-success-soft); color: var(--color-success); }
        .badge-warning { background-color: var(--color-warning-soft); color: var(--color-warning); }
        .badge-danger { background-color: var(--color-danger-soft); color: var(--color-danger); }
        .badge-info { background-color: var(--color-primary-soft); color: var(--color-primary); }
        .badge-neutral { background-color: #F2F4F7; color: var(--color-muted); }

        /* Action Recommendation Box */
        .recommendation-box {
            background-color: #F8FAFC;
            border-left: 4px solid var(--color-primary);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
        }

        /* Streamlit overrides */
        div[data-testid="stSidebarNav"] {
            padding-top: 10px;
        }

        .stButton>button {
            border-radius: var(--radius-control);
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, icon: str = "🎓") -> None:
    """Renders standardized page header with synthetic demo indicator."""
    st.markdown(
        f"""
        <div class="app-header">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h1>{icon} {title}</h1>
                    <p>{subtitle}</p>
                </div>
                <div>
                    <span class="demo-notice">⚡ Synthetic Demo Dataset (HacXLerate 2026)</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
