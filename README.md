## Description:

This repository contains a FastAPI-based User Artist Recommendation System. The system provides functionalities to manage users' artists, add new artists to their lists, and generate artist recommendations based on different criteria. The recommendation types include random artists, unknown artists to the user, and artists similar to the ones they have already listened to.

## Features:

Retrieve a list of a user's artists from the database.

Add artists to a user's list of artists.

Generate artist recommendations based on:<br>
<ul>
a. Random artists.<br>
b. Artists unknown to the user.<br>
c. Artists similar to the ones they already listened to.<br>
</ul>

## Files Description:

- main.py: It contains the main code for the API

- Similar_Artists_Kmeans_Model.ipynb: It contains the Kmeans Clustering AI model implementation for suggesting similar artists to the user

- Clean_Dataset.npy: Cleaned ready to train Numpy array of Dataset

- GenresKmeans.pickle: Kmeans trained model in pickle format

- lastfm-matrix-germany.csv: The data is sourced from this file


## Functions of API:
The API is doing the following things:

1. Gets a List of Artists of a user:<br>
<ul>
It takes the user_id and returns a list of artists that the user_id user has listened to.
</ul>

2. Updates the dataset when the user listens to an artist:<br>
<ul>
It takes a valid user_id and a valid artist_name and then it updates the dataset by setting the artist field for that user as 1.
</ul>

3. Gives recommendations to the user based on:<br>
        <ul>
        a. Random Artists:<br>
                <ul>
                Randomly suggests 5 artists from a list of all artists.<br>
                </ul>
        b. Unknown Artists:<br>
                <ul>
                Randomly suggest 5 artists that are unknown to the user.<br>
                </ul>
        c. Suggests Similar Artists:<br>
                <ul>
                It does the following steps:<br>
                        <ul>
                        - Checks if the user is in the database<br>
                        - Takes out the whole artists array of the selected user<br>
                        - Predicts cluster of the selected user using the array as an instance using Kmeans trained model<br>
                        - Uses the predicted cluster for finding other same predicted clusters of other users<br>
                        - Collects indexes of users of the same cluster<br>
                        - Gets the listened artists' names of all users of the cluster<br>
                        - Adds artists' names of same cluster users in a set<br>
                        - Appends similar artists in unknown_artists list that are not in user's lists<br>
                        - Suggest 5 artists from that unknown_artists list<br>
                        </ul>
                </ul>
        </ul>
## Additional Information:

The system utilizes KMeans Clustering to classify users into clusters based on their music preferences. Users belonging to the same cluster are assumed to have very similar tastes in music and artists.

Prior to applying KMeans Clustering, Principal Component Analysis (PCA) decomposition was performed on the dataset. PCA helps in dimensionality reduction, enabling a better selection of the number of clusters for the KMeans algorithm.

The number of clusters for the KMeans Clustering model was selected using the Elbow Method, a technique that plots the explained variation as a function of the number of clusters, helping to identify the optimal number of clusters for the dataset. This method aids in finding a balance between model complexity and the accuracy of cluster assignments.

The system is containerized using Docker, and the Docker image can be pulled from the provided Docker repository for easy deployment and usage.

## Pull from Docker Repository: 
To pull the Docker image "user-artist-system" from my repository, you can use the following command:
```
docker pull saadbs/alpha-repo7:user-artist-system
```

## Compose image
If you want to create your own Docker image, you can use Docker Compose. 

Open the docker-compose.yml file and change the image field under the app service to your desired image name.

Build and Run the Docker Compose:
```
docker-compose up --build
```

