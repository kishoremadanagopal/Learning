@@@ part
id: 5
title: Unsupervised Learning
level: Intermediate
blurb: No labels, no right answers: find natural groups of customers with k-means, and squeeze many columns into a few with PCA so you can see your data.

@@@ lesson
id: kmeans
title: Clustering with k-means
minutes: 18
summary: Group similar rows without any labels, choose the number of groups with the elbow and silhouette, and describe what each group means.
---
So far every dataset had answers to learn from. Often you don't: a shop has customers but no list of "customer types". **Clustering** finds groups of similar rows by itself. Marketing teams use it for **customer segments**; it's also used to group documents, products or sensor readings.

The `shoppers.csv` file has 200 customers with their income, a **spending score** (1–100, how much they spend relative to others), age and visits per month. No labels.

```python
import pandas as pd
import matplotlib.pyplot as plt

shoppers = pd.read_csv("shoppers.csv")
print(shoppers.head())

plt.scatter(shoppers["annual_income_k"], shoppers["spending_score"])
plt.xlabel("annual income (thousands)")
plt.ylabel("spending score")
plt.title("200 shoppers: can you see the groups?")
plt.show()
```

Your eye picks out about five blobs. k-means finds them with arithmetic.

### How k-means works

You choose **k**, the number of clusters. Then:

1. Place k **centres** (centroids) at random points.
2. **Assign** every row to its nearest centre.
3. **Move** each centre to the average of the rows assigned to it.
4. Repeat steps 2 and 3 until nothing changes.

![Four panels showing k-means on two-dimensional points. 1: three random starting centres. 2: each point coloured by its nearest centre. 3: centres moved to the middle of their points. 4: after a few rounds, three settled groups with a centre in each](figures/kmeans-steps.svg)

Because the start is random, different starts can end in different groupings. `n_init=10` runs it 10 times and keeps the best (the tightest clusters); `random_state` makes it repeatable.

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score"]]

kmeans = KMeans(n_clusters=5, n_init=10, random_state=0)
shoppers["cluster"] = kmeans.fit_predict(X)

print(shoppers["cluster"].value_counts().sort_index())
print(pd.DataFrame(kmeans.cluster_centers_, columns=X.columns).round(1))

plt.scatter(X["annual_income_k"], X["spending_score"], c=shoppers["cluster"], cmap="tab10")
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker="X", s=200, color="black")
plt.xlabel("annual income (thousands)")
plt.ylabel("spending score")
plt.title("Five shopper segments")
plt.show()
```

`fit_predict` fits and returns each row's cluster number. There's no `y` anywhere: that's what makes it unsupervised. The cluster numbers (0 to 4) are just names, in no particular order.

### Choosing k

There's no test set to tell you the right k. Two common guides:

- **Inertia** (the elbow method): the total squared distance from each row to its centre. It always falls as k grows (more centres, shorter distances), so look for the **elbow**, where adding clusters stops helping much.
- **Silhouette score** (−1 to 1): how much closer each row is to its own cluster than to the next nearest one. Higher is better.

![Left: inertia against k from 2 to 8, falling steeply until k=5 and then flattening into an elbow. Right: silhouette score against k, peaking at k=5](figures/elbow-silhouette.svg)

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score"]]

for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}  inertia {km.inertia_:>8.0f}   silhouette {silhouette_score(X, km.labels_):.3f}")
```

Both agree on **k = 5** here. Real data is rarely this tidy; often the "right" k is the one whose groups are **useful** and **explainable** to the people who'll act on them.

### Describe the clusters

A cluster is only useful once you can say what it **means**. Average each feature per cluster, including features you didn't cluster on:

```python
import pandas as pd
from sklearn.cluster import KMeans

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score"]]
shoppers["cluster"] = KMeans(n_clusters=5, n_init=10, random_state=0).fit_predict(X)

profile = shoppers.groupby("cluster")[["annual_income_k", "spending_score", "age", "visits_per_month"]].mean().round(1)
profile["customers"] = shoppers["cluster"].value_counts().sort_index()
print(profile)
```

