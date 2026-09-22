-- Field values are snapshot counts, not monthly usage rates.
WITH long_metrics AS (
  SELECT i.institution_id, i.churn_label, m.metric, m.value
  FROM institutions i,
  LATERAL (VALUES
    ('attendance_count', CAST(attendance_count AS DOUBLE)),
    ('material_count', CAST(material_count AS DOUBLE)),
    ('assessment_count', CAST(assessment_count AS DOUBLE)),
    ('teacher_count', CAST(teacher_count AS DOUBLE)),
    ('student_count', CAST(student_count AS DOUBLE)),
    ('class_count', CAST(class_count AS DOUBLE)),
    ('engagement_score', engagement_score)
  ) m(metric, value)
)
SELECT churn_label, metric, COUNT(*) AS institutions, SUM(value) AS total,
       AVG(value) AS mean, MEDIAN(value) AS median,
       QUANTILE_CONT(value, 0.25) AS p25, QUANTILE_CONT(value, 0.75) AS p75,
       SUM(CASE WHEN value > 0 THEN 1 ELSE 0 END) AS positive_count,
       100.0 * AVG(CASE WHEN value > 0 THEN 1.0 ELSE 0.0 END) AS positive_share_pct
FROM long_metrics GROUP BY churn_label, metric ORDER BY churn_label, metric;
