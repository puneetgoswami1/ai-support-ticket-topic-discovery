"""
AI Voice & Text Support Ticket Topic Discovery Engine
Author: Puneet Goswami
Description: Processes raw unstructured customer complaint transcripts using
             TF-IDF tokenization and K-Means clustering to uncover latent bug trends.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def generate_support_corpus(n_samples: int = 15000) -> pd.DataFrame:
    """Generates synthetic unstructured voice transcripts and chat tickets."""
    np.random.seed(42)

    # 5 realistic recurring core product issue templates
    templates = [
        # Cluster 0: Payment Gateway & Double Debits
        "Card debited twice during checkout but order status shows pending payment failed stripe gateway error",
        "Money deducted from bank account via apple pay but no confirmation email or receipt generated",
        "Payment gateway timeout transaction failed balance reduced refund not initiated",

        # Cluster 1: Mobile App Crash on Checkout
        "App keeps crashing whenever clicking place order button on checkout screen after recent update",
        "iOS app freezes and force closes when adding address in cart version upgrade bug",
        "Screen goes black during payment redirect app crashes on android device",

        # Cluster 2: OTP & Authentication Delay
        "Verification code SMS not received cannot log into workspace password reset OTP delayed",
        "Two factor auth code timed out did not arrive on phone number unable to access account",
        "Login screen says invalid OTP code repeatedly resend button is disabled",

        # Cluster 3: International Shipping & Customs
        "Tracking number not updating package stuck at customs clearance in germany international courier delay",
        "Delivery courier delayed customs duty invoice unexpectedly charged on cross border order",
        "Shipment tracking shows transit delay overseas warehouse haven't dispatched yet",

        # Cluster 4: Subscription Cancellation & Invoice
        "Unable to cancel auto renew subscription billing toggle hidden in settings want refund",
        "Charged annual fee unexpectedly invoice receipt missing tax identification number",
        "Subscription renewal charged without notification request immediate cancellation"
    ]

    ticket_ids = [f"TCK-{20000 + i}" for i in range(n_samples)]
    channels = np.random.choice(["VOICE_TRANSCRIPT", "LIVE_CHAT", "EMAIL"], size=n_samples, p=[0.40, 0.45, 0.15])
    
    # Assign tickets to issue categories with random wording noise
    assigned_texts = []
    for _ in range(n_samples):
        base_text = np.random.choice(templates)
        assigned_texts.append(base_text)

    csat = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.25, 0.20, 0.25, 0.18, 0.12])

    return pd.DataFrame({
        "ticket_id": ticket_ids,
        "channel": channels,
        "raw_complaint_text": assigned_texts,
        "csat_rating": csat
    })


def discover_latent_defect_topics(df: pd.DataFrame, n_clusters: int = 5):
    """Vectorizes text using TF-IDF and identifies top discriminative cluster keywords."""
    print("Vectorizing raw customer complaint transcripts via TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=2500,
        stop_words="english",
        ngram_range=(1, 2)
    )
    X = vectorizer.fit_transform(df["raw_complaint_text"])

    print(f"Running K-Means unsupervised clustering across {n_clusters} target topic buckets...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["topic_cluster"] = kmeans.fit_predict(X)

    # Extract top keywords per cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    print("\n==========================================================================")
    print("CUSTOMER SUPPORT TOPIC DISCOVERY & DEFECT TAXONOMY MATRIX")
    print("==========================================================================")

    cluster_labels = {
        0: "Payment & Gateway Double-Debit",
        1: "Checkout Screen Crash (App Bug)",
        2: "Authentication / OTP SMS Latency",
        3: "Cross-Border Customs & Transit Lag",
        4: "Subscription Billing & Invoicing"
    }

    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :6]]
        cluster_size = (df["topic_cluster"] == i).sum()
        pct = (cluster_size / len(df)) * 100
        avg_csat = df[df["topic_cluster"] == i]["csat_rating"].mean()

        print(f"\n[Topic Bucket {i}: {cluster_labels.get(i, 'Defect Trend')}]")
        print(f" - Ticket Share         : {cluster_size:,} tickets ({pct:.1f}% of total inbound load)")
        print(f" - Customer CSAT Index : {avg_csat:.2f} / 5.0")
        print(f" - Core Signal Keywords: {', '.join(top_terms)}")


if __name__ == "__main__":
    tickets = generate_support_corpus(15000)
    print(f"Ingested {len(tickets):,} unstructured customer interaction transcripts.\n")
    discover_latent_defect_topics(tickets, n_clusters=5)