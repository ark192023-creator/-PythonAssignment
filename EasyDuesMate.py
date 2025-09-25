import streamlit as st
import pandas as pd
from datetime import datetime
import io
import math

# Try to import plotly; if unavailable, fall back to Streamlit's built-in charts
try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

# Page configuration
st.set_page_config(
    page_title="Easy Dues Mate 💰",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------
# Custom CSS (cleaner + more robust)
# --------------------
st.markdown(
    """
    <style>
        :root {
            --card-bg: rgba(255,255,255,0.95);
            --muted: #666666;
        }

        .stApp {
            background: linear-gradient(135deg, #7b61ff 0%, #b388ff 100%);
            min-height: 100vh;
            padding: 1rem 0;
        }

        .main-header {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: 0.6px;
            margin-bottom: 0.25rem;
            color: white;
        }

        .subtitle {
            text-align: center;
            color: rgba(255,255,255,0.95);
            margin-bottom: 1.2rem;
        }

        .metric-card, .person-card {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        }

        .stButton > button {
            border-radius: 999px;
            padding: 0.6rem 1.6rem;
            font-weight: 700;
        }

        /* make side panel a little translucent for better contrast */
        .css-1d391kg, .css-1oe6wy4 {
            background: rgba(255,255,255,0.95);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------
# Session state initialization (safe)
# --------------------
if 'people' not in st.session_state:
    st.session_state.people = []
if 'calculations_done' not in st.session_state:
    st.session_state.calculations_done = False
if 'last_num_people' not in st.session_state:
    st.session_state.last_num_people = None

# --------------------
# Header
# --------------------
st.markdown('<div class="main-header">💰 Easy Dues Mate</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Split expenses fairly among friends — dinner, trips or everyday sharing</div>', unsafe_allow_html=True)

# --------------------
# Sidebar: inputs
# --------------------
with st.sidebar:
    st.header("🎯 Expense Details")

    total_amount = st.number_input(
        "💵 Total Amount (₹)",
        min_value=0.0,
        max_value=10_000_000.0,
        value=2500.0,
        step=1.0,
        help="Enter the total expense amount in Indian Rupees",
        format="%.2f"
    )

    num_people = st.number_input(
        "👥 Number of People",
        min_value=1,
        max_value=200,
        value=3,
        step=1,
        help="How many people are splitting this expense?"
    )

    st.divider()
    st.subheader("🔧 Advanced Options")
    use_names = st.checkbox("Add person names", value=True)
    use_contributions = st.checkbox("Track individual contributions", value=True)

    # Adjust session-state people list length only when number changed
    if st.session_state.last_num_people is None or num_people != st.session_state.last_num_people:
        # Preserve existing entries wherever possible
        old = st.session_state.people
        new = []
        for i in range(num_people):
            if i < len(old):
                new.append({
                    'name': old[i].get('name', f'Person {i+1}'),
                    'contribution': float(old[i].get('contribution', 0.0))
                })
            else:
                new.append({'name': f'Person {i+1}', 'contribution': 0.0})
        st.session_state.people = new
        st.session_state.last_num_people = num_people
        st.session_state.calculations_done = False

    st.subheader("👤 Person Details")

    # Inputs for each person
    for i in range(num_people):
        with st.container():
            cols = st.columns([2, 1])
            if use_names:
                name_val = cols[0].text_input(
                    f"Name {i+1}", value=st.session_state.people[i].get('name', f'Person {i+1}'), key=f"name_{i}", label_visibility="collapsed"
                )
                st.session_state.people[i]['name'] = name_val.strip() if isinstance(name_val, str) else f'Person {i+1}'
            else:
                # keep existing name or reset to default
                st.session_state.people[i]['name'] = st.session_state.people[i].get('name', f'Person {i+1}')

            if use_contributions:
                contrib_val = cols[1].number_input(
                    f"Paid (₹)", min_value=0.0, max_value=total_amount * 10, value=float(st.session_state.people[i].get('contribution', 0.0)), step=1.0, key=f"contrib_{i}", label_visibility="collapsed", format="%.2f"
                )
                st.session_state.people[i]['contribution'] = float(contrib_val)
            else:
                st.session_state.people[i]['contribution'] = float(st.session_state.people[i].get('contribution', 0.0))

            st.markdown("---")

    st.divider()

    if st.button("🗑️ Clear All", help="Reset all data"):
        st.session_state.people = [{'name': f'Person {i+1}', 'contribution': 0.0} for i in range(1)]
        st.session_state.calculations_done = False
        st.experimental_rerun()

# --------------------
# Main: validation, calculate and display
# --------------------
try:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Basic validation
        errors = []
        if total_amount <= 0:
            errors.append("Total amount must be greater than 0.")
        if num_people < 1:
            errors.append("Number of people must be at least 1.")

        if errors:
            for e in errors:
                st.error(e)

        if use_contributions:
            total_contributions = sum(float(p.get('contribution', 0.0)) for p in st.session_state.people[:int(num_people)])
            if total_contributions == 0:
                st.info("💡 Tip: Add individual contributions to see who owes/gets back what.")

        can_calculate = (len(errors) == 0)

        if st.button("🧮 Calculate Split", use_container_width=True, disabled=not can_calculate):
            st.session_state.calculations_done = True

        if st.session_state.calculations_done and can_calculate:
            # Calculate equal share and per-person results
            equal_share = round(float(total_amount) / int(num_people), 2)
            results = []
            total_contributions = 0.0

            for i in range(int(num_people)):
                person = st.session_state.people[i] if i < len(st.session_state.people) else {'name': f'Person {i+1}', 'contribution': 0.0}
                name = person.get('name', f'Person {i+1}') if use_names else f'Person {i+1}'
                contribution = float(person.get('contribution', 0.0)) if use_contributions else 0.0

                balance = round(contribution - equal_share, 2)
                total_contributions += contribution

                if balance < -0.01:
                    status = 'owes'
                elif balance > 0.01:
                    status = 'gets_back'
                else:
                    status = 'balanced'

                results.append({
                    'name': name,
                    'contribution': round(contribution, 2),
                    'equal_share': equal_share,
                    'balance': balance,
                    'status': status
                })

            # Summary metrics
            st.subheader("📊 Summary")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 Total Amount", f"₹{float(total_amount):,.2f}")
            m2.metric("👥 People", f"{int(num_people)}")
            m3.metric("⚖️ Equal Share", f"₹{equal_share:,.2f}")

            if use_contributions:
                diff = round(total_contributions - float(total_amount), 2)
                m4.metric("💳 Total Paid", f"₹{total_contributions:,.2f}", delta=(f"₹{diff:,.2f}" if abs(diff) > 0.01 else None))
            else:
                m4.metric("💳 Total Paid", "Not tracked")

            st.divider()

            # Individual breakdown (UI)
            st.subheader("👤 Individual Breakdown")
            for p in results:
                # pick styling based on status
                if p['status'] == 'owes':
                    emoji = '💸'
                    status_text = f"OWES ₹{abs(p['balance']):,.2f}"
                elif p['status'] == 'gets_back':
                    emoji = '💰'
                    status_text = f"GETS BACK ₹{p['balance']:,.2f}"
                else:
                    emoji = '✅'
                    status_text = 'ALL SETTLED'

                c1, c2, c3 = st.columns([1, 3, 1])
                with c2:
                    st.markdown(f"""
                        <div class="person-card">
                            <h4 style='margin: 0'>{emoji} {p['name']}</h4>
                            <div style='color: var(--muted); margin-top:8px;'>
                                <strong>Equal Share:</strong> ₹{p['equal_share']:,.2f}
                                {f"<br><strong>Contributed:</strong> ₹{p['contribution']:,.2f}" if use_contributions else ""}
                            </div>
                            <div style='margin-top:12px; font-weight:700;'>
                                {status_text}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Contribution mismatch warning
            if use_contributions and abs(total_contributions - float(total_amount)) > 0.01:
                diff = round(total_contributions - float(total_amount), 2)
                if diff > 0:
                    st.warning(f"⚠️ Contributions exceed total by ₹{diff:,.2f}")
                else:
                    st.warning(f"⚠️ Contributions are short by ₹{abs(diff):,.2f}")

            # Suggested settlements
            st.subheader("💡 Settlement Tips")
            owes = [r.copy() for r in results if r['status'] == 'owes']
            gets = [r.copy() for r in results if r['status'] == 'gets_back']

            if use_contributions and owes and gets:
                owes_sorted = sorted(owes, key=lambda x: abs(x['balance']), reverse=True)
                gets_sorted = sorted(gets, key=lambda x: x['balance'], reverse=True)

                settlements = []
                i, j = 0, 0
                # operate on copies
                while i < len(owes_sorted) and j < len(gets_sorted):
                    o = owes_sorted[i]
                    g = gets_sorted[j]
                    amount = round(min(abs(o['balance']), g['balance']), 2)
                    if amount <= 0:
                        break
                    settlements.append(f"{o['name']} → {g['name']}: ₹{amount:,.2f}")

                    o['balance'] += amount
                    g['balance'] -= amount

                    if abs(o['balance']) < 0.01:
                        i += 1
                    if g['balance'] < 0.01:
                        j += 1

                for s in settlements:
                    st.write(f"• {s}")

                # allow export of suggested settlements
                if settlements:
                    settlements_txt = "\n".join(settlements)
                    st.download_button("⬇️ Download Settlements (TXT)", data=settlements_txt, file_name=f"settlements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                if not use_contributions:
                    st.info("Enter contributions to see suggested settlements.")
                elif not owes and not gets:
                    st.success("🎉 Everyone is settled! No payments needed.")

            # Download full results as CSV
            df_results = pd.DataFrame(results)
            csv_bytes = df_results.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Detailed Results (CSV)", data=csv_bytes, file_name=f"dues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime='text/csv')

    # Right column: visualizations
    with col2:
        st.subheader("📈 Visual Breakdown")

        if st.session_state.calculations_done and can_calculate:
            # Prepare viz data
            viz = []
            for r in results:
                if abs(r['balance']) > 0.01:
                    viz.append({'Person': (r['name'][:15] + '...') if len(r['name']) > 15 else r['name'], 'Amount': abs(r['balance']), 'Type': ('Owes' if r['status']=='owes' else 'Gets Back')})

            if viz:
                df_viz = pd.DataFrame(viz)
                # If Plotly available, use it; otherwise fallback
                if HAS_PLOTLY:
                    fig = px.bar(df_viz, x='Person', y='Amount', color='Type', text='Amount', title='Who Owes What?')
                    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
                    fig.update_layout(height=380, plot_bgcolor='rgba(255,255,255,0.9)', paper_bgcolor='rgba(255,255,255,0.9)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # simple fallback
                    st.write("(Plotly not available — showing a simple chart)")
                    pivot = df_viz.pivot_table(index='Person', values='Amount', aggfunc='sum')
                    st.bar_chart(pivot)

            # Pie chart for contributions
            if use_contributions and results:
                contribs = [{'Person': r['name'], 'Contribution': r['contribution']} for r in results if r['contribution'] > 0]
                if contribs:
                    df_contrib = pd.DataFrame(contribs)
                    if HAS_PLOTLY:
                        fig_pie = px.pie(df_contrib, names='Person', values='Contribution', title='Contribution Distribution')
                        fig_pie.update_layout(height=300)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.write(df_contrib.set_index('Person'))

except Exception as ex:
    st.error(f"An unexpected error occurred: {ex}")
    st.info("Try refreshing the page. If the problem persists please share the debug info below.")

# Footer + tips
st.divider()
st.markdown(
    """
    <div style='text-align:center; padding:1rem; background: rgba(255,255,255,0.9); border-radius:10px;'>
        <p style='margin:0'>💡 <strong>Pro Tip:</strong> Use the downloads to share results with your group.</p>
        <p style='margin:0; font-size:0.9rem;'>Made with ❤️ for fair expense splitting — Version 2.1</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Debug info (development only)
if st.checkbox("🔧 Show Debug Info"):
    st.subheader("Debug Information")
    st.write("Session State:", st.session_state)
    st.write("People (len):", len(st.session_state.people))
    st.write("Num people expected:", num_people)
