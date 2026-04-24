CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE positions (
    position_id SERIAL PRIMARY KEY,
    position_name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    hire_date DATE NOT NULL,
    start_date DATE NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    supervisor_id INT NULL
);

ALTER TABLE employees
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

ALTER TABLE employees
ADD CONSTRAINT fk_position
FOREIGN KEY (position_id)
REFERENCES positions(position_id);

ALTER TABLE employees
ADD CONSTRAINT fk_supervisor
FOREIGN KEY (supervisor_id)
REFERENCES employees(employee_id);
