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
    "Workout 2": [
        "Barbell Bench Press",
        "Romanian Deadlift",
        "Lat Pulldown",
        "Glute-Focused Walking Lunges",
        "Superset: Side Delts And Abs"
    ],
    "Workout 3": [
        "Seated Dumbbell Shoulder Press",
        "Lat-Focused Dumbbell Row",
        "Hip Thrust",
        "Leg Extensions",
        "Chest Flyes",
        "Superset: Calves And Rear Delts"
    ]
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

Both options create a deep stretch, a powerful driver for muscle growth.""",
"Barbell Bench Press": """First up, we’re hitting the chest again, but this time focusing on the mid and lower chest with the barbell bench press for 3 sets of 4-6 reps. 

Now, we used to think that lower reps were only for building strength, 6-12 reps were ideal for muscle growth, and higher reps were best for endurance.

But research has shown that all of these rep ranges can lead to similar muscle growth — as long as you’re pushing hard. 

So why go with lower reps here? 

Heavier weight in the lower rep range not only builds muscle but also comes with the added bonus of boosting strength.

And for the bench press, going heavy can be a lot of fun, especially if you’ve got a spotter to keep things safe. That said, if heavy benching bothers your shoulders, no worries.

You can lighten the load and aim for higher reps or swap it out for the flat dumbbell press, which is often easier on the joints.""",
"Romanian Deadlift": """Next up in Workout 2 of our full body workout plan, we’re working the hamstrings with Romanian deadlifts for 3 sets of 6-8 reps.

Back in Workout 1, we focused on one function of the hamstrings — knee flexion — which has also been shown to activate the lower part of the hamstrings more.

Romanian deadlifts, however, focus on the other main function: hip extension.

This shift also seems to activate the upper hamstrings more, making it the perfect combo for overall development. But with the Romanian Deadlift, proper technique is key to avoid just overworking your lower back:

Start with a shoulder-width stance and grip the bar just outside your knees.
Brace your core, and then imagine a band around your hips pulling you back. This will naturally bend your torso towards the floor.
Keep your knees relatively straight and let the bar slide along your thighs as you continue pushing your hips back. 
But once your hips can’t push back any further, stop — going any lower will only round your lower back. This end point will vary for everyone. If you’ve got longer arms, you’ll be able to get closer to the floor. With shorter arms, you might stop just past your knees. Both are perfectly fine, so don’t force it.
On the way up, drive your hips forward, then repeat for the next rep.""",
"Lat Pulldown": """Next up in our full body workout program, lat pulldowns for 3 sets of 8-12 reps.

Despite the name, lat pulldowns don’t actually work your lats very well.

The wider bar forces your elbows to flare out, engaging more of your upper and outer back muscles. 

This is perfectly fine, so don’t be worried if you can’t feel your lats all that much, as we’ll be focusing on them in Workout 3 of our full body workout routine. 

Use a fairly wide grip here, lean back slightly, and pull the bar towards your upper chest.

And lastly, don’t forget the technique from Workout 1: on your last set, push past failure by doing as many full reps as you can, then extend your set with 3-5 half reps in the stretched position to squeeze out extra growth.""",
"Glute-Focused Walking Lunges": """Next up in our full body workout program, we’re back to the lower body to target the glutes with 3 sets of walking lunges, aiming for about 6-10 reps per leg. 

The secret to making this glute-focused is all in the setup.

Take a wide step forward, keep your knee directly over your foot, and lean your torso forward slightly while keeping your back straight. This creates a deeper stretch in the glutes.

Switch legs with each step and focus on controlling the descent — your back knee should hover just above the ground at the bottom of each rep.""",
"Superset: Side Delts And Abs": """o finish up Workout 2 of our full body workout routine, we’ve got another isolation exercise superset.

This time with the side delts and abs. 

For the side delts, I’d recommend behind the body cable lateral raise with the cables set up 3-4 notches up from the bottom. This not only gives your side delts a deep stretch but challenges them more in that stretched position.

After you’re done, we’ll immediately go into an ab exercise: reverse crunches. 

While your abs help stabilize your body in many of your compound exercises, training them directly can help build them up just like any other muscle, which visibly can make them pop more. 

Reverse crunches are a great choice here because they challenge your abs a little more when they’re stretched. 

Lay on a bench or on a mat and bend your legs to 90 degrees.
Then, raise your hips by moving your knees toward your chest, focusing on curling your pelvis. Even if it’s just lifting your tailbone, go as far as you can.
Then slowly control the way down.
Repeat this superset for a total of 3 times.""",
"Seated Dumbbell Shoulder Press": """First up in Workout 3 of our full body workout program, we have the seated dumbbell shoulder press for 3 sets of 8-12 reps, which will mainly target the front part of your shoulders. 

I personally prefer using dumbbells over barbells for this movement because they’re easier on the joints. 

Plus, by setting the bench 1-2 notches down from fully upright, you’ll reduce the demand on your shoulder mobility while still getting the most out of the exercise. 

Lastly, as you press, to maximize shoulder activation, let your elbows flare out to the sides, but as you lower the dumbbells, tuck them slightly in front of your body.""",
"Lat-Focused Dumbbell Row": """Next up, we’ve emphasized almost every area of the back in the previous workouts of our full body workout program, but there’s 1 major part left: the lats. 

This is where the dumbbell row comes in, with 3 sets of 8-12 reps. 

