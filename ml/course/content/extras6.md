@@ text-classification
topics: bag of words, CountVectorizer, vocabulary and document-term matrix, sparse matrices, stop words and n-grams, TF-IDF, Naive Bayes, a spam filter, top words, embeddings and LLMs
terms:
- **Bag of words:** representing a text by how many times each word appears, ignoring the order.
- **Vocabulary:** all the distinct words a vectorizer learned from the training texts.
- **Document-term matrix:** a table with one row per text and one column per word, holding counts or weights.
- **CountVectorizer:** turns texts into word counts.
- **TfidfVectorizer:** turns texts into TF-IDF weights.
- **TF-IDF:** term frequency × inverse document frequency: a word's count, scaled down if it appears in many texts.
- **Stop words:** very common words (the, a, to) often removed because they carry little meaning.
- **n-gram:** a run of n neighbouring words, such as "free prize" (a 2-gram, or bigram).
- **Naive Bayes:** a fast probabilistic classifier that combines how likely each word is in each class.
- **Embedding:** a list of numbers produced by a language model that captures a text's meaning; similar meanings get similar numbers.
- **Large language model (LLM):** a very large model trained on text that can follow instructions, such as labelling a message.
- **Evals:** tests that measure how well an AI system (such as an LLM) performs, using held-out labelled examples.
mistakes:
- Passing a DataFrame with double brackets to a text vectorizer. It wants one column of strings: df["text"].
- Fitting the vectorizer on all texts before splitting. Its vocabulary must come from the training texts (use a pipeline).
- Expecting a bag-of-words model to understand synonyms or negation.

@@ model-to-product
topics: saving and loading pipelines with joblib, version and security warnings, serving predictions, data and concept drift, monitoring, fairness per group and proxies, model cards, classic ML vs LLMs
terms:
- **joblib:** a library that saves Python objects, such as fitted pipelines, to files and loads them back.
- **Serialisation:** saving an object to a file or bytes so it can be loaded later.
- **Serving:** making a model's predictions available to other software, often as a web API.
- **FastAPI:** a popular Python library for building web APIs, often used to serve models.
- **Data drift:** a change in the input data compared with the training data.
- **Concept drift:** a change in the relationship between features and the label.
- **Monitoring:** tracking a live model's inputs, predictions and accuracy over time.
- **Retraining:** fitting the model again on fresher data.
- **Fairness:** a model working comparably well for different groups of people.
- **Proxy:** a feature that indirectly reveals another one, such as a postcode standing in for ethnicity or income.
- **Model card:** a short document describing a model's intended use, data, performance, groups checked and limits.
- **EU AI Act:** the European Union's law setting rules for AI systems according to their risk.
mistakes:
- Saving only the model and redoing the preparation by hand at prediction time.
- Loading a model file from an untrusted source; it can run code.
- Assuming a model keeps working after launch. Monitor it and retrain.
- Checking fairness only on averages, or trusting a rate computed on a handful of people.

@@ final-project
topics: framing a business question, choosing a success measure, splitting first, baseline, pipeline, comparing models with CV, tuning, choosing a threshold with cross_val_predict, the single final test, permutation importance on a pipeline, the final report
terms:
- **Success measure:** the metric and target agreed before modelling, such as recall of at least 0.7.
- **cross_val_predict:** returns, for every training row, the prediction from the CV round in which that row was held out.
- **Out-of-fold prediction:** a prediction for a row made by a model that didn't train on it.
- **Final test:** the single, last evaluation on the untouched test set.
- **Deliverable:** what the project hands over: the model, its honest numbers, explanations and limits.
mistakes:
- Starting with models before agreeing what success looks like.
- Choosing the threshold, the model or the features by looking at test scores.
- Reporting only the best number, without the baseline, the threshold or the limits.
