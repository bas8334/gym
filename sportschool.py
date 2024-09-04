import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Titel van de app
st.title('Data verzenden naar een Webhook')

# Aantal rijen en kolommen
num_rows = 15
num_cols = 6

# Definieer de kolomnamen
kolom_namen = ['Oefening', 'Set 1 (#xKG)', 'Set 2 (#xKG)', 'Set 3 (#xKG)', 'Set 4 (#xKG)', 'Set 5 (#xKG)']

# Creëer een lege DataFrame met de juiste kolomnamen
data = pd.DataFrame('', index=range(num_rows), columns=kolom_namen)

# Naam_sporter invoerveld
naam_sporter = st.text_input('Naam van de sporter', value='')

# Haal de huidige datum op in de vorm dd-mm-yyyy
datum_vandaag = datetime.now().strftime('%d-%m-%Y')

# Maak invoervelden voor elke cel in de tabel zonder rij-benaming
for i in range(num_rows):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        data.iloc[i, j] = cols[j].text_input(f'{kolom_namen[j]}', value='', key=f'input_{i}_{j}')

# URL van de webhook
webhook_url = st.text_input('Voer de Webhook URL in', 'https://example.com/webhook')

# Verzendknop
if st.button('Verzend Data'):
    # Vervang lege waarden met None (Python's equivalent van Null)
    data = data.applymap(lambda x: None if x == '' else x)
    
    # Filter de rijen die ten minste één waarde bevatten
    filtered_data = data.dropna(how='all').copy()

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
