from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

def create_semantic_entries(emr_list):
    mi_attributes = ['diagnosis', 'treatment', 'results']
    semantic_entries = []

    for emr in emr_list:
        mi_data = "; ".join(getattr(emr, attr) for attr in mi_attributes)
        semantic_entries.append(mi_data)

    return semantic_entries

def create_clusters(semantic_entries, entries_per_cluster=200):
    n_clusters = len(semantic_entries) // entries_per_cluster or 1
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    corpus_embeddings = embedder.encode(semantic_entries)

    clustering_model = KMeans(n_clusters=n_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(n_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append((sentence_id, semantic_entries[sentence_id]))

    return clustered_sentences