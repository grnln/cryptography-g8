from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh import qparser, query

from noscuramus.settings import ENCRYPTED_INDEX_DIR, PLAIN_INDEX_DIR
from collections import Counter

from .cipher import *

import os
import whoosh.scoring as scoring

def encrypted_search(keywords):
    ids = dict()

    for _, _, files in os.walk(ENCRYPTED_INDEX_DIR):
        for file in files:
            with open(os.path.join(ENCRYPTED_INDEX_DIR, file), mode = 'r') as f:
                for line in f.readlines():
                    for keyword in keywords:
                        if str(hash_word(keyword.lower().strip())) == line.strip():
                            if keyword in ids:
                                ids[keyword].add(int(file.split('.')[0].strip()))
                            else:
                                ids[keyword] = {int(file.split('.')[0].strip())}
    return ids

def plain_search(keywords):
    ids = []
    index = open_dir(PLAIN_INDEX_DIR)
    keywords_string = ' OR '.join([k.lower().strip() for k in keywords])

    with index.searcher(weighting = scoring.BM25F()) as searcher:
        parser = MultifieldParser(['diagnosis', 'treatment', 'results'], schema = index.schema)
        results = searcher.search(parser.parse(keywords_string), limit = None)
        
        ids = [(int(row['id']), row.score) for row in results]
    return ids

def hybrid_search(keywords):
    all_matches = []

    encrypted_ids = encrypted_search(keywords)
    plain_ids = plain_search(keywords)

    ranked = []

    for key in encrypted_ids.keys():
        all_matches.extend(list(encrypted_ids[key]))

    encrypted_ids_freqs = Counter(all_matches)

    for id, score in plain_ids:
        if id in encrypted_ids_freqs:
            ranked.append((id, score * encrypted_ids_freqs[id]))
        else:
            ranked.append((id, score))

    for id, k in encrypted_ids_freqs.items():
        if id not in [t[0] for t in ranked]:
            ranked.append((id, k))

    return dict(ranked)