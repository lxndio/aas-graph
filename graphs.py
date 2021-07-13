import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import io

algorithms = {
    "BNDM": "bndm",
    "BOM": "bom",
    "BLIM": "blim",
    "Double Window": "dw",
    "Horspool": "horspool",
    "Naive": "naive",
    "KMP": "kmp",
    "Classic KMP": "kmp-classic",
    "Shift-And": "shift-and",
    "Weak Boyer Moore": "wbm",
    "Weak Memorizing Boyer Moore": "wmbm",
    "Weak Turbo Boyer Moore": "wtbm"
}
textSources = {
    "Randomly Generated": "--tr",
    "File": "--tf"
}
patternSources = {
    "Fixed Position in Text": "--pt",
    "Random Position in Text": "--prt",
    "Argument": "--pa",
    "File": "--pf",
    "Randomly Generated": "--pr"
}

st.sidebar.header("Algorithms")
st.sidebar.multiselect("Algorithms", list(algorithms.keys()), key="algorithms")
st.sidebar.header("Text Source")
st.sidebar.selectbox("Text Source", list(textSources.keys()), key="textSource")

if st.session_state.textSource == "Randomly Generated":
    st.sidebar.number_input("Text Length", key="textLength", min_value=1, step=1)
    runTextSourceParameter = str(st.session_state.textLength)
elif st.session_state.textSource == "File":
    st.sidebar.text_input("Text File Path", key="textFile")
    runTextSourceParameter = st.session_state.textFile

st.sidebar.header("Pattern Source")
st.sidebar.checkbox("Multiple Patterns", key="patternMultiple")

lstPatternSources = list(patternSources.keys())

if st.session_state.patternMultiple:
    lstPatternSources.remove("Fixed Position in Text")

st.sidebar.selectbox("Pattern Source", lstPatternSources, key="patternSource")

if st.session_state.patternSource == "Fixed Position in Text":
    st.sidebar.number_input("From", key="patternFrom", min_value=1, step=1)
    st.sidebar.number_input("To", key="patternTo", min_value=int(st.session_state.patternFrom + 1), step=1)
    st.sidebar.number_input("Step Size", key="patternStepSize", min_value=1, step=1)
    runPatternSourceParameter = str(st.session_state.patternFrom) + '..' + str(st.session_state.patternTo) + ',' + str(st.session_state.patternStepSize)
elif st.session_state.patternSource == "Random Position in Text":
    if not st.session_state.patternMultiple:
        st.sidebar.number_input("Pattern Length", key="patternLength", min_value=1, step=1)
        runPatternSourceParameter = str(st.session_state.patternLength)
    else:
        st.sidebar.number_input("From", key="patternFrom", min_value=1, step=1)
        st.sidebar.number_input("To", key="patternTo", min_value=int(st.session_state.patternFrom + 1), step=1)
        st.sidebar.number_input("Step Size", key="patternStepSize", min_value=1, step=1)
        runPatternSourceParameter = str(st.session_state.patternFrom) + '..' + str(st.session_state.patternTo) + ',' + str(st.session_state.patternStepSize)
elif st.session_state.patternSource == "Argument":
    if not st.session_state.patternMultiple:
        st.sidebar.text_input("Pattern", key="pattern")
        runPatternSourceParameter = st.session_state.pattern
    else:
        st.sidebar.text_area("Patterns", key="patterns")
        st.sidebar.write("Enter one pattern per line.")
        # st.session_state.patterns.splitlines()
elif st.session_state.patternSource == "File":
    st.sidebar.text_input("Pattern File Path", key="patternFile")
    runPatternSourceParameter = st.session_state.patternFile
elif st.session_state.patternSource == "Randomly Generated":
    if not st.session_state.patternMultiple:
        st.sidebar.number_input("Pattern Length", key="patternLength", min_value=1, step=1)
        runPatternSourceParameter = str(st.session_state.patternLength)
    else:
        st.sidebar.number_input("From", key="patternFrom", min_value=1, step=1)
        st.sidebar.number_input("To", key="patternTo", min_value=int(st.session_state.patternFrom + 1), step=1)
        st.sidebar.number_input("Step Size", key="patternStepSize", min_value=1, step=1)
        runPatternSourceParameter = str(st.session_state.patternFrom) + '..' + str(st.session_state.patternTo) + ',' + str(st.session_state.patternStepSize)

st.sidebar.header("Other")
st.sidebar.number_input("Executions", key="executions", min_value=1, step=1)

stRun = st.sidebar.button("Run")

if stRun:
    runAlgorithms = ','.join([algorithms[x] for x in st.session_state.algorithms])
    runTextSource = textSources[st.session_state.textSource]
    runPatternSource = patternSources[st.session_state.patternSource]
    runExecutions = str(st.session_state.executions)

    runArguments = ['./aas-benchmark', runAlgorithms, runTextSource, runTextSourceParameter, runPatternSource, runPatternSourceParameter, '-n', runExecutions]

    st.spinner()
    with st.spinner(text="Running aas-benchmark"):
        result = subprocess.run(runArguments, capture_output=True, text=True).stdout
    
    st.session_state.measurements = pd.read_csv(io.StringIO(result), quoting=csv.QUOTE_NONE, dtype={
        'algorithm': str, 'text_length': int, 'pattern_length': int, 'execution': int,
        'matches': int, 'prep_time_ms': int, 'time_ms': int
    })

    st.session_state.chartData = []
    st.session_state.chartData.append(st.session_state.measurements[['algorithm', 'pattern_length', 'time_ms']])

if 'measurements' in st.session_state:
    #st.table(st.session_state.measurements[['algorithm', 'pattern_length', 'time_ms']])

    fig, ax = plt.subplots()
    sns.lineplot(x='pattern_length', y='time_ms', hue='algorithm', data=st.session_state.chartData[0], ci=68, ax=ax)
    st.pyplot(fig)

    col1, col2 = st.beta_columns(2)

    fig, ax = plt.subplots()
    sns.lineplot(x='pattern_length', y='time_ms', hue='algorithm', data=st.session_state.chartData[0], ax=ax)
    col1.pyplot(fig)
