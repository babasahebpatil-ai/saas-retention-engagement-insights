-- One row per anonymised educational institution; not subscriptions or users.
-- A label share across this snapshot is not a monthly churn rate.
SELECT COUNT(*) AS institutions,
       COUNT(DISTINCT institution_id) AS unique_institutions,
       SUM(CASE WHEN churn_label = 1 THEN 1 ELSE 0 END) AS churn_labelled,
       SUM(CASE WHEN churn_label = 0 THEN 1 ELSE 0 END) AS active_labelled,
       100.0 * AVG(churn_label) AS churn_label_share_pct,
       SUM(student_count) AS recorded_students,
       SUM(teacher_count) AS recorded_teachers,
       SUM(class_count) AS recorded_classes,
       SUM(material_count) AS recorded_materials
FROM institutions;
