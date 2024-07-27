import streamlit as st
import pickle
import pandas as pd

# List of teams and cities
teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

# Load the prediction model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Set the title of the Streamlit app
st.title('🏏 IPL Win Predictor 🏆')

# Add a brief description with enhanced styling
st.write("""
    **Welcome to the IPL Win Predictor!**  
    Select the batting and bowling teams, choose the host city, and input the match statistics to predict the probability of each team winning the match. 🌟
""")

# Create two columns for team selection with colorful headers
col1, col2 = st.columns(2)

with col1:
    st.subheader('**Batting Team 🎯**')
    batting_team = st.selectbox('', sorted(teams), key='batting_team')
with col2:
    st.subheader('**Bowling Team 🎳**')
    bowling_team = st.selectbox('', sorted(teams), key='bowling_team')

# Select the host city with a styled dropdown
st.subheader('**Host City 🌆**')
selected_city = st.selectbox('', sorted(cities), key='city')

# Input the target score with an enhanced look
st.subheader('**Match Details 📊**')
target = st.number_input('**Target Score**', min_value=0, step=1, key='target')

# Create three columns for match statistics with labels
col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('**Current Score**', min_value=0, step=1, key='score')
with col4:
    overs = st.number_input('**Overs Completed**', min_value=0.0, step=0.1, format="%.1f", key='overs')
with col5:
    wickets = st.number_input('**Wickets Out**', min_value=0, step=1, key='wickets')

# Prediction button with enhanced styling
if st.button('🔮 Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    remaining_wickets = 10 - wickets
    crr = score / overs if overs != 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left != 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [remaining_wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    # Get the prediction probabilities
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    # Display the prediction results with colored headers and emojis
    st.markdown(f"""
        <div style='background-color: #f0f8ff; padding: 10px; border-radius: 5px;'>
            <h2 style='color: #2e8b57;'>{batting_team} 🌟 - {round(win * 100)}%</h2>
        </div>
        <div style='background-color: #fff0f5; padding: 10px; border-radius: 5px;'>
            <h2 style='color: #ff4500;'>{bowling_team} 💔 - {round(loss * 100)}%</h2>
        </div>
    """, unsafe_allow_html=True)
