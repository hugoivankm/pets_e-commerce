-- Initial manual PostgreSQL schema generated from the SQLAlchemy models

BEGIN;
SET LOCAL search_path TO public;

CREATE TABLE categories (
	id SERIAL NOT NULL,
	category_name VARCHAR(255) NOT NULL,
	category_description TEXT,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_categories PRIMARY KEY (id),
	CONSTRAINT uq_categories_category_name UNIQUE (category_name)
);

CREATE TABLE suppliers (
	id SERIAL NOT NULL,
	name VARCHAR(255) NOT NULL,
	contact_email VARCHAR(320),
	contact_phone VARCHAR(50),
	address TEXT,
	active BOOLEAN DEFAULT 'true' NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_suppliers PRIMARY KEY (id)
);

CREATE TABLE users (
	id SERIAL NOT NULL,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(320) NOT NULL,
	role VARCHAR(50) DEFAULT 'customer' NOT NULL,
	is_active BOOLEAN DEFAULT 'true' NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_users PRIMARY KEY (id),
	CONSTRAINT uq_users_email UNIQUE (email)
);

CREATE TABLE products (
	id SERIAL NOT NULL,
	name VARCHAR(255) NOT NULL,
	sku VARCHAR(100) NOT NULL,
	category_id INTEGER NOT NULL,
	description TEXT,
	price NUMERIC(12, 2) NOT NULL,
	stock INTEGER DEFAULT '0' NOT NULL,
	active BOOLEAN DEFAULT 'true' NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_products PRIMARY KEY (id),
	CONSTRAINT ck_products_price_non_negative CHECK (price >= 0),
	CONSTRAINT uq_products_sku UNIQUE (sku),
	CONSTRAINT fk_products_category_id_categories FOREIGN KEY(category_id) REFERENCES categories (id)
);

CREATE INDEX ix_products_category_id ON products (category_id);

CREATE TABLE stock_receipts (
	id SERIAL NOT NULL,
	supplier_id INTEGER NOT NULL,
	received_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	received_by INTEGER NOT NULL,
	notes TEXT,
	status VARCHAR(50) DEFAULT 'received' NOT NULL,
	CONSTRAINT pk_stock_receipts PRIMARY KEY (id),
	CONSTRAINT fk_stock_receipts_supplier_id_suppliers FOREIGN KEY(supplier_id) REFERENCES suppliers (id),
	CONSTRAINT fk_stock_receipts_received_by_users FOREIGN KEY(received_by) REFERENCES users (id)
);

CREATE INDEX ix_stock_receipts_supplier_id ON stock_receipts (supplier_id);

CREATE INDEX ix_stock_receipts_received_by ON stock_receipts (received_by);

