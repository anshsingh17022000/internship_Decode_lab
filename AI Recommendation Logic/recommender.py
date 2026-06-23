"""
recommender.py
================
DecodeLabs | Project 3 - AI Recommendation Logic
The "Digital Matchmaker" - A Content-Based Filtering Engine

This module implements the full logic skeleton described in the training kit:

    INPUT (User State) -> PROCESS (Similarity Logic) -> OUTPUT (Top-N List)

Pipeline (4 steps):
    1. Ingestion  - capture user skills (min 3 required)
    2. Scoring    - TF-IDF vectorization + Cosine Similarity against every item
    3. Sorting    - rank items by descending similarity score
    4. Filtering  - truncate to Top-N to avoid choice overload

No external ML libraries are used - every formula (TF, IDF, dot product,
magnitude, cosine) is implemented from scratch so the math stays visible.
"""

import csv
import math
from collections import Counter


class ColdStartError(Exception):
    """Raised when the user profile shares zero vocabulary with any item."""
    pass


class TechStackRecommender:
    """
    A content-based recommendation engine.

    Items   = job roles (e.g. "DevOps Engineer")
    Features = skill tags (e.g. "Python", "Docker")

    The engine maps both items and the user profile into the SAME shared
    vocabulary space, weights that space with TF-IDF, and ranks items by
    the cosine angle between the user vector and each item vector.
    """

    # Fallback used for the "User Cold Start" problem (Slide 21: Trending Fallback)
    TRENDING_FALLBACK = ["Full Stack Developer", "Data Scientist", "DevOps Engineer"]

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.items = self._load_dataset(dataset_path)        # [{role, skills:set}]
        self.vocabulary = self._build_vocabulary(self.items)
        self.idf = self._compute_idf(self.items, self.vocabulary)
        self.item_vectors = {
            item["role"]: self._vectorize(item["skills"])
            for item in self.items
        }

    # ------------------------------------------------------------------ #
    # STEP 0 (setup): Load + normalize the dataset
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize(tag: str) -> str:
        """Lowercase + strip so 'Python', 'python ', ' PYTHON' all match."""
        return tag.strip().lower()

    def _load_dataset(self, path: str):
        items = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skills = {self._normalize(s) for s in row["skills"].split("|") if s.strip()}
                items.append({"role": row["role"].strip(), "skills": skills})
        return items

    @staticmethod
    def _build_vocabulary(items):
        """The shared vocabulary space every vector must map into (Slide 9)."""
        vocab = set()
        for item in items:
            vocab |= item["skills"]
        return sorted(vocab)

    # ------------------------------------------------------------------ #
    # TF-IDF WEIGHTING (Slides 10-12)
    # ------------------------------------------------------------------ #
    def _compute_idf(self, items, vocabulary):
        """
        IDF = log( total_documents / documents_containing_term )

        Penalizes generic skills that appear in almost every role
        (e.g. "Git") and rewards rare, descriptive ones (e.g. "Terraform").
        """
        n_docs = len(items)
        idf = {}
        for term in vocabulary:
            docs_with_term = sum(1 for item in items if term in item["skills"])
            # +1 smoothing guards against division by zero / log(0) edge cases
            idf[term] = math.log(n_docs / docs_with_term) if docs_with_term else 0.0
        return idf

    def _vectorize(self, skill_set):
        """
        Turns a set of skills into a TF-IDF weighted vector (dict: term -> weight).

        TF = (count of term in doc) / (total terms in doc)
        For our tag-based profiles each term appears once, so TF = 1 / len(doc).
        """
        if not skill_set:
            return {}
        tf = 1.0 / len(skill_set)
        return {
            term: tf * self.idf.get(term, 0.0)
            for term in skill_set
            if term in self.idf
        }

    # ------------------------------------------------------------------ #
    # COSINE SIMILARITY (Slides 13-16)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _cosine_similarity(vec_a: dict, vec_b: dict) -> float:
        """
        cos(theta) = (A . B) / (||A|| * ||B||)

        Invariant to vector magnitude -> measures ORIENTATION, not size.
        This is why a short user profile can still match a richly-tagged
        item with a high score, unlike raw Euclidean distance.
        """
        if not vec_a or not vec_b:
            return 0.0

        shared_terms = vec_a.keys() & vec_b.keys()
        dot_product = sum(vec_a[t] * vec_b[t] for t in shared_terms)

        mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
        mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

        if mag_a == 0 or mag_b == 0:
            return 0.0

        return dot_product / (mag_a * mag_b)

    # ------------------------------------------------------------------ #
    # THE 4-STEP RANKING PIPELINE (Slides 17-19)
    # ------------------------------------------------------------------ #
    def recommend(self, user_skills, top_n: int = 3):
        """
        Runs the full IPO pipeline and returns the Top-N matched roles.

        Returns a list of tuples: (role_name, score_percentage, matched_skills)
        """
        # --- Step 1: Ingestion ---
        if len(user_skills) < 3:
            raise ValueError("Project 3 requires a minimum of 3 user skills for accurate matching.")

        normalized_input = [self._normalize(s) for s in user_skills]
        recognized = [s for s in normalized_input if s in self.vocabulary]
        unrecognized = [s for s in normalized_input if s not in self.vocabulary]

        user_vector = self._vectorize(set(recognized))

        # --- Cold Start handling (Slide 20-21) ---
        if not recognized:
            fallback = [
                (role, 0.0, [])
                for role in self.TRENDING_FALLBACK[:top_n]
            ]
            return {
                "cold_start": True,
                "unrecognized": unrecognized,
                "results": fallback,
            }

        # --- Step 2: Scoring ---
        scored = []
        for item in self.items:
            score = self._cosine_similarity(user_vector, self.item_vectors[item["role"]])
            matched = sorted(item["skills"] & set(recognized))
            scored.append((item["role"], score, matched))

        # --- Step 3: Sorting ---
        scored.sort(key=lambda x: x[1], reverse=True)

        # --- Step 4: Filtering ---
        top_results = scored[:top_n]

        return {
            "cold_start": False,
            "unrecognized": unrecognized,
            "results": [(role, round(score * 100, 1), matched) for role, score, matched in top_results],
        }

    def list_known_skills(self):
        """Utility: show the full vocabulary the engine understands."""
        return self.vocabulary
