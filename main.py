from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse ####
from typing import List, Optional
import pandas as pd
import numpy as np
import random
import pickle


# load Kmeans Trained model for Similarity Artists Recommendation
loaded_model = pickle.load(open("GenresKmeans.pickle", "rb"))
# load Clean_Dataset.npy for getting Kmeans Clustering Predictions
clean_data = np.load("Clean_Dataset.npy", allow_pickle=True)

clusters_list = loaded_model.predict(clean_data)    # Clusters prediction of all the data entries

main_description = """
User Artist Recommendation System 🚀

## Items

<ul>
<li>You can <strong>Get a list of User's Artists</strong>.</li>
<li>You can <strong>Add Artists to User's Artists list</strong>.</li>
<li>You can <strong>Generate Artists Recommendation for a User based on:</strong>
    <ul>
    <li><strong>Random artists,</strong></li>
    <li><strong>Artists unknown to the user, or</strong></li>
    <li><strong>Artists that are similar to the ones they already listened to.</strong></li>
    </ul>
</li>
</ul>
"""

get_artists_description = """
<strong>Get Artists:</strong> Gets Artists list of the User from Database. Just enter the <strong>user_id</strong> of user you want to access.
"""
add_artist_description = """
<strong>Add Artists:</strong> Adds an Artist from Database to the User's Artists list. Enter <strong>user_id</strong> of the user and <strong>artist_name</strong> from the database.
"""
get_recommendations_description = """
<strong>Get Recommendations:</strong> Gives recommendations to the user based on:
    <ul>
    <li><strong>Random Artists: [recommendation_type: random]</strong>
        <ul>
        <li>Randomly suggests 5 artists from a list of all artists.</li>
        </li>
        </ul>
    <li><strong>Unknown Artists: [recommendation_type: unknown]</strong>
        <ul>
        <li>Randomly suggests 5 artists that are unknown to the user.</li>
        </li>
        </ul>
    <li><strong>Suggests similar Artists: [recommendation_type: similar]</strong>
        <ul>
        <li>It does the following steps:</li>
        <li>Checks if user is in the database</li>
        <li>Takes out the whole artists array of the selected user</li>
        <li>Predicts cluster of the selected user using the array as an instance using Kmeans trained model</li>
        <li>Uses the predicted cluster for finding other same predicted clusters of other users</li>
        <li>Collects indexes of users of the same cluster</li>
        <li>Gets the listened artists names of all users of the cluster</li>
        <li>Adds artists names of same cluster users in a set</li>
        <li>Appends similar artists in unknown_artists list that are not in user's lists</li>
        <li>Suggest 5 artists from that unknown_artists list</li>
        </ul>
    </ul>
Enter the <strong>user_id</strong> of the user and <strong>recommendation_type</strong> for the user.
"""


users_data = pd.read_csv("lastfm-matrix-germany.csv", index_col=0)
all_user_ids = users_data.index
all_artists_names = users_data.columns

ind_clust = pd.DataFrame({1:users_data.index,2: clusters_list}, )
ind_clust = ind_clust.set_index(ind_clust.columns[0])

# Define a function to get a list of recommended artists
async def get_recommended_artists(user_artists: List[int], recommendation_type: str, user_id: Optional[int] = 0):
    recommended_artists = []
    unknown_artists = []
    similar_artists = []
    if recommendation_type == "random":
        recommended_artists = random.sample(set(all_artists_names), 5)
    elif recommendation_type == "unknown":
        for artist in all_artists_names:
            if artist not in user_artists:
                unknown_artists.append(artist)
        recommended_artists = random.sample(set(unknown_artists), 5)
    elif recommendation_type == "similar":
        # similar_artists.append("sss")
        same_clusters = []
        common_artists = []
        common_artists = set(common_artists)
        temp = []
        for user in all_user_ids:
            if user == user_id: # If user is in the database
                instance = users_data.loc[user].values  # Take out the artists array
                pred = loaded_model.predict([instance])   # Predict cluster of the user
                for index in ind_clust.index:   # Use the predicted cluster for finding other same predicted clusters
                    if ind_clust.loc[index][2] == pred:
                        same_clusters.append(index) # Appending indexes of users of same cluster
                for row in same_clusters:
                    temp = await get_artists(row)    # Getting the artists names of each user of the cluster
                    for artists in temp.values():
                        common_artists.update(artists)
                    for artist in common_artists:
                        if artist not in user_artists:  # Appending similar artists in unknown_artists list that are not in user's lists
                            similar_artists.append(artist)
                    # raise HTTPException(status_code=404, detail="artist not found")
                recommended_artists = random.sample(set(similar_artists), 5)
                # raise HTTPException(status_code=404, detail="index not found")
    return recommended_artists


app = FastAPI(
    title="Artists Recommender",
    description=main_description,
    # summary="Deadpool's favorite app. Nuff said.",
    version="0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Saad Bin Sajid",
        "url": "https://www.linkedin.com/in/saadbinsajid/",
        "email": "saadbs7@gmail.com",
    }
)


@app.get("/")
async def home():
    return {"Please Go to: http://xx.xx.xx.xx:xxxx/docs#/"}
    #  return FileResponse(path = r'C:\Users\pc\Downloads\qq.csv', filename= 'Download.csv', media_type='csv')


@app.get("/users/{user_id}/artists}", description=get_artists_description)
# Define a function to get an User by ID and get it's Artists
async def get_artists(user_id: int):
    list = []
    for user in all_user_ids:
        if user == user_id:
            for artist in all_artists_names:
                if users_data.loc[user][artist] == 1:
                    list.append(artist)
            
            return {user : list}
    raise HTTPException(status_code=404, detail="User not found")


# Define a route to update an artist's listeners
@app.put("/users/{user_id}/artists", description=add_artist_description)
async def add_artist(user_id: int, artist_name: str):
    for user in all_user_ids:
        if user == user_id:
            for artist in all_artists_names:
                if artist == artist_name:
                    users_data.loc[user_id][artist_name] = 1
                    users_data.to_csv("lastfm-matrix-germany.csv")
                    return {"message": f"User: {user_id}, Successfully listened to Artist: {artist_name}"}
            raise HTTPException(status_code=404, detail="Artist not found")
    raise HTTPException(status_code=404, detail="User not found")


# Define a route to get recommended artists for a user
@app.get("/users/{user_id}/recommendations", description=get_recommendations_description)
async def get_recommendations(user_id: int, recommendation_type: Optional[str] = "random"):
    user_artists = (await get_artists(user_id))[user_id] # Contains the Artists the selected User already listened
    recommendations = await get_recommended_artists(user_artists, recommendation_type, user_id)
    return recommendations


