-- Groups can overlap. Counts must not be summed as distinct institutions.
SELECT 'Positive score; all six counts zero' AS review_group, COUNT(*) AS institutions
FROM institutions WHERE engagement_score > 0 AND attendance_count = 0 AND material_count = 0
  AND assessment_count = 0 AND teacher_count = 0 AND student_count = 0 AND class_count = 0
UNION ALL
SELECT 'Materials recorded; score zero', COUNT(*) FROM institutions WHERE material_count > 0 AND engagement_score = 0
UNION ALL
SELECT 'Active label; no students recorded', COUNT(*) FROM institutions WHERE churn_label = 0 AND student_count = 0
UNION ALL
SELECT 'Active label; no teacher or no class recorded', COUNT(*) FROM institutions
WHERE churn_label = 0 AND (teacher_count = 0 OR class_count = 0)
UNION ALL
SELECT 'Active label; no materials recorded', COUNT(*) FROM institutions WHERE churn_label = 0 AND material_count = 0;