CREATE TABLE carts (
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	status VARCHAR(50) DEFAULT 'active' NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_carts PRIMARY KEY (id),
	CONSTRAINT fk_carts_user_id_users FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_carts_user_id ON carts (user_id);

CREATE TABLE payment_methods (
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	method_type VARCHAR(50) NOT NULL,
	provider VARCHAR(100) NOT NULL,
	is_default BOOLEAN DEFAULT 'false' NOT NULL,
	is_active BOOLEAN DEFAULT 'true' NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_payment_methods PRIMARY KEY (id),
	CONSTRAINT fk_payment_methods_user_id_users FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_payment_methods_user_id ON payment_methods (user_id);

CREATE TABLE stock_movements (
	id SERIAL NOT NULL,
	product_id INTEGER NOT NULL,
	quantity_change INTEGER NOT NULL,
	type VARCHAR(50) NOT NULL,
	reason TEXT,
	reference_type VARCHAR(100),
	reference_id INTEGER,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_stock_movements PRIMARY KEY (id),
	CONSTRAINT ck_stock_movements_quantity_change_non_zero CHECK (quantity_change <> 0),
	CONSTRAINT fk_stock_movements_product_id_products FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE INDEX ix_stock_movements_product_id ON stock_movements (product_id);

CREATE TABLE stock_receipt_items (
	id SERIAL NOT NULL,
	stock_receipt_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	quantity_received INTEGER NOT NULL,
	unit_cost NUMERIC(12, 2) NOT NULL,
	CONSTRAINT pk_stock_receipt_items PRIMARY KEY (id),
	CONSTRAINT receipt_product UNIQUE (stock_receipt_id, product_id),
	CONSTRAINT ck_stock_receipt_items_quantity_received_positive CHECK (quantity_received > 0),
	CONSTRAINT ck_stock_receipt_items_unit_cost_non_negative CHECK (unit_cost >= 0),
	CONSTRAINT fk_stock_receipt_items_stock_receipt_id_stock_receipts FOREIGN KEY(stock_receipt_id) REFERENCES stock_receipts (id) ON DELETE CASCADE,
	CONSTRAINT fk_stock_receipt_items_product_id_products FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE INDEX ix_stock_receipt_items_product_id ON stock_receipt_items (product_id);

CREATE INDEX ix_stock_receipt_items_stock_receipt_id ON stock_receipt_items (stock_receipt_id);

CREATE TABLE cart_items (
	id SERIAL NOT NULL,
	cart_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	unit_price NUMERIC(12, 2) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_cart_items PRIMARY KEY (id),
	CONSTRAINT cart_product UNIQUE (cart_id, product_id),
	CONSTRAINT ck_cart_items_quantity_positive CHECK (quantity > 0),
	CONSTRAINT ck_cart_items_unit_price_non_negative CHECK (unit_price >= 0),
	CONSTRAINT fk_cart_items_cart_id_carts FOREIGN KEY(cart_id) REFERENCES carts (id) ON DELETE CASCADE,
	CONSTRAINT fk_cart_items_product_id_products FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE INDEX ix_cart_items_cart_id ON cart_items (cart_id);

CREATE INDEX ix_cart_items_product_id ON cart_items (product_id);

CREATE TABLE orders (
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	cart_id INTEGER NOT NULL,
	status VARCHAR(50) DEFAULT 'pending' NOT NULL,
	total_amount NUMERIC(12, 2) NOT NULL,
	payment_method_id INTEGER NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_orders PRIMARY KEY (id),
	CONSTRAINT ck_orders_total_amount_non_negative CHECK (total_amount >= 0),
	CONSTRAINT fk_orders_user_id_users FOREIGN KEY(user_id) REFERENCES users (id),
	CONSTRAINT fk_orders_cart_id_carts FOREIGN KEY(cart_id) REFERENCES carts (id),
	CONSTRAINT fk_orders_payment_method_id_payment_methods FOREIGN KEY(payment_method_id) REFERENCES payment_methods (id)
);

CREATE INDEX ix_orders_cart_id ON orders (cart_id);

CREATE INDEX ix_orders_user_id ON orders (user_id);

CREATE INDEX ix_orders_payment_method_id ON orders (payment_method_id);

CREATE TABLE invoices (
	id SERIAL NOT NULL,
	order_id INTEGER NOT NULL,
	invoice_number VARCHAR(100) NOT NULL,
	total NUMERIC(12, 2) NOT NULL,
	status VARCHAR(50) DEFAULT 'issued' NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_invoices PRIMARY KEY (id),
	CONSTRAINT ck_invoices_total_non_negative CHECK (total >= 0),
	CONSTRAINT uq_invoices_order_id UNIQUE (order_id),
	CONSTRAINT fk_invoices_order_id_orders FOREIGN KEY(order_id) REFERENCES orders (id),
	CONSTRAINT uq_invoices_invoice_number UNIQUE (invoice_number)
);

CREATE TABLE order_items (
	id SERIAL NOT NULL,
	order_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	unit_price NUMERIC(12, 2) NOT NULL,
	CONSTRAINT pk_order_items PRIMARY KEY (id),
	CONSTRAINT order_product UNIQUE (order_id, product_id),
	CONSTRAINT ck_order_items_quantity_positive CHECK (quantity > 0),
	CONSTRAINT ck_order_items_unit_price_non_negative CHECK (unit_price >= 0),
	CONSTRAINT fk_order_items_order_id_orders FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE,
	CONSTRAINT fk_order_items_product_id_products FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE INDEX ix_order_items_product_id ON order_items (product_id);

CREATE INDEX ix_order_items_order_id ON order_items (order_id);

CREATE TABLE payments (
	id SERIAL NOT NULL,
	order_id INTEGER NOT NULL,
	payment_method_id INTEGER NOT NULL,
	status VARCHAR(50) DEFAULT 'pending' NOT NULL,
	reference VARCHAR(255),
	amount NUMERIC(12, 2) NOT NULL,
	confirmed_at TIMESTAMP WITH TIME ZONE,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_payments PRIMARY KEY (id),
	CONSTRAINT ck_payments_amount_positive CHECK (amount > 0),
	CONSTRAINT fk_payments_order_id_orders FOREIGN KEY(order_id) REFERENCES orders (id),
	CONSTRAINT fk_payments_payment_method_id_payment_methods FOREIGN KEY(payment_method_id) REFERENCES payment_methods (id),
	CONSTRAINT uq_payments_reference UNIQUE (reference)
);

CREATE INDEX ix_payments_order_id ON payments (order_id);

CREATE INDEX ix_payments_payment_method_id ON payments (payment_method_id);

CREATE TABLE refunds (
	id SERIAL NOT NULL,
	payment_id INTEGER NOT NULL,
	reason VARCHAR(500) NOT NULL,
	amount NUMERIC(12, 2) NOT NULL,
	processed_at TIMESTAMP WITH TIME ZONE,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	CONSTRAINT pk_refunds PRIMARY KEY (id),
	CONSTRAINT ck_refunds_amount_positive CHECK (amount > 0),
	CONSTRAINT fk_refunds_payment_id_payments FOREIGN KEY(payment_id) REFERENCES payments (id)
);

CREATE INDEX ix_refunds_payment_id ON refunds (payment_id);

COMMIT;
