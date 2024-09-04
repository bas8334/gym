import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Titel van de app
st.title('Data verzenden naar een Webhook')

# Aantal rijen en kolommen
num_rows = 15
num_cols = 4

# Creëer een lege DataFrame met de juiste afmetingen
data = pd.DataFrame('', index=range(num_rows), columns=[f'Kolom {i+1}' for i in range(num_cols)])

# Naam_sporter invoerveld
naam_sporter = st.text_input('Naam van de sporter', value='')

# Haal de huidige datum op in de vorm dd-mm-yyyy
datum_vandaag = datetime.now().strftime('%d-%m-%Y')

# Maak invoervelden voor elke cel in de tabel
for i in range(num_rows):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        data.iloc[i, j] = cols[j].text_input(f'Rij {i+1} - Kolom {j+1}', value='', key=f'input_{i}_{j}')

# URL van de webhook
webhook_url = st.text_input('Voer de Webhook URL in', 'https://example.com/webhook')

# Verzendknop
if st.button('Verzend Data'):
    # Converteer de DataFrame naar een lijst van dicts (rijen)
    payload = data.to_dict(orient='records')
    
    # Voeg Naam_sporter en datum toe aan het payload
    extra_data = {
        'Naam_sporter': naam_sporter if naam_sporter else None,  # Stuur Null als de naam_sporter leeg is
        'Datum': datum_vandaag
    }
    
    payload.append(extra_data)
    
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
