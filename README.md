Hi! Welcome to my Coding Exercise!
I have tried to write good (not too long) comments in my codes for a better explanation.

You may find the following files in this folder:

- main.py : It contains the code for the API

- Similar_Artists_Kmeans_Model.ipynb : It contains the Kmeans Clustering AI model implementation for suggesting similar artists to the user

- Clean_Dataset.npy : Cleaned ready to train numpy array of dataset

- GenresKmeans.pickle : Kmeans trained model in pickle format

- lastfm-matrix-germany.csv : This is the Dataset that was given for this challenge


The API is doing following things:

1. Gets List of Artists of a user: 
        It takes the user_id and returs list of artists that the user_id user has listened.

2. Updates the dataset when the user listens to an artist: 
        It takes a valid user_id and a valid artist_name and then it updates the dataset by setting the artist field for that user as 1.

3. Gives recommendations to the user based on:
    a. Random Artists:
        Randomly suggests 5 artists from a list of all artists.
    b. Unknown Artists:
        Randomly suggests 5 artists that are unknown to the user.
    c. Suggests similar Artists:
        It does the following steps:
        # Checks if user is in the database
        # Takes out the whole artists array of the selected user
        # Predicts cluster of the selected user using the array as an instance using Kmeans trained model
        # Uses the predicted cluster for finding other same predicted clusters of other users
        # Collects indexes of users of the same cluster
        # Gets the listened artists names of all users of the cluster
        # Adds artists names of same cluster users in a set
        # Appends similar artists in unknown_artists list that are not in user's lists
        # Suggest 5 artists from that unknown_artists list


I used Kmeans Clustering for classifying users in clusters. The idea is that the users who belong to the same clusters have very similar taste of music and artists.
For Kmeans Clustering model I did PCA decomposition of Dataset for a better selection of Number of Clusters for the algorithm. 
I used Elbow method for selection criteria of number of clusters.

That's all!

I really liked working on the task and it helped me in revising some stuff too.
I am looking forward to our Meeting!

Best regards.
Saad

