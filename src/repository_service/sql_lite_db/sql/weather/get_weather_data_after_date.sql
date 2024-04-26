SELECT  id as id,
        datetime as datetime,
        cloud_cover as cloud_cover,
        temperature as temperature,
        latitude as latitude,
        longitude as longitude
 FROM weather where datetime > :datetime