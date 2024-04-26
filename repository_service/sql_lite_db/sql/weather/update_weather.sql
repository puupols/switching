UPDATE weather SET
    cloud_cover = :cloud_cover,
    temperature = :temperature
WHERE datetime = :datetime AND latitude = :latitude AND longitude = :longitude