import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns

algorithms = ["Naive", "Horspool", "BNDM"]
textSources = ["Randomly Generated", "File"]
patternSources = ["Fixed Position in Text", "Random Position in Text", "Argument", "File", "Randomly Generated"]

st.sidebar.header("Algorithms")
st.sidebar.multiselect("Algorithms", algorithms, key="algorithms")
st.sidebar.header("Text Source")
st.sidebar.selectbox("Text Source", textSources, key="textSource")

if st.session_state.textSource == "Randomly Generated":
    st.sidebar.number_input("Text Length", key="textLength", min_value=1, step=1)
elif st.session_state.textSource == "File":
    st.sidebar.file_uploader("Text File", key="textFile")

st.sidebar.header("Pattern Source")
st.sidebar.selectbox("Pattern Source", patternSources, key="patternSource")

if st.session_state.patternSource == "Fixed Position in Text":
    st.sidebar.number_input("From", key="patternFrom", min_value=1, step=1)
    st.sidebar.number_input("To", key="patternTo", min_value=int(st.session_state.patternFrom + 1), step=1)
    st.sidebar.number_input("Step Size", key="patternStepSize", min_value=1, step=1)
elif st.session_state.patternSource == "Random Position in Text":
    st.sidebar.number_input("Pattern Length", key="patternLength", min_value=1, step=1)
elif st.session_state.patternSource == "Argument":
    st.sidebar.text_input("Pattern", key="pattern")
elif st.session_state.patternSource == "File":
    st.sidebar.file_uploader("Pattern File", key="patternFile")
elif st.session_state.patternSource == "Randomly Generated":
    st.sidebar.number_input("Pattern Length", key="patternLength", min_value=1, step=1)

st.sidebar.header("Other")
st.sidebar.number_input("Executions", key="executions", min_value=1, step=1)

stRun = st.sidebar.button("Run")

fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [1, 2, 3])
st.pyplot(fig)