UPDATE weather SET
    cloud_cover = :cloud_cover,
    temperature = :temperature,
    sunshine_duration = :sunshine_duration
WHERE datetime = :datetime AND latitude = :latitude AND longitude = :longitude