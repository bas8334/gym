import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Workout programma's
programmas = {
    "Push": [
        "Chest Low incline db press",
        "Deficit push up",
        "Seated db lateral raise",
        "Seated overhead tricep extension",
        "Triceps dips",
        "High bar squat",
        "Seated leg curl",
        "Sit-back squat"
    ],
    "Pull": [
        "Barbell Row",
        "Lat prayer",
        "Clown Curl",
        "Incline db curl",
        "Lying skullcrusher",
        "Hack squat",
        "Lying leg curl",
        "Glute thrust Machine"
    ],
    "Legs & Extra": [
        "Flad db fly",
        "Super ROM lateral raise",
        "Cable face pull",
        "Pull up",
        "Free motion \u201csuper man\u201d cable curl",
        "Reverse Nordic curl",
        "Stiff Leg Deadlift",
        "Front foot elevated smith lunge",
        "Standing Calf raise"
    ]
}

# Functie om data uit een Google Sheet te halen
def get_google_sheet_data(spreadsheet_id, sheet_name, api_key):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A1:Z?alt=json&key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rows = data.get('values', [])
        if rows:
            return pd.DataFrame(rows[1:], columns=rows[0])
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# Haal secrets op
spreadsheet_id = st.secrets["spreadsheet_id"]
sheet_name = st.secrets["sheet_name"]
api_key = st.secrets["api_key"]
df = get_google_sheet_data(spreadsheet_id, sheet_name, api_key)

# App UI
st.title("Workout Logger")
naam_sporter = st.text_input("Naam van de sporter")
programma_keuze = st.selectbox("Kies een programma", list(programmas.keys()))
oefeningen = programmas[programma_keuze]

log_data = []

for oef in oefeningen:
    st.subheader(oef)
    vorige = df[(df['Oefening'] == oef) & (df['Naam_sporter'] == naam_sporter)]
    vorige['Datum'] = pd.to_datetime(vorige['Datum'], format='%d-%m-%Y', errors='coerce')
    vorige = vorige.sort_values('Datum', ascending=False).head(1)
    if not vorige.empty:
        st.info(f"Vorige keer ({vorige.iloc[0]['Datum'].strftime('%d-%m-%Y')}): " +
