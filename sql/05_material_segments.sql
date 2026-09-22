SELECT CASE WHEN material_count > 0 THEN 'Materials recorded' ELSE 'No materials recorded' END AS segment,
       COUNT(*) AS institutions, SUM(churn_label) AS churn_labelled,
       SUM(1-churn_label) AS active_labelled,
       100.0 * AVG(churn_label) AS churn_label_share_pct
FROM institutions GROUP BY segment ORDER BY segment;