Now you can name them: high earners who spend a lot (and visit often), high earners who spend little (older, rarely visit: a group worth winning over), younger lower-income big spenders, careful low-income spenders, and a large middle group. Age and visits weren't used for clustering, yet they differ between groups: a sign the segments are real.

### Scale when features differ

k-means uses distances, so like KNN it needs **scaled** features when units differ. Income (12–108) and spending score (1–99) happen to have similar ranges, which is why the example above worked unscaled. Add age and visits (0–12) and you should scale:

```python
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score", "age", "visits_per_month"]]

model = make_pipeline(StandardScaler(), KMeans(n_clusters=5, n_init=10, random_state=0))
shoppers["cluster"] = model.fit_predict(X)
print(shoppers.groupby("cluster")[X.columns].mean().round(1))
```

### Limits of k-means

- You must choose k.
- It assumes roundish, similar-sized blobs. Long, curved or very uneven groups confuse it (`DBSCAN` and `AgglomerativeClustering` in scikit-learn handle other shapes).
- Every row is forced into some cluster, even a strange one that fits nowhere.

:::exercise Segment the shoppers
Cluster the shoppers on `annual_income_k` and `spending_score` (unscaled) with `KMeans(n_clusters=4, n_init=10, random_state=1)`. Store the model in `km`, each row's cluster in a new column `shoppers["segment"]`, and the model's inertia in `inertia`.
```python starter
import pandas as pd
from sklearn.cluster import KMeans

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score"]]

```
```python check
import pandas as pd
from sklearn.cluster import KMeans
s = pd.read_csv("shoppers.csv")
ref = KMeans(n_clusters=4, n_init=10, random_state=1).fit(s[["annual_income_k", "spending_score"]])
got = need("km", KMeans)
same(got.n_clusters, 4, "n_clusters")
sh = need("shoppers", pd.DataFrame)
if "segment" not in sh.columns:
    raise AssertionError("Add a column called segment with the cluster numbers.")
same(list(sh["segment"]), list(ref.labels_), "shoppers['segment']")
same(float(need("inertia")), float(ref.inertia_), "inertia", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.cluster import KMeans

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score"]]

km = KMeans(n_clusters=4, n_init=10, random_state=1)
shoppers["segment"] = km.fit_predict(X)
inertia = km.inertia_
print(shoppers["segment"].value_counts(), round(inertia))
```
hint: `km.fit_predict(X)` returns the cluster numbers; after fitting, `km.inertia_` holds the inertia.
:::

:::exercise Pick k by silhouette
For the **scaled** four-feature shopper data below, try k from 2 to 7 with `KMeans(n_clusters=k, n_init=10, random_state=0)`. Store a dictionary `sil` mapping each k to its silhouette score (computed on the **scaled** data), and the k with the highest score in `best_k`.
```python starter
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

shoppers = pd.read_csv("shoppers.csv")
X_scaled = StandardScaler().fit_transform(shoppers[["annual_income_k", "spending_score", "age", "visits_per_month"]])

```
```python check
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
s = pd.read_csv("shoppers.csv")
Xs = StandardScaler().fit_transform(s[["annual_income_k", "spending_score", "age", "visits_per_month"]])
exp = {k: silhouette_score(Xs, KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(Xs)) for k in range(2, 8)}
got = need("sil", dict)
same({int(k): float(v) for k, v in got.items()}, exp, "sil", tol=1e-6)
same(int(need("best_k")), max(exp, key=exp.get), "best_k")
```
```python solution
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

shoppers = pd.read_csv("shoppers.csv")
X_scaled = StandardScaler().fit_transform(shoppers[["annual_income_k", "spending_score", "age", "visits_per_month"]])

sil = {}
for k in range(2, 8):
    labels = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X_scaled)
    sil[k] = silhouette_score(X_scaled, labels)
best_k = max(sil, key=sil.get)
print({k: round(v, 3) for k, v in sil.items()}, best_k)
```
hint: `silhouette_score(X_scaled, labels)` needs the same data the clusters were made from, plus the labels.
:::

