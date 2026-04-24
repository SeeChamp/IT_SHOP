
-- สร้างตารางสำหรับ Data Warehouse
-- ตาราง Dimension
CREATE TABLE product_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

-- ตาราง Dimension
CREATE TABLE customer_dim (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
    
);

-- ตาราง Dimension
CREATE TABLE date_dim (
    date_id INT PRIMARY KEY NOT NULL,
    date DATE,
    year INT,
    month INT,
    day INT
);

-- ตาราง Fact 
CREATE TABLE sales_fact (
    sale_id SERIAL PRIMARY KEY,
    date_id INT,
    product_id INT,
    customer_id INT,
    quantity INT,
    sales_amount DECIMAL(10,2),

    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (product_id) REFERENCES product_dim(product_id),
    FOREIGN KEY (customer_id) REFERENCES customer_dim(customer_id)
);

    
