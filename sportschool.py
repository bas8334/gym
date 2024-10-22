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

# Voeg een lege optie toe voor de dropdown
unique_oefeningen.insert(0, "")

# Aantal rijen en kolommen
num_rows = 10
num_cols = 6

# Definieer de kolomnamen
kolom_namen = ['Oefening', 'Set 1 (#xKG)', 'Set 2 (#xKG)', 'Set 3 (#xKG)', 'Set 4 (#xKG)', 'Set 5 (#xKG)']

# Creëer een lege DataFrame met de juiste kolomnamen en het juiste aantal rijen
data = pd.DataFrame('', index=range(num_rows), columns=kolom_namen)

# Naam_sporter invoerveld
naam_sporter = st.text_input('Naam van de sporter', value='')

# Maak invoervelden voor elke cel in de tabel zonder rij-benaming
for i in range(num_rows):
    cols = st.columns(num_cols)
    # Maak de eerste kolom een dropdown voor de oefening met unieke oefeningen
    data.iloc[i, 0] = cols[0].selectbox('Oefening', options=unique_oefeningen, key=f'oefening_{i}')
    
    # Maak tekstinvoer voor de sets
    for j in range(1, num_cols):
        data.iloc[i, j] = cols[j].text_input(f'{kolom_namen[j]}', value='', key=f'input_{i}_{j}')

# URL van de webhook
webhook_url = st.text_input('Voer de Webhook URL in', 'https://example.com/webhook')

# Verzendknop
if st.button('Verzend Data'):
    # Vervang lege strings ('') met None zodat ze als lege waarden worden behandeld
    data = data.applymap(lambda x: None if x == '' else x)
    
    # Filter de rijen waarbij de kolom 'Oefening' niet leeg is
    filtered_data = data[data['Oefening'].notna()].copy()

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
