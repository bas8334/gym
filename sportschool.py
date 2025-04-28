import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Workout programma's
programmas = {
    "Workout 1": [
        "Incline Dumbbell Press",
        "Barbell Squats",
        "Dumbbell Chest Supported Row",
        "Leg Curls",
        "Superset: Biceps And Triceps"
    ],
    "Workout 2": [],  # Later toe te voegen
    "Workout 3": []   # Later toe te voegen
}

# Uitleg per oefening
exercise_descriptions = {
    "Incline Dumbbell Press": """To kick off Workout 1 of our full body workout plan, we’ll target the upper chest with the incline dumbbell press for 3 sets of 8-12 reps.

Why start here?

Most people’s upper chest is underdeveloped compared to other areas, yet it plays a huge role in creating a fuller, more balanced chest.

And the incline dumbbell press doesn’t just hit the upper chest; it’s one of the best all-around chest builders.

In fact, a 2020 study found that incline pressing led to similar mid-chest growth as flat bench but was significantly better for the upper chest. That's why it's 1 of the only 2 chest exercises that truly helped grow my chest.

But before jumping in, do a quick warm up to activate your muscles and protect your joints:

Start with 1 light set for 8-10 reps
Increase the weight for 3-5 reps
Do this one more time with a heavy weight for 1-2 reps

This helps you ease into the movement without draining your energy.

But you’ll also want to make sure you get the bench angle right. This can make or break the exercise and depends on your chest structure.

Lay on a flat bench and place your phone between your pecs.

If your phone angles down, you’ve got a steep sternum. In this case, a flat bench acts more like a decline press, so you’ll need a steeper incline (30 to 45 degrees) to hit your upper chest properly.

But if your phone stays relatively flat (flat sternum), you’ve got a flat sternum like me.

In this case, a flat bench works as intended, and a slight incline — just one or two notches up — is all you need. Anything past this and you’ll likely just feel it more in your shoulders.

Finally, to optimize your form, tuck your elbows into an arrow shape on the way down and press the dumbbells up and back toward your collarbone. This lines up the tension perfectly with your upper chest fibers.""",

    "Barbell Squats": """Next in our full body workout plan, we’re moving to the lower body with squats for 3 sets of 6-8 reps.

Follow the same warm-up protocol we used for the incline dumbbell press to get your leg muscles ready.

The barbell squat has been getting some hate online recently, with people claiming it’s not “optimal.”

But in a full body workout, you want exercises that give you the most bang for your buck. And squats do just that.

Research shows they don’t just grow the glutes as effectively as glute-focused exercises like hip thrusts, they also strengthen and grow the quads, adductors, and even your lower back.

It’s essentially 4 exercises in 1, which is why it deserves a spot in this full body workout routine.

That said, not everyone’s body is built to squat the same way.

If you’re like Max and struggle to squat deep, try elevating your heels on plates. This simple adjustment will allow you to stay more upright, shifting more of the focus to your quads.""",

    "Dumbbell Chest Supported Row": """Next in the full body workout routine, we’re focusing on the mid and upper back muscles with the dumbbell chest-supported row for 3 sets of 8-12 reps.

Adjust an incline bench to 45 degrees and lie chest-down on it with your legs slightly bent and feet firmly planted.

Key points:
- Keep your elbows angled out in an arrow shape as you pull.
- At the top, squeeze your shoulder blades together.
- Let them fully open up at the bottom.

If your forearms bend upward, your biceps are taking over. Keep your forearm straight up and down.

Bonus technique: After hitting failure, do 3-5 partial reps at the bottom.""",

    "Leg Curls": """We’re heading back to the lower body to target the hamstrings, for 3 sets of 10-15 reps.

One of the hamstring muscles only crosses the knee, so to fully develop them, you need both a curl and a hip-extension movement.

Today we focus on leg curls.

Seated leg curls (if available) are better than lying curls for hamstring growth due to the greater stretch.

Form tip: Avoid fully straightening your legs at the start of each rep to minimize calf involvement.""",

    "Superset: Biceps And Triceps": """Final 2 exercises: focus on biceps and triceps, often neglected by compound lifts.

Option 1 (dumbbells): Incline dumbbell curls superset with dumbbell overhead extensions.

Option 2 (cables): Behind-the-body cable curls superset with overhead rope extensions.

Both options create a deep stretch, a powerful driver for muscle growth."""
}

# Functie om data uit Google Sheets te halen
# Afbeeldingen per oefening
exercise_images = {
    "Incline Dumbbell Press": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-incline-dumbbell-press-1536x864.webp",
    "Barbell Squats": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-barbell-squats-1536x864.webp",
    "Dumbbell Chest Supported Row": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-dumbbell-chest-supported-row-form-1536x864.webp",
    "Leg Curls": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-leg-curls-1536x864.webp",
    "Superset: Biceps And Triceps": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-superset-option-2-1536x864.webp"
}

# Functie om data uit Google Sheets te halen
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

st.title("Workout Logger")
naam_sporter = st.text_input("Naam van de sporter")

# Tabs voor programma's
tabs = st.tabs(list(programmas.keys()))

log_data = []
df_columns = df.columns.tolist() if not df.empty else []

for tab, programma_naam in zip(tabs, programmas.keys()):
    with tab:
        st.header(f"{programma_naam}")
        oefeningen = programmas[programma_naam]

        for oef in oefeningen:
            # Toon afbeelding boven de expander
            if oef in exercise_images:
                st.image(exercise_images[oef], use_container_width=True)

            with st.expander(oef):
                st.markdown(exercise_descriptions.get(oef, "Geen uitleg beschikbaar."))
            
            sets = []
            cols = st.columns(5)
            for i in range(5):
                sets.append(cols[i].text_input(f"Set {i+1} (#xKG)", key=f"{programma_naam}_{oef}_set_{i}"))

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
