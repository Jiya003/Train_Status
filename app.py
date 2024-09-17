import streamlit as st
import requests

def fetch_live_train_status(train_no):
    url = f"https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus?trainNo={train_no}&startDay=1"
    headers = {
        "X-RapidAPI-Key": "a1e0032c9amsh0c59e81fe5967c8p1e443bjsn602da0c29fd4",
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == True and 'data' in data:
            return data['data']
        else:
            return {"error": "Train data not found or the request was unsuccessful."}
    else:
        return {"error": f"Unable to fetch data. Status code: {response.status_code}"}

def main():
    st.set_page_config(page_title="Live Train Status", layout="wide")
    
    # App Title and Description
    st.title("🚆 Live Train Status")
    st.write(
        "Enter the train number below to get the live status of the train. "
        "You can check the current location, source, destination, and more."
    )

    # Input for Train Number
    train_number = st.text_input("Train Number", placeholder="Enter train number...")

    # Button to Fetch Status
    if st.button("Get Status"):
        if train_number:
            with st.spinner("Fetching train status..."):
                train_data = fetch_live_train_status(train_number)
                
                if "error" in train_data:
                    st.error(train_data["error"])
                else:
                    st.success(f"Train Number: **{train_data.get('train_number', 'Unknown')}**")
                    st.write(f"**Train Name:** {train_data.get('train_name', 'Unknown')}")
                    st.write(f"**Update Time:** {train_data.get('notification_date', 'Unknown')}")
                    st.write(f"**Source Station:** {train_data.get('source', 'Unknown')}")
                    st.write(f"**Destination Station:** {train_data.get('destination', 'Unknown')}")
                    st.write(f"**Total Distance:** {train_data.get('total_distance', 'Unknown')} km")
                    st.write(f"**Distance from Source:** {train_data.get('distance_from_source', 'Unknown')} km")
                    st.write(f"**Current Station:** {train_data.get('current_station_name', 'Unknown')}")
                    
                    if 'current_location_info' in train_data and train_data['current_location_info']:
                        for i, location_info in enumerate(train_data["current_location_info"]):
                            st.write(f"**Message {i+1}:** {location_info.get('readable_message', 'No message available')}")
                    else:
                        st.write("**No location messages available.**")
        else:
            st.warning("Please enter a train number.")

if __name__ == "__main__":
    main()
