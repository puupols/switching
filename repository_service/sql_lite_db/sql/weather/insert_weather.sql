INSERT INTO weather (datetime, cloud_cover, temperature, latitude, longitude)
                SELECT :datetime, :cloud_cover, :temperature, :latitude, :longitude
WHERE NOT EXISTS (SELECT 1 FROM weather WHERE datetime = :datetime and latitude = :latitude and longitude = :longitude)