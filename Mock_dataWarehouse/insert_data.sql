
INSERT INTO product_dim (product_id, product_name, category, price)
SELECT 
    generate_series(101,110),
    'Product_' || generate_series(101,110),
    CASE 
        WHEN random() > 0.5 THEN 'Drinks'
        ELSE 'Desserts'
    END,
    (random()*100)::int + 20;

INSERT INTO customer_dim (customer_id, customer_name, city)
SELECT 
    generate_series(201,220),
    'Customer_' || generate_series(201,220),
    (ARRAY[
        Bangkok, 
        Chiang Mai, 
        Phuket, 
        Khon Kaen, 
        Nakhon Ratchasima,
        Udon Thani,
        Surat Thani,
        Nakhon Si Thammarat,
        Chonburi,
        Rayong
    ])floor(random()*10 + 1);

INSERT INTO date_dim (date_id, date, year, month, day)
SELECT 
    TO_CHAR(d, 'YYYYMMDD')::INT,
    d,
    EXTRACT(YEAR FROM d),
    EXTRACT(MONTH FROM d),
    EXTRACT(DAY FROM d)
FROM generate_series(
    DATE '2026-01-01',
    DATE '2026-03-31',
    INTERVAL '1 day'
) AS d
ON CONFLICT (date_id) DO NOTHING;




INSERT INTO sales_fact (date_id, product_id, customer_id, quantity, sales_amount)
SELECT 
    TO_CHAR(d, 'YYYYMMDD')::INT,
    101 + (random()*2)::int,
    201 + (random()*2)::int,
    (random()*5)::int + 1,
    (random()*100)::int + 20
FROM generate_series(
    DATE '2026-01-01',
    DATE '2026-03-31',
    INTERVAL '1 day'
) d;


-- insert sales_fact แบบ manual (ไม่แนะนำสำหรับข้อมูลจำนวนมาก)
/*INSERT INTO sales_fact (sale_id, date_id, product_id, customer_id, quantity, sales_amount) VALUES
(1, 20260101, 101, 201, 2, 50.00),
(2, 20260102, 102, 202, 1, 30.00),
(3, 20260103, 103, 203, 3, 90.00);*/
