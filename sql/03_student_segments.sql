-- Descriptive size bands, specified for interpretability rather than predictive optimisation.
WITH segments AS (
  SELECT *, CASE WHEN student_count = 0 THEN '0'
                 WHEN student_count <= 10 THEN '1-10'
                 WHEN student_count <= 50 THEN '11-50'
                 ELSE '51+' END AS student_band,
            CASE WHEN student_count = 0 THEN 1 WHEN student_count <= 10 THEN 2
                 WHEN student_count <= 50 THEN 3 ELSE 4 END AS band_order
  FROM institutions
), grouped AS (
  SELECT student_band, band_order, COUNT(*) AS institutions,
         SUM(churn_label) AS churn_labelled, SUM(1-churn_label) AS active_labelled,
         100.0 * AVG(churn_label) AS churn_label_share_pct
  FROM segments GROUP BY student_band, band_order
)
SELECT *, 100.0 * churn_labelled / SUM(churn_labelled) OVER () AS share_of_churn_labels_pct
FROM grouped ORDER BY band_order;
