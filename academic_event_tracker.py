import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Academic Calendar & Event Tracker", layout="wide")

st.title("📅 Academic Calendar & Event Tracker Dashboard")

# Initialize or load data
def load_data():
    try:
        df = pd.read_csv("events.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Event Name", "Date", "Description", "Status"])
    return df

def save_data(df):
    df.to_csv("events.csv", index=False)

df = load_data()

# Sidebar - Add new event
st.sidebar.header("➕ Add New Event")
event_name = st.sidebar.text_input("Event Name")
event_date = st.sidebar.date_input("Date")
event_description = st.sidebar.text_area("Description")
event_status = st.sidebar.selectbox("Status", ["Upcoming", "Completed", "Missed"])

if st.sidebar.button("Add Event"):
    new_event = pd.DataFrame({
        "Event Name": [event_name],
        "Date": [event_date],
        "Description": [event_description],
        "Status": [event_status]
    })
    df = pd.concat([df, new_event], ignore_index=True)
    save_data(df)
    st.sidebar.success("Event added successfully!")

# Main dashboard
st.subheader("📘 All Events")
st.dataframe(df)

# Filter events
st.subheader("🔍 Filter by Status")
filter_option = st.selectbox("Choose status to filter:", ["All", "Upcoming", "Completed", "Missed"])
if filter_option != "All":
    filtered_df = df[df["Status"] == filter_option]
else:
    filtered_df = df

st.dataframe(filtered_df)

# Delete event
st.subheader("🗑️ Delete an Event")
delete_name = st.text_input("Enter the exact Event Name to delete")
if st.button("Delete"):
    if delete_name in list(df["Event Name"]):
        df = df[df["Event Name"] != delete_name]
        save_data(df)
        st.success(f"Event '{delete_name}' deleted successfully!")
    else:
        st.error("Event not found!")

# Display today's events
today = datetime.now().date()
today_events = df[df["Date"] == pd.to_datetime(today)]
if not today_events.empty:
    st.markdown("### 🎉 Events Today")
    st.table(today_events)
else:
    st.info("No events scheduled for today.")
