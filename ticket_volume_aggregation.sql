-- =====================================================================
-- CUSTOMER SUPPORT TOPIC & ESCALATION TRIAGE PIPELINE
-- Author: Puneet Goswami
-- Description: Aggregates multi-channel support tickets (Voice/Chat/Email),
--              calculates first-contact resolution (FCR), and tags SLA breaches.
-- =====================================================================

WITH ticket_events_normalized AS (
    SELECT 
        ticket_id,
        customer_id,
        channel, -- 'VOICE_TRANSCRIPT', 'LIVE_CHAT', 'EMAIL'
        created_at,
        first_response_at,
        resolved_at,
        status,
        csat_score,
        predicted_topic_cluster,
        
        -- First response time in minutes
        DATEDIFF('minute', created_at, first_response_at) AS first_response_minutes,
        
        -- Full resolution duration in hours
        ROUND(DATEDIFF('minute', created_at, resolved_at) / 60.0, 2) AS resolution_hours,
        
        -- Flag SLA breach (Standard: first response under 15 mins for Chat/Voice)
        CASE 
            WHEN channel IN ('VOICE_TRANSCRIPT', 'LIVE_CHAT') AND DATEDIFF('minute', created_at, first_response_at) > 15 THEN 1
            WHEN channel = 'EMAIL' AND DATEDIFF('minute', created_at, first_response_at) > 120 THEN 1
            ELSE 0 
        END AS is_sla_breached
    FROM support_dw.fct_support_tickets
    WHERE created_at >= CURRENT_DATE - INTERVAL '90 DAYS'
),

topic_cluster_performance AS (
    SELECT 
        predicted_topic_cluster,
        channel,
        COUNT(DISTINCT ticket_id) AS total_ticket_volume,
        ROUND(AVG(first_response_minutes), 1) AS avg_first_response_min,
        ROUND(AVG(resolution_hours), 2) AS avg_resolution_time_hrs,
        ROUND(AVG(csat_score), 2) AS avg_csat_rating,
        SUM(is_sla_breached) AS total_sla_violations,
        ROUND((SUM(is_sla_breached) * 100.0) / COUNT(ticket_id), 2) AS sla_violation_rate_pct
    FROM ticket_events_normalized
    GROUP BY predicted_topic_cluster, channel
)

SELECT 
    predicted_topic_cluster,
    channel,
    total_ticket_volume,
    avg_first_response_min,
    avg_resolution_time_hrs,
    avg_csat_rating,
    total_sla_violations,
    sla_violation_rate_pct,
    
    -- Severity ranking for engineering prioritization
    CASE 
        WHEN sla_violation_rate_pct >= 20.0 OR avg_csat_rating < 3.2 THEN 'CRITICAL_PRODUCT_DEFECT'
        WHEN sla_violation_rate_pct >= 10.0 THEN 'HIGH_OPERATIONAL_LOAD'
        ELSE 'STABLE_WORKFLOW'
    END AS operational_severity_tier
FROM topic_cluster_performance
ORDER BY total_ticket_volume DESC;