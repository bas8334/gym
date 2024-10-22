import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Functie om data uit een Google Sheet te halen
def get_google_sheet_data(spreadsheet_id, sheet_name, api_key):
    # Construct the URL for the Google Sheets API
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A1:Z?alt=json&key={api_key}'

    try:
        # Maak een GET-verzoek om data op te halen
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse de JSON-response
        data = response.json()

        # Haal de rijen op
        rows = data.get('values', [])

        # Converteer naar DataFrame, gebruik de eerste rij als headers
        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0])  # Gebruik de eerste rij als headers
            st.write("Kolommen in de DataFrame:", df.columns.tolist())  # Print de kolomnamen voor controle
            return df
        else:
            st.error("Geen data gevonden in de Google Sheet.")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Fout bij het ophalen van data: {e}")
        return None

# Functie om de unieke oefeningen uit een pandas DataFrame te halen
def get_unique_oefeningen(df):
    if 'Oefening' in df.columns:
        return df['Oefening'].unique().tolist()
    else:
        return []

# Functie om de meest recente regel op te halen voor een specifieke oefening
def get_last_entry_for_exercise(df, exercise):
    # Filter op de specifieke oefening
    oefening_df = df[df['Oefening'] == exercise]
    
    if not oefening_df.empty:
        # Converteer de Datum kolom naar datetime met het formaat 'dd-mm-yyyy'
        oefening_df['Datum'] = pd.to_datetime(oefening_df['Datum'], format='%d-%m-%Y', errors='coerce')
        
        # Sorteer op datum (nieuwste eerst) en haal de meest recente rij op
        meest_recente = oefening_df.sort_values('Datum', ascending=False).iloc[0]
        return meest_recente
    return None

# Titel van de app
st.title('Data verzenden naar een Webhook')

# Haal de secrets op vanuit Streamlit secrets
spreadsheet_id = st.secrets["spreadsheet_id"]
sheet_name = st.secrets["sheet_name"]
api_key = st.secrets["api_key"]

# Haal data uit de Google Sheet
df = get_google_sheet_data(spreadsheet_id, sheet_name, api_key)

# Controleer of de data geladen is en haal unieke oefeningen op
if df is not None:
    unique_oefeningen = get_unique_oefeningen(df)
else:
    unique_oefeningen = []

# Voeg een lege optie toe om standaard geen oefening te selecteren
unique_oefeningen.insert(0, "Selecteer een oefening")
unique_oefeningen.insert(1, "Anders, namelijk...")

# Aantal rijen en kolommen
num_rows = 10
num_cols = 6

# Definieer de kolomnamen
kolom_namen = ['Oefening', 'Set 1 (aantal x KG)', 'Set 2 (aantal x KG)', 'Set 3 (aantal x KG)', 'Set 4 (aantal x KG)', 'Set 5 (aantal x KG)']

# Creëer een lege DataFrame met de juiste kolomnamen en het juiste aantal rijen
data = pd.DataFrame('', index=range(num_rows), columns=kolom_namen)

# Naam_sporter invoerveld
naam_sporter = st.text_input('Naam van de sporter', value='')

# Maak invoervelden voor elke cel in de tabel zonder rij-benaming
for i in range(num_rows):
    cols = st.columns(num_cols)
    
    # Maak een selectbox voor oefeningen met een lege standaardoptie
    selectie = cols[0].selectbox(f'Kies een oefening {i+1}', unique_oefeningen, key=f'select_oefening_{i}')
    
    # Als de gebruiker kiest voor vrije invoer ("Anders, namelijk..."), laat een tekstinvoerveld zien
    if selectie == "Anders, namelijk...":
        oefening_keuze = cols[0].text_input("Voer je eigen oefening in", key=f'oefening_input_{i}')
    elif selectie == "Selecteer een oefening":
        oefening_keuze = None  # Geen oefening geselecteerd
    else:
        oefening_keuze = selectie
        # Haal de meest recente sessie op voor de geselecteerde oefening
        last_entry = get_last_entry_for_exercise(df, oefening_keuze)
        
        # Als er een vorige sessie is, laat de sets van de vorige keer zien
        if last_entry is not None:
            st.write(f"De vorige keer deed je '{oefening_keuze}' op {last_entry['Datum'].strftime('%d-%m-%Y')} met de volgende sets:")
            for j in range(1, 6):
                kolom_naam = f'Set {j} (aantal x KG)'
                if kolom_naam in last_entry and pd.notna(last_entry[kolom_naam]):
                    st.write(f"Set {j}: {last_entry[kolom_naam]}")
        else:
            st.write(f"Geen eerdere data gevonden voor '{oefening_keuze}'.")

    # Sla de geselecteerde of ingevoerde oefening op in de data
    data.iloc[i, 0] = oefening_keuze
    
    # Maak tekstinvoer voor de sets
    for j in range(1, num_cols):
        data.iloc[i, j] = cols[j].text_input(f'{kolom_namen[j]}', value='', key=f'input_{i}_{j}')

# URL van de webhook
webhook_url = st.text_input('Voer de Webhook URL in', 'https://cloud.activepieces.com/api/v1/webhooks/gxHbhWT3mdrd8des1W8yA')

# Verzendknop
if st.button('Verzend Data'):
    # Vervang lege strings ('') met None zodat ze als lege waarden worden behandeld
    data = data.applymap(lambda x: None if x == '' else x)
    
    # Filter de rijen waarbij de kolom 'Oefening' niet leeg is en er een waarde is ingevuld
    filtered_data = data[data['Oefening'].notna() & (data['Oefening'] != 'Selecteer een oefening')].copy()

    # Voeg Naam_sporter en Datum kolommen toe aan de gefilterde DataFrame
    filtered_data['Naam_sporter'] = naam_sporter if naam_sporter else None
    filtered_data['Datum'] = datetime.now().strftime('%d-%m-%Y')

    # Verzend alleen als er gegevens zijn
    if not filtered_data.empty:
        payload = filtered_data.to_dict(orient='records')

        # Verstuur de data naar de webhook
        try:
            response = requests.post(webhook_url, json=payload)
            
            # Toon de response status
            if response.status_code == 200:
                st.success('Data succesvol verzonden! 😊')
            else:
                st.error(f'Er is iets misgegaan. Statuscode: {response.status_code}, Response: {response.text}')
        
        except requests.exceptions.RequestException as e:
            st.error(f'Verzoek mislukt: {e}')
    else:
        st.warning('Er is geen data om te verzenden.')
