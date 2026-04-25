-- =========================================================
-- 为默认用户创建储物柜
-- =========================================================

-- 为 person_id = 1 (我) 创建默认柜子
INSERT INTO storage_units (person_id, name, location, description)
VALUES (1, '默认柜子', '卧室', '我的衣柜')
ON CONFLICT (id) DO NOTHING;

-- 为 person_id = 2 (妈) 创建默认柜子
INSERT INTO storage_units (person_id, name, location, description)
VALUES (2, '默认柜子', '卧室', '妈妈的衣柜')
ON CONFLICT (id) DO NOTHING;

-- 为 person_id = 3 (爸) 创建默认柜子
INSERT INTO storage_units (person_id, name, location, description)
VALUES (3, '默认柜子', '卧室', '爸爸的衣柜')
ON CONFLICT (id) DO NOTHING;

-- 查看结果
SELECT 
    s.id,
    s.person_id,
    s.name,
    s.location,
    s.created_at
FROM storage_units s
ORDER BY s.person_id;
