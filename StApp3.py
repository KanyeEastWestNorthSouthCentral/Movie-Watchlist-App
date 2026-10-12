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

# Track active view in session state (default to 'Add Movie')
if "page" not in st.session_state:
    st.session_state.page = "Add Movie"

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


# --- MAIN MENU / SIDEBAR NAVIGATION ---
st.title("🎬 MOVIE WATCHLIST")

st.sidebar.markdown("### Navigation")

# Listed Navigation Buttons
if st.sidebar.button("➕ Add Movie", use_container_width=True):
    st.session_state.page = "Add Movie"

if st.sidebar.button("📋 View Watchlist", use_container_width=True):
    st.session_state.page = "View Watchlist"

if st.sidebar.button("✅ Mark Movie as Watched", use_container_width=True):
    st.session_state.page = "Mark Movie as Watched"

st.sidebar.divider()

# Dedicated Save Button
if st.sidebar.button("💾 Save Watchlist", use_container_width=True):
    save_watchlist(st.session_state.watchList)
    st.sidebar.success("Saved successfully!")


# --- ROUTING / PAGE DISPLAY ---
if st.session_state.page == "Add Movie":
    add_movie(st.session_state.watchList)
elif st.session_state.page == "View Watchlist":
    view_movies(st.session_state.watchList)
elif st.session_state.page == "Mark Movie as Watched":
    mark_watched(st.session_state.watchList)
