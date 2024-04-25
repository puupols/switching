INSERT INTO weather (datetime, cloud_cover, temperature)
                SELECT ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM weather WHERE datetime = ?)