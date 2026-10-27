# AI Voice & Text Support Ticket Topic Discovery Engine

An unsupervised NLP embedding and clustering pipeline designed to ingest unstructured customer service transcripts (voice calls, live chat, email) and automatically group complaints into actionable product defect trends.

## Overview
Customer support teams manually tag incoming tickets with generic classifications (e.g. "Bug", "Account Issue"), masking acute product outages and regressions. This engine uses TF-IDF n-gram vectorization and K-Means clustering to parse 50,000+ unstructured interactions, exposing underlying operational bottlenecks and CSAT drop drivers.

## Project Structure
- `ticket_volume_aggregation.sql`: Production SQL pipeline calculating first-contact resolution (FCR), SLA breach frequencies, and CSAT scores across extracted topic clusters.
- `topic_discovery_nlp_engine.py`: Python NLP pipeline transforming raw text/voice transcripts into feature vectors and surfacing top discriminative root-cause keywords.
- `requirements.txt`: Python package dependencies.

## Key Analytical Workflows
1. **Unstructured Text Ingestion:** Preprocesses multi-channel inputs (ASR voice transcript logs, live chat sessions, support tickets).
2. **Feature Extraction:** Implements bi-gram TF-IDF (`ngram_range=(1,2)`) to preserve domain phrases (e.g., "apple pay", "force closes", "invalid otp").
3. **Cluster Taxonomy:** Automatically partitions unstructured logs into 5 core product friction areas with associated ticket volumes and CSAT sentiment impacts.

## How to Run

```bash
# Clone the repository
git clone [https://github.com/puneetgoswami1/ai-support-ticket-topic-discovery.git](https://github.com/puneetgoswami1/ai-support-ticket-topic-discovery.git)
cd ai-support-ticket-topic-discovery

# Install dependencies
pip install -r requirements.txt

# Run NLP topic discovery engine
python topic_discovery_nlp_engine.py