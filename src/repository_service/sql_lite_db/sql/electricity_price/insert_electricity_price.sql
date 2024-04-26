INSERT INTO electricity_price (datetime, price)
                SELECT :datetime, :price
WHERE NOT EXISTS (SELECT 1 FROM electricity_price WHERE datetime = :datetime)