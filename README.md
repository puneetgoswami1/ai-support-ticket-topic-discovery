# Support Ticket Topic Discovery & CSAT Diagnostics

An NLP clustering workflow that groups unstructured customer support logs (chat, email, voice transcripts) into specific product issue buckets and tracks SLA and CSAT impact.

## Problem Context
Generic support tags like "Bug" or "Account Issue" hide recurring product regressions until ticket volume spikes. This project pairs SQL SLA/CSAT rollups with bi-gram TF-IDF and K-Means clustering to surface specific root-cause phrases from raw ticket text.

## Files
- `ticket_volume_aggregation.sql`: Computes first-contact resolution (FCR), SLA breach rates, and CSAT scores by topic cluster.
- `topic_discovery_nlp_engine.py`: Vectorizes 50k+ unstructured transcripts with bi-gram TF-IDF and extracts top keywords per cluster.
- `requirements.txt`: Python dependencies.

## How It Works
1. **Text Normalization:** Cleans raw multi-channel support transcripts and preserves two-word product phrases (e.g., "apple pay", "invalid otp").
2. **Unsupervised Grouping:** Clusters tickets into 5 operational friction themes without relying on manual agent tags.
3. **SLA & CSAT Impact:** Joins cluster assignments against resolution timestamps to highlight which issues hurt customer satisfaction most.

## Run Locally

    git clone https://github.com/puneetgoswami1/ai-support-ticket-topic-discovery.git
    cd ai-support-ticket-topic-discovery
    pip install -r requirements.txt
    python topic_discovery_nlp_engine.py
