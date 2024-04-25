CREATE TABLE IF NOT EXISTS weather
                            (id INTEGER PRIMARY KEY, datetime TEXT,
                            cloud_cover INTEGER,
                            temperature REAL);

CREATE TABLE IF NOT EXISTS electricity_price
                            (id INTEGER PRIMARY KEY, datetime TEXT,
                            price REAL)