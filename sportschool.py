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
        "Free motion super man cable curl",
        "Reverse Nordic curl",
        "Stiff Leg Deadlift",
        "Front foot elevated smith lunge",
        "Standing Calf raise"
    ]
}

# Oefening-afbeeldingen (bron: musclewiki.com)
exercise_images = {
    "Chest Low incline db press": "https://musclewiki.com/media/uploads/images/db-incline-press-male-front.gif",
    "Deficit push up": "https://musclewiki.com/media/uploads/images/pushup-male-front.gif",
    "Seated db lateral raise": "https://musclewiki.com/media/uploads/images/dumbbell-lateral-raise-male-front.gif",
    "Seated overhead tricep extension": "https://musclewiki.com/media/uploads/images/dumbbell-overhead-tricep-extension-male-front.gif",
    "Triceps dips": "https://musclewiki.com/media/uploads/images/tricep-dip-male-front.gif",
    "High bar squat": "https://musclewiki.com/media/uploads/images/barbell-squat-male-front.gif",
    "Seated leg curl": "https://musclewiki.com/media/uploads/images/seated-leg-curl-male-side.gif",
    "Sit-back squat": "https://musclewiki.com/media/uploads/images/goblet-squat-male-front.gif",
    "Barbell Row": "https://musclewiki.com/media/uploads/images/barbell-row-male-front.gif",
    "Lat prayer": "https://musclewiki.com/media/uploads/images/cable-straight-arm-pulldown-male-front.gif",
    "Clown Curl": "https://musclewiki.com/media/uploads/images/dumbbell-bicep-curl-male-front.gif",
    "Incline db curl": "https://musclewiki.com/media/uploads/images/incline-dumbbell-curl-male-front.gif",
    "Lying skullcrusher": "https://musclewiki.com/media/uploads/images/barbell-skullcrusher-male-front.gif",
    "Hack squat": "https://musclewiki.com/media/uploads/images/machine-hack-squat-male-side.gif",
    "Lying leg curl": "https://musclewiki.com/media/uploads/images/lying-leg-curl-male-side.gif",
    "Glute thrust Machine": "https://musclewiki.com/media/uploads/images/barbell-hip-thrust-male-side.gif",
    "Flad db fly": "https://musclewiki.com/media/uploads/images/dumbbell-fly-male-front.gif",
    "Super ROM lateral raise": "https://musclewiki.com/media/uploads/images/cable-lateral-raise-male-side.gif",
    "Cable face pull": "https://musclewiki.com/media/uploads/images/cable-face-pull-male-front.gif",
    "Pull up": "https://musclewiki.com/media/uploads/images/pullup-male-front.gif",
    "Free motion super man cable curl": "https://musclewiki.com/media/uploads/images/cable-curl-male-front.gif",
    "Reverse Nordic curl": "https://musclewiki.com/media/uploads/images/nordic-hamstring-curl-male-side.gif",
    "Stiff Leg Deadlift": "https://musclewiki.com/media/uploads/images/barbell-stiff-leg-deadlift-male-side.gif",
    "Front foot elevated smith lunge": "https://musclewiki.com/media/uploads/images/smith-machine-lunge-male-side.gif",
    "Standing Calf raise": "https://musclewiki.com/media/uploads/images/standing-calf-raise-male-side.gif"
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

df_columns = df.columns.tolist() if not df.empty else []

for oef in oefeningen:
    st.subheader(oef)

    # Toon oefening afbeelding indien beschikbaar
    if oef in exercise_images:
        st.image(exercise_images[oef], use_column_width=True)

    if 'Oefening' in df_columns and 'Naam_sporter' in df_columns:
        vorige = df[(df['Oefening'] == oef) & (df['Naam_sporter'] == naam_sporter)]
        vorige['Datum'] = pd.to_datetime(vorige['Datum'], format='%d-%m-%Y', errors='coerce')
        vorige = vorige.sort_values('Datum', ascending=False).head(1)
        if not vorige.empty:
            vorige_sets = []
            for i in range(5):
                set_val = vorige.iloc[0].get(f'Set {i+1} (#xKG)', '-')
                vorige_sets.append(f"Set {i+1}: {set_val}")
            vorige_datum = vorige.iloc[0]['Datum'].strftime('%d-%m-%Y')
            st.info("Vorige keer (" + vorige_datum + "): " + ", ".join(vorige_sets))

    sets = []
    cols = st.columns(5)
    for i in range(5):
        sets.append(cols[i].text_input(f"Set {i+1} (#xKG)", key=f"{oef}_set_{i}"))

    log_data.append({
        "Oefening": oef,
        "Set 1 (#xKG)": sets[0],
        "Set 2 (#xKG)": sets[1],
        "Set 3 (#xKG)": sets[2],
        "Set 4 (#xKG)": sets[3],
        "Set 5 (#xKG)": sets[4],
        "Naam_sporter": naam_sporter,
        "Datum": datetime.now().strftime('%d-%m-%Y')
    })

# Webhook input en verzenden
webhook_url = st.text_input("Webhook URL", "https://cloud.activepieces.com/api/v1/webhooks/gxHbhWT3mdrd8des1W8yA")

if st.button("Verzend data"):
    to_send = [entry for entry in log_data if entry["Oefening"] and naam_sporter]
    if to_send:
        try:
            response = requests.post(webhook_url, json=to_send)
            if response.status_code == 200:
                st.success("Data succesvol verzonden!")
            else:
                st.error(f"Fout bij verzenden: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Verzoek mislukt: {e}")
    else:
        st.warning("Geen data om te verzenden.")
