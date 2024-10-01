import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Titel van de app
st.title('Data verzenden naar een Webhook')

# Aantal rijen en kolommen
num_rows = 10
num_cols = 6

# Definieer de kolomnamen
kolom_namen = ['Oefening', 'Set 1 (#xKG)', 'Set 2 (#xKG)', 'Set 3 (#xKG)', 'Set 4 (#xKG)', 'Set 5 (#xKG)']

# Creëer een lege DataFrame met de juiste kolomnamen
data = pd.DataFrame('', index=range(num_rows), columns=kolom_namen)

# Naam_sporter invoerveld
naam_sporter = st.text_input('Naam van de sporter', value='')

# Invoerveld om een nieuwe oefening toe te voegen
nieuwe_oefening = st.text_input('Voeg een nieuwe oefening toe aan de lijst')

# Knop om de oefening op te slaan
if st.button('Sla oefening op'):
    if nieuwe_oefening:
        try:
            # Voeg de nieuwe oefening toe aan het bestand oefeningen.txt
            with open('oefeningen.txt', 'a') as f:
                f.write(f'\n{nieuwe_oefening}')
            st.success(f'Oefening "{nieuwe_oefening}" is toegevoegd!')
        except Exception as e:
            st.error(f'Fout bij het opslaan van de oefening: {e}')
    else:
        st.warning('Voer een oefening in om op te slaan.')

# Haal de huidige datum op in de vorm dd-mm-yyyy
datum_vandaag = datetime.now().strftime('%d-%m-%Y')

# Lees de lijst met oefeningen uit een kladblokbestand
try:
    with open('oefeningen.txt', 'r') as f:
        oefeningen = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    st.error('Het bestand oefeningen.txt is niet gevonden.')
    oefeningen = []

# Voeg een lege optie toe voor de dropdown
oefeningen.insert(0, "")

# Maak invoervelden voor elke cel in de tabel zonder rij-benaming
for i in range(num_rows):
    cols = st.columns(num_cols)
    # Maak de eerste kolom een dropdown voor de oefening
    data.iloc[i, 0] = cols[0].selectbox('Oefening', options=oefeningen, key=f'oefening_{i}')
    
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
    filtered_data['Datum'] = datum_vandaag

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
