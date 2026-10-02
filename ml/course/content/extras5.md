@@ kmeans
topics: clustering without labels, the k-means steps, centroids, fit_predict, inertia and the elbow, silhouette score, describing clusters, scaling, limits of k-means
terms:
- **Clustering:** grouping similar rows without any labels.
- **Customer segmentation:** clustering customers into groups that behave alike, so each can be treated differently.
- **k-means:** a clustering method that alternates between assigning rows to the nearest centre and moving each centre to the average of its rows.
- **Centroid:** the centre of a cluster: the average of its rows.
- **n_init:** how many random starts k-means tries, keeping the best.
- **fit_predict:** fits a clustering model and returns each row's cluster number.
- **Inertia:** the total squared distance from each row to its cluster centre; lower means tighter clusters.
- **Elbow method:** choosing k where adding more clusters stops reducing inertia much.
- **Silhouette score:** from −1 to 1, how much closer rows are to their own cluster than to the nearest other one.
- **Cluster profile:** the average of each feature within each cluster, used to describe what the cluster means.
- **DBSCAN:** a clustering method that finds groups of any shape and can leave odd points unassigned.
mistakes:
- Clustering unscaled features with very different units.
- Picking the k with the lowest inertia. It always falls as k grows.
- Treating cluster numbers as meaningful order or as labels that stay the same between runs.
- Stopping at "we found 5 clusters" without describing what each one is.

@@ pca
topics: dimensionality reduction, principal components, explained variance ratio, scaling before PCA, 2-D pictures of many features, reading components_, choosing the number of components, t-SNE and UMAP
terms:
- **Dimensionality reduction:** replacing many columns with a few new ones that keep most of the information.
- **Dimension:** a column (feature) of the data; 3 features means 3-dimensional data.
- **PCA (principal component analysis):** finds new axes (principal components) along which the data varies most.
- **Principal component:** a new column made as a weighted mix of the original features; PC1 holds the most variation.
- **Explained variance ratio:** the share of the total variation each component captures.
- **components_:** the weights each component gives to the original features.
- **n_components:** how many components to keep, or (between 0 and 1) what share of variation to keep.
- **t-SNE / UMAP:** non-linear methods for drawing complex data in 2-D; good for pictures, with axes that have no meaning.
mistakes:
- Running PCA on unscaled features, so the biggest-unit feature becomes PC1 by itself.
- Thinking PCA picks the features most useful for predicting a label. It ignores labels entirely.
- Fitting PCA on all the data before a train/test split. Like any learned step, put it in a pipeline.
- Over-interpreting small component weights.
