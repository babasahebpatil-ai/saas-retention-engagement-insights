SELECT churn_label,
       CASE WHEN churn_label = 0 THEN 'Active-labelled' ELSE 'Churn-labelled' END AS label,
       COUNT(*) AS institutions,
       100.0 * COUNT(*) / SUM(COUNT(*)) OVER () AS share_pct
FROM institutions
GROUP BY churn_label
ORDER BY churn_label;
