import json

watchList = []

def add_movie(watchList):
    title = input("Enter Movie Title: ")
    genre = input("Enter Genre: ")
    watchList.append({"Title": title, "Genre": genre, "Status": "Not Watched"})
    print(f"Added {title} to your watchlist!")

def view_movies(watchList):
    if not watchList:
        print("Your watchlist is empty!")
        return
    for index, movie in enumerate(watchList, 1):
        print(f"{index}. Movie: {movie["Title"]} \n   Genre: {movie["Genre"]} \n   Status: {movie["Status"]}\n")

def mark_watched(watchList):
    view_movies(watchList)
    try:
        choice = int(input("\nEnter the number of the movie that you watched: ")) - 1
        watchList[choice]["Status"] = "Watched"
        print(f"Updated {watchList[choice]["Title"]} to Watched!")
    except (IndexError, ValueError):
        print("Invalid Selection. Please try again.")

def save_watchlist(watchlist, filename="watchlist.json"):
    with open(filename, "w") as f:
        json.dump(watchlist, f, indent=4)

def load_watchlist(filename="watchlist.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist yet


watchList = load_watchlist()

while True:
    print("\n====================")
    print(" MOVIE WATCHLIST ")
    print("====================")
    print("1. Add Movie")
    print("2. View Watchlist")
    print("3. Mark Movie as Watched")
    print("4. Save & Exit")
    
    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":
        add_movie(watchList)
    elif choice == "2":
        view_movies(watchList)
    elif choice == "3":
        mark_watched(watchList)
    elif choice == "4":
        save_watchlist(watchList)
        print("Saved. Goodbye!")
        break  # Exit the loop
    else:
        print("Invalid choice, please select 1, 2, 3, or 4.")