Start by placing your same-side hand and knee on a bench for support while planting your other leg far out for stability. 

Next, the key to activating your lats is to keep your elbow tight to your side as you row and focus on driving your elbow back towards your hips in a sweeping, arcing motion, almost like you’re "sweeping the floor" with the weight. 

But to prevent your biceps from taking over, make sure your forearm stays vertical rather than curling the weight as you pull. 
Lastly, as you row, avoid rotating your torso to make the movement easier.

Keep your back flat, pull until your elbow reaches your torso, and then control the weight back down. 

And don’t forget. On your last set, push past failure by doing as many half-reps as you can in the stretched position to maximize growth.""",
"Hip Thrust": """Next up, our first lower body exercise in Workout 3 of our full body workout routine: 3 sets of 10-15 reps of hip thrusts. 

Hip thrusts have been shown to grow the glutes just as much as squats and, in this study, even led to almost double the glute growth when added to a leg workout (9.1% vs 5.9%). 

And if you sit most of the day, this is a must to avoid “flat butt syndrome.” 

Now, one big mistake is arching your back, which puts pressure on your lower back instead of the glutes.

To fix this, brace your core as if someone’s about to punch your stomach, then squeeze your glutes hard. Think about holding a $100 bill between your cheeks — don’t let me steal it.

At the top, your back should be flat, and your glutes should be burning. 

But if I’m being honest, sometimes I just don’t feel like going through all the effort to set up hip thrusts.

So an effective swap are dumbbell step-ups on a bench or platform. But just like we did with walking lunges in Workout 2 of our full body workout routine, lean forward slightly to target the glutes more, and alternate legs each step.""",
"Leg Extensions": """To finish off the quads for the week, we’re doing 3 sets of 10-15 reps of leg extensions. 

While pressing movements like the squat are great for overall quad growth, research suggests they only really grow just 3 of the 4 quad muscles.

The 4th quad muscle, the rectus femoris, because of its unique anatomy, is instead better grown with leg extensions, hence why I’ve added them to this full body workout routine.  

But if you want even more growth from this exercise, if your machine lets you, lean back as you perform it.

This stretches out the rectus femoris and has been shown to significantly boost growth compared to the normal version.""",
"Chest Flyes": """Next up in Workout 3 of our full body workout program, we’re working the chest with 3 sets of 10-15 reps of flyes to compliment the pressing we’ve done earlier in the week.

My preferred setup is a seated cable fly with a pad or foam roller between my back and the bench for a deeper stretch in the chest.

Another option is the pec deck, but the downside is it tends to be much harder in the “squeeze”.

So, to make up for it,  just like we did with the back exercises throughout the week, at the end of your very last set do as many half reps as you can in that all important stretched position.""",
"Superset: Calves And Rear Delts": """Alright, to finish off the week and our full body workout routine, we’ve got our final isolation superset, starting with calf raises.

Your calves are made up of 2 muscles, and we used to think seated calf raises target one better while standing hits the other.

But when researchers tested this, they found something surprising.

Seated calf raises do grow that one muscle well, but standing calf raises grow it just as much, while also growing the other calf muscle significantly more.

So for maximum growth, standing calf raises are the way to go.

You can do these on a leg press machine, smith machine, or single leg with a dumbbell on any platform. Anything where your legs stay straight.

And here’s the key: pause at the bottom of each rep for a deep stretch.

For calves, this stretch is one of the most important drivers of growth.

Once you’re done, move straight into reverse cable flyes to target the rear delts, a part of the shoulder that often gets overlooked.

Set the cables slightly above shoulder height, grab the left cable with your right hand and the right cable with your left hand, and sweep your arms outward. Let your arms cross over at the start for a deeper stretch in the rear delts.

Repeat this superset for a total of 3 sets to wrap up your week of training (and week of full body workout routine).""",
}

# Functie om data uit Google Sheets te halen
# Afbeeldingen per oefening
exercise_images = {
    "Incline Dumbbell Press": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-incline-dumbbell-press-1536x864.webp",
    "Barbell Squats": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-barbell-squats-1536x864.webp",
    "Dumbbell Chest Supported Row": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-dumbbell-chest-supported-row-form-1536x864.webp",
    "Leg Curls": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-leg-curls-1536x864.webp",
    "Superset: Biceps And Triceps": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-1-superset-option-2-1536x864.webp",
    "Barbell Bench Press": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-2-barbell-bench-press-1536x864.webp",
    "Romanian Deadlift": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-2-romanian-deadlifts-1536x864.webp",
    "Lat Pulldown": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-2-lat-pulldowns-1536x864.webp",
    "Glute-Focused Walking Lunges": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-2-walking-lunges-1536x864.webp",
    "Superset: Side Delts And Abs": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-2-superset-1536x864.webp",
    "Seated Dumbbell Shoulder Press": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-seated-dumbbell-shoulder-press-1536x864.webp",
    "Lat-Focused Dumbbell Row": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-dumbbell-row-form-1536x864.webp",
    "Hip Thrust": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-hip-thrusts-1536x864.webp",
    "Leg Extensions": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-leg-extensions-1536x864.webp",
    "Chest Flyes": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-chest-flyes-1536x864.webp",
    "Superset: Calves And Rear Delts": "https://builtwithscience.com/wp-content/uploads/2025/01/Full-body-workout-plan-workout-3-superset-1536x864.webp"    
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
