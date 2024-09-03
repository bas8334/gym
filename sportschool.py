import streamlit as st
import requests

# Titel van de app
st.title('Data verzenden naar een Webhook')

# Input velden voor de kolommen
col1 = st.text_input('Vul data in voor Kolom 1')
col2 = st.text_input('Vul data in voor Kolom 2')

# URL van de webhook
webhook_url = st.text_input('Voer de Webhook URL in', 'https://example.com/webhook')

# Verzendknop
if st.button('Verzend Data'):
    # Maak een payload met de data
    payload = {
        "kolom1": col1,
        "kolom2": col2
    }
    
    # Verstuur de data naar de webhook
    response = requests.post(webhook_url, json=payload)
    
    # Toon de response status
    if response.status_code == 200:
        st.success('Data succesvol verzonden! 😊')
    else:
        st.error(f'Er is iets misgegaan. Statuscode: {response.status_code}')
