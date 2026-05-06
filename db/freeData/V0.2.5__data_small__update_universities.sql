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
