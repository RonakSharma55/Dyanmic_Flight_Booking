
-- ================================================
--  PostgreSQL Flight Booking Simulator
--  Database: flight_sim
-- ================================================



CREATE TABLE flights_flight (
    id SERIAL PRIMARY KEY,
    airline VARCHAR(100),
    origin VARCHAR(10),
    destination VARCHAR(10),
    duration_minutes INT,
    base_fare NUMERIC(10,2)
);

CREATE TABLE flights_schedule (
    id SERIAL PRIMARY KEY,
    flight_id INT REFERENCES flights_flight(id) ON DELETE CASCADE,
    departure_datetime TIMESTAMP,
    arrival_datetime TIMESTAMP,
    seats_available INT,
    demand_factor NUMERIC(5,2)
);

-- ================================================
--  30 Sample Flights
-- ================================================
INSERT INTO flights_flight (airline, origin, destination, duration_minutes, base_fare) VALUES
('IndiGo', 'DEL', 'BOM', 130, 4500),
('Air India', 'DEL', 'BLR', 155, 5200),
('Vistara', 'BLR', 'DEL', 160, 5300),
('GoAir', 'DEL', 'HYD', 140, 4100),
('SpiceJet', 'DEL', 'PNQ', 120, 3900),
('AirAsia', 'BOM', 'DEL', 135, 4700),
('IndiGo', 'BLR', 'HYD', 70, 2800),
('Vistara', 'DEL', 'CCU', 150, 5000),
('GoAir', 'CCU', 'DEL', 155, 4800),
('Air India', 'DEL', 'MAA', 165, 5500),
('Akasa Air', 'BOM', 'BLR', 90, 3200),
('IndiGo', 'HYD', 'BLR', 75, 2900),
('SpiceJet', 'MAA', 'DEL', 160, 5200),
('AirAsia', 'BLR', 'BOM', 95, 3100),
('GoAir', 'DEL', 'AMD', 115, 3500),
('Vistara', 'AMD', 'DEL', 120, 3600),
('IndiGo', 'DEL', 'PAT', 130, 4000),
('Air India', 'PAT', 'DEL', 130, 4200),
('SpiceJet', 'DEL', 'LKO', 75, 2800),
('Vistara', 'LKO', 'DEL', 80, 2900),
('AirAsia', 'BLR', 'MAA', 60, 2500),
('GoAir', 'MAA', 'BLR', 60, 2500),
('IndiGo', 'DEL', 'GOI', 135, 4700),
('Air India', 'GOI', 'DEL', 140, 4900),
('Vistara', 'BOM', 'CCU', 170, 5600),
('IndiGo', 'CCU', 'BOM', 165, 5500),
('SpiceJet', 'DEL', 'BBI', 120, 4100),
('GoAir', 'BBI', 'DEL', 130, 4200),
('AirAsia', 'BLR', 'CCU', 160, 5400),
('Vistara', 'CCU', 'BLR', 155, 5300);

-- ================================================
--  Generate schedules dynamically (3 days)
-- ================================================
DO $$
DECLARE
    f RECORD;
    d INT;
    dep TIMESTAMP;
    arr TIMESTAMP;
    seat_count INT;
    demand NUMERIC(5,2);
BEGIN
    FOR f IN SELECT * FROM flights_flight LOOP
        FOR d IN 0..2 LOOP
            dep := NOW() + (d || ' days')::INTERVAL + ((random() * 8 + 6) || ' hours')::INTERVAL;
            arr := dep + (f.duration_minutes || ' minutes')::INTERVAL;
            seat_count := 150 - floor(random() * 50); -- 100–150 seats
            demand := round((0.7 + random() * 0.6)::NUMERIC, 2); -- 0.7–1.3
            INSERT INTO flights_schedule (flight_id, departure_datetime, arrival_datetime, seats_available, demand_factor)
            VALUES (f.id, dep, arr, seat_count, demand);
        END LOOP;
    END LOOP;
END $$;
