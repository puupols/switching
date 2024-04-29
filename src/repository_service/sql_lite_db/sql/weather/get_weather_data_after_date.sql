SELECT  id as id,
        datetime as datetime,
        cloud_cover as cloud_cover,
        temperature as temperature,
        latitude as latitude,
        longitude as longitude,
        sunshine_duration as sunshine_duration
 FROM weather where datetime > :datetime