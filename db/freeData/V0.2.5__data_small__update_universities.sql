INSERT INTO `MOB_partner_university_places` (`id_partner_university`, `id_promo`, `number_of_places`)
SELECT id_partner_university, 15, S8_IDU FROM MOB_partner_university WHERE S8_IDU > 0 AND S8_IDU IS NOT NULL UNION ALL
SELECT id_partner_university, 16, S9_IDU FROM MOB_partner_university WHERE S9_IDU > 0 AND S9_IDU IS NOT NULL UNION
SELECT id_partner_university, 18, S8_MM FROM MOB_partner_university WHERE S8_MM > 0 AND S8_MM IS NOT NULL UNION ALL
SELECT id_partner_university, 19, S9_MM FROM MOB_partner_university WHERE S9_MM > 0 AND S9_MM IS NOT NULL UNION ALL
SELECT id_partner_university, 21, S8_SNI FROM MOB_partner_university WHERE S8_SNI > 0 AND S8_SNI IS NOT NULL UNION ALL
SELECT id_partner_university, 22, S9_SNI FROM MOB_partner_university WHERE S9_SNI > 0 AND S9_SNI IS NOT NULL UNION ALL
SELECT id_partner_university, 24, S8_BAT FROM MOB_partner_university WHERE S8_BAT > 0 AND S8_BAT IS NOT NULL UNION ALL
SELECT id_partner_university, 25, S9_BAT FROM MOB_partner_university WHERE S9_BAT > 0 AND S9_BAT IS NOT NULL UNION ALL
SELECT id_partner_university, 27, S8_EIT FROM MOB_partner_university WHERE S8_EIT > 0 AND S8_EIT IS NOT NULL UNION ALL
SELECT id_partner_university, 28, S9_EIT FROM MOB_partner_university WHERE S9_EIT > 0 AND S9_EIT IS NOT NULL UNION ALL
SELECT id_partner_university, 30, S8_MC FROM MOB_partner_university WHERE S8_MC > 0 AND S8_MC IS NOT NULL UNION ALL
SELECT id_partner_university, 31, S9_MC FROM MOB_partner_university WHERE S9_MC > 0 AND S9_MC IS NOT NULL;

ALTER TABLE `MOB_partner_university`
    DROP COLUMN `S8_total_places`,
    DROP COLUMN `S8_MM`,
    DROP COLUMN `S8_MC`,
    DROP COLUMN `S8_MMT`,
    DROP COLUMN `S8_SNI`,
    DROP COLUMN `S8_BAT`,
    DROP COLUMN `S8_EIT`,
    DROP COLUMN `S8_IDU`,
    DROP COLUMN `S8_ESB`,
    DROP COLUMN `S8_AM`,
    DROP COLUMN `S9_total_places`,
    DROP COLUMN `S9_MM`,
    DROP COLUMN `S9_MC`,
    DROP COLUMN `S9_MMT`,
    DROP COLUMN `S9_SNI`,
    DROP COLUMN `S9_BAT`,
    DROP COLUMN `S9_EIT`,
    DROP COLUMN `S9_IDU`,
    DROP COLUMN `S9_ESB`,
    DROP COLUMN `S9_AM`;