:::quiz
? What makes k-means "unsupervised"?
+ It groups rows without any labels to learn from
- It runs without supervision from the programmer
- It needs no data
= There's no y: the model only looks at the features.
? What happens to inertia as k increases?
+ It always goes down, so you look for the elbow instead of the minimum
- It always goes up
- It's lowest at the right k
= More centres always mean shorter distances. At k = number of rows, inertia is 0.
? Why scale features before k-means?
+ It uses distances, so features in bigger units would dominate the grouping
- k-means only accepts values between 0 and 1
- Scaling chooses k automatically
= Same reason as KNN.
? You've found 5 clusters. What's the next essential step?
+ Describe each cluster (averages of the features) so people can understand and act on it
- Delete the smallest cluster
- Compute accuracy against the labels
= Unlabelled groups are only useful once you can explain them.
:::

@@@ lesson
id: pca
title: Dimensionality reduction with PCA
minutes: 16
summary: Combine many correlated columns into a few new ones that keep most of the information, to see data in 2-D and simplify models.
---
You can plot two features on a chart. With 4, 50 or 1,000 features, you can't. **Dimensionality reduction** builds a few **new** columns that summarise many old ones. The classic method is **principal component analysis (PCA)**.

### The idea

When features are correlated, they partly repeat each other. Fruit width and weight go together; maths and science scores go together. PCA finds new axes, called **principal components**, along which the data varies most:

- **PC1** is the direction of the **most** variation in the data.
- **PC2** is the direction of the most remaining variation, at right angles to PC1.
- And so on: there are as many components as features, each capturing less than the one before.

Keeping just the first few components keeps most of the information in far fewer columns.

![Left: a cloud of points that stretches along a diagonal, with two arrows: a long arrow (PC1) along the stretch and a short arrow (PC2) across it. Right: the same points redrawn using PC1 as the x-axis and PC2 as the y-axis; almost all the spread is along PC1](figures/pca-idea.svg)

### Fruit: from 3 columns to 2

```python
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]

pca = make_pipeline(StandardScaler(), PCA())
pca.fit(X)
ratios = pca[-1].explained_variance_ratio_
print("share of variation per component:", ratios.round(3))
print("first two together:", ratios[:2].sum().round(3))
```

**Explained variance ratio** is the share of the total variation each component captures. The first two components keep about 98% of the fruits' variation, so a 2-D picture loses almost nothing:

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
coords = make_pipeline(StandardScaler(), PCA(n_components=2)).fit_transform(X)

for kind, colour in [("apple", "tab:red"), ("orange", "tab:orange"), ("lemon", "gold")]:
    rows = (fruit["fruit"] == kind).to_numpy()
    plt.scatter(coords[rows, 0], coords[rows, 1], label=kind, color=colour, edgecolor="black", linewidth=0.3)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.title("Three measurements, drawn in two dimensions")
plt.show()
```

PCA never saw the fruit names (it's unsupervised), yet lemons separate clearly, while apples and oranges overlap: the same difficulty every classifier in this course ran into.

Scale first: PCA looks for the directions of biggest variation, so unscaled, weight in grams (spread about 36) would swamp the centimetres (spread about 1) and become PC1 by itself.

### What do the components mean?

Each component is a weighted mix of the original features. The weights are in `components_`:

```python
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

students = pd.read_csv("students.csv")
cols = ["hours_studied", "attendance_pct", "math", "science", "english"]
pca = make_pipeline(StandardScaler(), PCA(n_components=2)).fit(students[cols])

print(pd.DataFrame(pca[-1].components_, columns=cols, index=["PC1", "PC2"]).round(2))
print(pca[-1].explained_variance_ratio_.round(3))
```

PC1 has positive weights on everything, biggest on study hours, maths and science: it's an "overall effort and results" score, and it holds about 53% of the variation. Interpreting components is part science, part art; don't over-read small weights.

### Choosing how many components

Ask PCA to keep enough components for a share of the variation, by passing a number between 0 and 1:

```python
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

