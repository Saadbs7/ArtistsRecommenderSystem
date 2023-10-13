## Description:

This repository contains a FastAPI-based User Artist Recommendation System. The system provides functionalities to manage users' artists, add new artists to their lists, and generate artist recommendations based on different criteria. The recommendation types include random artists, unknown artists to the user, and artists similar to the ones they have already listened to.

## Features:

Retrieve a list of a user's artists from the database.

Add artists to a user's list of artists.

Generate artist recommendations based on:

a. Random artists.

b. Artists unknown to the user.

c. Artists similar to the ones they already listened to.


## Files Description:

- main.py: It contains the main code for the API

- Similar_Artists_Kmeans_Model.ipynb: It contains the Kmeans Clustering AI model implementation for suggesting similar artists to the user

- Clean_Dataset.npy: Cleaned ready to train Numpy array of Dataset

- GenresKmeans.pickle: Kmeans trained model in pickle format

- lastfm-matrix-germany.csv: Dataset used in Task


## Functions of API:
The API is doing the following things:

1. Gets a List of Artists of a user: 
        It takes the user_id and returns a list of artists that the user_id user has listened to.

2. Updates the dataset when the user listens to an artist: 
        It takes a valid user_id and a valid artist_name and then it updates the dataset by setting the artist field for that user as 1.

3. Gives recommendations to the user based on:
    a. Random Artists:
        Randomly suggests 5 artists from a list of all artists.
    b. Unknown Artists:
        Randomly suggest 5 artists that are unknown to the user.
    c. Suggests Similar Artists:
        It does the following steps:
        # Checks if the user is in the database
        # Takes out the whole artists array of the selected user
        # Predicts cluster of the selected user using the array as an instance using Kmeans trained model
        # Uses the predicted cluster for finding other same predicted clusters of other users
        # Collects indexes of users of the same cluster
        # Gets the listened artists' names of all users of the cluster
        # Adds artists' names of same cluster users in a set
        # Appends similar artists in unknown_artists list that are not in user's lists
        # Suggest 5 artists from that unknown_artists list

## Clustering Algorithm for Similar Artist Recommendations:
I used Kmeans Clustering for classifying users in clusters. The idea is that the users who belong to the same clusters have very similar tastes of music and artists.
For the Kmeans Clustering model, I did PCA decomposition of the Dataset for a better selection of the Number of Clusters for the algorithm. 
I used Elbow-method for selection criteria of the number of clusters.

That's all!
