-- Sample tables for text-2-sql project

-- Create sample schema
CREATE SCHEMA IF NOT EXISTS sample;

-- Create users table
CREATE TABLE IF NOT EXISTS sample.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS sample.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS sample.orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES sample.users(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'pending'
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS sample.order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES sample.orders(id),
    product_id INT NOT NULL REFERENCES sample.products(id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Insert sample users
INSERT INTO sample.users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('bob_wilson', 'bob@example.com'),
('alice_johnson', 'alice@example.com');

-- Insert sample products
INSERT INTO sample.products (name, description, price, stock_quantity) VALUES
('Laptop', 'High-performance laptop for development', 1299.99, 15),
('Mouse', 'Wireless ergonomic mouse', 29.99, 50),
('Keyboard', 'Mechanical gaming keyboard', 129.99, 30),
('Monitor', '4K UHD Display', 399.99, 20),
('Webcam', 'Full HD webcam with microphone', 79.99, 25);

-- Insert sample orders
INSERT INTO sample.orders (user_id, total_amount, status) VALUES
(1, 1359.98, 'completed'),
(2, 509.98, 'pending'),
(3, 79.99, 'completed'),
(4, 1729.97, 'shipped');

-- Insert sample order items
INSERT INTO sample.order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 4, 1, 399.99),
(2, 3, 1, 129.99),
(3, 5, 1, 79.99),
(4, 1, 1, 1299.99),
(4, 3, 1, 129.99),
(4, 2, 1, 29.99);

-- Create indexes for better performance
CREATE INDEX idx_orders_user_id ON sample.orders(user_id);
CREATE INDEX idx_order_items_order_id ON sample.order_items(order_id);
CREATE INDEX idx_order_items_product_id ON sample.order_items(product_id);

-- Grant permissions (optional)
GRANT ALL PRIVILEGES ON SCHEMA sample TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sample TO postgres;