housing = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km", "price_k"]
pca = make_pipeline(StandardScaler(), PCA(n_components=0.9)).fit(housing[cols])
print("components kept:", pca[-1].n_components_)
print(pca[-1].explained_variance_ratio_.round(3), "total", pca[-1].explained_variance_ratio_.sum().round(3))
```

Three components hold over 90% of the variation in five housing columns.

### What PCA is used for

- **Seeing** high-dimensional data in 2-D (like the fruit chart), to spot groups and odd points.
- **Simplifying** before another model, especially when there are many correlated features (it can reduce overfitting and speed up training).
- **Compressing** data, like images, by keeping only the strongest components.

Trade-off: components are mixtures, so a model built on them is harder to explain than one built on the original features. For pictures of very complex data (like word or image embeddings), non-linear methods such as **t-SNE** and **UMAP** often show groups more clearly, but their axes have no meaning at all.

:::exercise Keep 95%
Fit `make_pipeline(StandardScaler(), PCA(n_components=0.95))` on the four numeric shopper columns below. Store the pipeline in `pca`, the number of components it kept in `n_kept`, and the transformed data in `reduced`.
```python starter
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score", "age", "visits_per_month"]]

```
```python check
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
s = pd.read_csv("shoppers.csv")
X_ = s[["annual_income_k", "spending_score", "age", "visits_per_month"]]
ref = make_pipeline(StandardScaler(), PCA(n_components=0.95)).fit(X_)
same(int(need("n_kept")), int(ref[-1].n_components_), "n_kept")
got = np.asarray(need("reduced"))
exp = ref.transform(X_)
same(got.shape, exp.shape, "reduced's shape")
same(np.abs(got), np.abs(exp), "reduced", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

shoppers = pd.read_csv("shoppers.csv")
X = shoppers[["annual_income_k", "spending_score", "age", "visits_per_month"]]

pca = make_pipeline(StandardScaler(), PCA(n_components=0.95))
reduced = pca.fit_transform(X)
n_kept = pca[-1].n_components_
print(n_kept, reduced.shape)
```
hint: `pca.fit_transform(X)` returns the reduced data; `pca[-1].n_components_` is the number kept.
:::

:::exercise How much does PC1 hold?
Fit a scaled PCA (all components) on `area_sqm`, `bedrooms`, `age_years`, `distance_km` and `price_k` from `housing.csv`. Store the share of variation captured by the **first** component in `pc1_share`, and the name of the feature with the **largest absolute weight** in PC1 in `top_feature`.
```python starter
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

housing = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km", "price_k"]

```
```python check
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
h = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km", "price_k"]
p = make_pipeline(StandardScaler(), PCA()).fit(h[cols])
same(float(need("pc1_share")), float(p[-1].explained_variance_ratio_[0]), "pc1_share", tol=1e-6)
same(str(need("top_feature")), cols[int(np.argmax(np.abs(p[-1].components_[0])))], "top_feature")
```
```python solution
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

housing = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km", "price_k"]

pca = make_pipeline(StandardScaler(), PCA()).fit(housing[cols])
pc1_share = pca[-1].explained_variance_ratio_[0]
weights = pd.Series(pca[-1].components_[0], index=cols)
top_feature = weights.abs().idxmax()
print(round(pc1_share, 3))
print(weights.round(2))
```
hint: `components_[0]` holds PC1's weights in the order of `cols`; put them in a Series and use `.abs().idxmax()`.
:::

:::quiz
? What is the first principal component?
+ The direction in which the data varies the most
- The first column of the data
- The most important feature for predicting the label
= PCA finds directions of biggest variation; it never looks at a label.
? PCA's explained_variance_ratio_ is [0.73, 0.25, 0.02]. Keeping two components keeps:
+ About 98% of the variation
- About 73%
- Two thirds of the rows
= Add the first two shares.
? Why scale before PCA?
+ Otherwise the feature with the biggest units dominates the first component
- PCA only works on values between 0 and 1
- Scaling removes outliers
= PCA looks for large variation, and unscaled grams vary far more than centimetres.
? A downside of training a model on PCA components is:
+ The components are mixtures of features, so the model is harder to explain
- It always lowers accuracy
- It leaks the test set
= You trade some interpretability for fewer columns.
:::
