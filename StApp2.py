import json
import streamlit as st

def save_watchlist(watchlist, filename="watchlist.json"):
    with open(filename, "w") as f:
        json.dump(watchlist, f, indent=4)

def load_watchlist(filename="watchlist.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Initialize state from load_watchlist()
if "watchList" not in st.session_state:
    st.session_state.watchList = load_watchlist()

def add_movie(watchList):
    st.subheader("Add Movie")
    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("Enter Movie Title:")
        genre = st.text_input("Enter Genre:")
        submitted = st.form_submit_button("Add")
        
        if submitted:
            if title.strip() and genre.strip():
                watchList.append({"Title": title, "Genre": genre, "Status": "Not Watched"})
                save_watchlist(watchList)
                st.success(f"Added {title} to your watchlist!")
            else:
                st.warning("Please enter both Title and Genre.")

def view_movies(watchList):
    st.subheader("Your Watchlist")
    if not watchList:
        st.info("Your watchlist is empty!")
        return
    for index, movie in enumerate(watchList, 1):
        st.markdown(f"**{index}. Movie:** {movie['Title']}  \n"
                    f"**Genre:** {movie['Genre']}  \n"
                    f"**Status:** {movie['Status']}")
        st.divider()

def mark_watched(watchList):
    st.subheader("Mark Movie as Watched")
    if not watchList:
        st.info("Your watchlist is empty!")
        return
    
    view_movies(watchList)
    
    options = [f"{i}. {m['Title']}" for i, m in enumerate(watchList, 1)]
    selected_option = st.selectbox("Select the movie number you watched:", options)
    
    if st.button("Mark Watched"):
        try:
            choice = int(selected_option.split(".")[0]) - 1
            watchList[choice]["Status"] = "Watched"
            save_watchlist(watchList)
            st.success(f"Updated {watchList[choice]['Title']} to Watched!")
            st.rerun()
        except (IndexError, ValueError):
            st.error("Invalid Selection. Please try again.")


# --- MAIN MENU / NAVIGATION ---
st.title("🎬 MOVIE WATCHLIST")

# 1. Clean dropdown navigation (removes circle radio buttons)
menu_choice = st.sidebar.selectbox(
    "Menu", 
    ["1. Add Movie", "2. View Watchlist", "3. Mark Movie as Watched"]
)

st.sidebar.divider()

# 2. Dedicated Save Button
if st.sidebar.button("💾 Save Watchlist", use_container_width=True):
    save_watchlist(st.session_state.watchList)
    st.sidebar.success("Saved successfully!")

# Display selected page content
if menu_choice == "1. Add Movie":
    add_movie(st.session_state.watchList)
elif menu_choice == "2. View Watchlist":
    view_movies(st.session_state.watchList)
elif menu_choice == "3. Mark Movie as Watched":
    mark_watched(st.session_state.watchList)