import streamlit as st
import json
import os

st.set_page_config(
    page_title="SkillSwap",
    page_icon="🤝",
    layout="wide"
)

DATA_FILE = "skillswap_data.json"


# ---------- DATA STORAGE ----------

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {"profiles": []}

    return {"profiles": []}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def parse_skills(text):
    return [
        skill.strip().title()
        for skill in text.split(",")
        if skill.strip()
    ]


data = load_data()


# ---------- SIDEBAR NAVIGATION ----------

st.sidebar.title("🤝 SkillSwap")
st.sidebar.write("Learn together. Grow together.")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Create Profile",
        "Partner Preferences",
        "Recommendations"
    ]
)


# ---------- HOME PAGE ----------

if page == "Home":

    st.title("🤝 Welcome to SkillSwap!")

    st.subheader(
        "Share What You Know. Learn What You Love."
    )

    st.write(
        "SkillSwap connects students who want to exchange "
        "skills, teach each other, and learn together."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📚 Teach")
        st.write(
            "Share your knowledge and help other students."
        )

    with col2:
        st.subheader("🎯 Learn")
        st.write(
            "Discover skills and learn from fellow students."
        )

    with col3:
        st.subheader("🤝 Connect")
        st.write(
            "Find learning partners with matching skills."
        )

    st.divider()

    st.info(
        "Get started by selecting 'Create Profile' "
        "from the sidebar."
    )

    st.metric(
        "Registered Profiles",
        len(data["profiles"])
    )


# ---------- CREATE PROFILE ----------

elif page == "Create Profile":

    st.title("👤 Create Your Profile")

    st.write(
        "Tell us about yourself, your skills, "
        "and your learning preferences."
    )

    with st.form("profile_form"):

        st.subheader("Basic Information")

        name = st.text_input("What's your name?")

        course = st.text_input(
            "What's your college course?"
        )

        year = st.selectbox(
            "Which year are you in?",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )

        about = st.text_area(
            "Tell us about yourself (optional)"
        )

        st.divider()

        st.subheader("📚 Your Skills")

        teach_text = st.text_input(
            "Skills you can teach",
            placeholder="Python, Drawing, Mathematics"
        )

        learn_text = st.text_input(
            "Skills you want to learn",
            placeholder="Java, Web Development, Excel"
        )

        level = st.selectbox(
            "Your current learning level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        st.divider()

        st.subheader("🧠 Learning Preferences")

        speed = st.selectbox(
            "Your preferred learning speed",
            [
                "Slow",
                "Moderate",
                "Fast"
            ]
        )

        style = st.selectbox(
            "How do you prefer to learn?",
            [
                "Practical",
                "Theory",
                "Both"
            ]
        )

        daily_time = st.selectbox(
            "How much time can you give daily?",
            [
                "15–30 minutes",
                "30–60 minutes",
                "1+ hour"
            ]
        )

        availability = st.selectbox(
            "When are you available?",
            [
                "Morning",
                "Afternoon",
                "Evening",
                "Flexible"
            ]
        )

        mode = st.selectbox(
            "Preferred learning mode",
            [
                "Online",
                "In person",
                "Either"
            ]
        )

        submitted = st.form_submit_button(
            "Save Profile"
        )

    if submitted:

        teach_skills = parse_skills(teach_text)
        learn_skills = parse_skills(learn_text)

        if not name.strip():
            st.error("Please enter your name.")

        elif not teach_skills:
            st.error(
                "Please enter at least one skill you can teach."
            )

        elif not learn_skills:
            st.error(
                "Please enter at least one skill you want to learn."
            )

        else:

            profile = {
                "name": name.strip(),
                "course": course.strip(),
                "year": year,
                "about": about.strip(),
                "teach": teach_skills,
                "learn": learn_skills,
                "level": level,
                "speed": speed,
                "style": style,
                "daily_time": daily_time,
                "availability": availability,
                "mode": mode,
                "partner_preferences": {
                    "speed": "Any",
                    "style": "Any",
                    "availability": "Any",
                    "mode": "Any",
                    "year": "Any"
                }
            }

            # Update the profile if this name already exists
            existing_index = next(
                (
                    i for i, old_profile
                    in enumerate(data["profiles"])
                    if old_profile["name"].lower()
                    == name.strip().lower()
                ),
                None
            )

            if existing_index is None:
                data["profiles"].append(profile)
            else:
                data["profiles"][existing_index] = profile

            save_data(data)

            st.success(
                "Your profile has been saved successfully! 🎉"
            )

            st.write("### Your Profile Summary")

            st.write("**Name:**", profile["name"])

            st.write(
                "**Skills you can teach:**",
                ", ".join(profile["teach"])
            )

            st.write(
                "**Skills you want to learn:**",
                ", ".join(profile["learn"])
            )

            st.info(
                "Next, open Partner Preferences from the sidebar."
            )


# ---------- PARTNER PREFERENCES ----------

elif page == "Partner Preferences":

    st.title("🤝 Your Ideal Learning Partner")

    if not data["profiles"]:

        st.warning(
            "Please create a profile before setting preferences."
        )

    else:

        profile_names = [
            profile["name"]
            for profile in data["profiles"]
        ]

        selected_name = st.selectbox(
            "Select your profile",
            profile_names
        )

        profile_index = profile_names.index(selected_name)

        profile = data["profiles"][profile_index]

        preferences = profile["partner_preferences"]

        with st.form("partner_preferences_form"):

            st.subheader("Partner Preferences")

            partner_speed = st.selectbox(
                "Preferred teaching speed",
                [
                    "Any",
                    "Slow",
                    "Moderate",
                    "Fast"
                ],
                index=[
                    "Any",
                    "Slow",
                    "Moderate",
                    "Fast"
                ].index(preferences.get("speed", "Any"))
            )

            partner_style = st.selectbox(
                "Preferred teaching style",
                [
                    "Any",
                    "Practical",
                    "Theory",
                    "Both"
                ],
                index=[
                    "Any",
                    "Practical",
                    "Theory",
                    "Both"
                ].index(preferences.get("style", "Any"))
            )

            partner_availability = st.selectbox(
                "Preferred availability",
                [
                    "Any",
                    "Morning",
                    "Afternoon",
                    "Evening",
                    "Flexible"
                ],
                index=[
                    "Any",
                    "Morning",
                    "Afternoon",
                    "Evening",
                    "Flexible"
                ].index(
                    preferences.get("availability", "Any")
                )
            )

            partner_mode = st.selectbox(
                "Preferred learning mode",
                [
                    "Any",
                    "Online",
                    "In person",
                    "Either"
                ],
                index=[
                    "Any",
                    "Online",
                    "In person",
                    "Either"
                ].index(preferences.get("mode", "Any"))
            )

            partner_year = st.selectbox(
                "Preferred college year",
                [
                    "Any",
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                ],
                index=[
                    "Any",
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                ].index(preferences.get("year", "Any"))
            )

            save_preferences = st.form_submit_button(
                "Save Preferences"
            )

        if save_preferences:

            profile["partner_preferences"] = {
                "speed": partner_speed,
                "style": partner_style,
                "availability": partner_availability,
                "mode": partner_mode,
                "year": partner_year
            }

            save_data(data)

            st.success(
                "Your partner preferences have been saved! 🎉"
            )


# ---------- RECOMMENDATIONS ----------

elif page == "Recommendations":

    st.title("✨ Learning Partner Recommendations")

    if len(data["profiles"]) < 2:

        st.info(
            "At least two student profiles are needed "
            "to find potential learning partners."
        )

    else:

        profile_names = [
            profile["name"]
            for profile in data["profiles"]
        ]

        selected_name = st.selectbox(
            "View recommendations for",
            profile_names
        )

        current_index = profile_names.index(selected_name)

        current = data["profiles"][current_index]

        preferences = current.get(
            "partner_preferences",
            {}
        )

        recommendations = []

        for index, candidate in enumerate(data["profiles"]):

            if index == current_index:
                continue

            candidate_teach = [
                skill.lower()
                for skill in candidate["teach"]
            ]

            candidate_learn = [
                skill.lower()
                for skill in candidate["learn"]
            ]

            # Find skills the candidate can teach the current student
            matching_skills = [
                skill
                for skill in current["learn"]
                if skill.lower() in candidate_teach
            ]

            if not matching_skills:
                continue

            score = 50

            reasons = [
                "Can teach: " + ", ".join(matching_skills)
            ]

            # Check for mutual skill exchange
            mutual_skills = [
                skill
                for skill in current["teach"]
                if skill.lower() in candidate_learn
            ]

            if mutual_skills:
                score += 20

                reasons.append(
                    "Mutual exchange: " + ", ".join(mutual_skills)
                )

            # Compare partner preferences
            comparisons = [
                ("speed", "speed"),
                ("style", "style"),
                ("availability", "availability"),
                ("mode", "mode"),
                ("year", "year")
            ]

            for preference_key, profile_key in comparisons:

                preferred = preferences.get(
                    preference_key,
                    "Any"
                )

                actual = candidate.get(profile_key, "")

                if preferred == "Any":
                    score += 2

                elif preferred == actual:
                    score += 5

                elif (
                    preference_key == "mode"
                    and preferred == "Either"
                ):
                    score += 5

                elif (
                    preference_key == "availability"
                    and actual == "Flexible"
                ):
                    score += 5

            recommendations.append(
                (score, candidate, reasons)
            )

        recommendations.sort(
            key=lambda result: result[0],
            reverse=True
        )

        if not recommendations:

            st.warning(
                "No matching partners found yet. "
                "Try adding more student profiles."
            )

        else:

            for score, partner, reasons in recommendations:

                with st.container(border=True):

                    st.subheader(
                        "👤 " + partner["name"]
                    )

                    st.write(
                        "**Course:**",
                        partner["course"] or "Not specified"
                    )

                    st.write(
                        "**College year:**",
                        partner["year"]
                    )

                    st.write(
                        "**Can teach:**",
                        ", ".join(partner["teach"])
                    )

                    st.write(
                        "**Wants to learn:**",
                        ", ".join(partner["learn"])
                    )

                    st.write(
                        "**Availability:**",
                        partner["availability"]
                    )

                    st.write(
                        "**Learning style:**",
                        partner["style"]
                    )

                    st.write("**Why this is a potential match:**")

                    for reason in reasons:
                        st.write("•", reason)

                    st.caption(
                        f"Compatibility score: {score}"
                    )


# ---------- FOOTER ----------

st.sidebar.divider()

st.sidebar.caption(
    "SkillSwap | Learn together, grow together 🤝"
)