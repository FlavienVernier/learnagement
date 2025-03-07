CREATE VIEW MRDBF_link_table AS
SELECT `TABLE_NAME` AS `TABLE_NAME`
FROM `information_schema`.`KEY_COLUMN_USAGE`
WHERE `TABLE_SCHEMA` = 'learnagement'
    AND `CONSTRAINT_NAME` = 'PRIMARY'
GROUP BY `TABLE_NAME`
HAVING count(0) = 2;

CREATE VIEW MRDBF_linked_table AS
SELECT DISTINCT `KEY_COLUMN_USAGE`.`TABLE_NAME` AS `TABLE_NAME`
FROM `information_schema`.`KEY_COLUMN_USAGE`
WHERE `REFERENCED_TABLE_SCHEMA` = 'learnagement'
    AND `TABLE_NAME` NOT IN (SELECT `TABLE_NAME` FROM `learnagement`.`MRDBF_link_table`);


CREATE VIEW MRDBF_leaf_table AS
SELECT table_name 
FROM information_schema.tables
WHERE TABLE_SCHEMA = "learnagement" 
    AND table_type = "BASE TABLE"
    AND TABLE_NAME NOT IN (SELECT * FROM learnagement.MRDBF_link_table)
    AND TABLE_NAME NOT IN (SELECT * FROM learnagement.MRDBF_linked_table);
