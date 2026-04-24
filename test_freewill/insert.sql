
INSERT INTO departments (department_name)
VALUES ('แผนกไอที'), ('แผนกทรัพยากรบุคคล'), ('แผนกการเงิน');


INSERT INTO positions (position_name)
VALUES ('เจ้าของบริษัท'), ('ผู้จัดการ'), ('พนักงาน');


INSERT INTO employees (
    first_name, last_name, birth_date,
    hire_date, start_date, salary,
    department_id, position_id, supervisor_id
)
VALUES (
    'ณัฐพงษ์', 'คงมั่น', '1985-02-15',
    '2000-05-22','2000-05-22', 123456,
    1, 1, NULL
);


INSERT INTO employees (
    first_name, last_name, birth_date,
    hire_date, start_date, salary,
    department_id, position_id, supervisor_id
)
VALUES (
    'นางสาวอิศรา', 'ฎรัณกุล', '1992-08-10',
    '2017-07-01','2017-07-01', 60000,
    1, 2, 1
);


INSERT INTO employees (
    first_name, last_name, birth_date,
    hire_date, start_date, salary,
    department_id, position_id, supervisor_id
)
VALUES (
    'นายศรัณ', 'ก้าวหน้า', '1990-04-07',
    '2015-08-01','2015-08-01', 80000,
    1, 3, 2
);

INSERT INTO employees (
    first_name, last_name, birth_date,
    hire_date, start_date, salary,
    department_id, position_id, supervisor_id
)
VALUES (
    'นายว่องไว', 'ไวดี', '1988-03-10',
    '2012-01-01','2012-01-01', 60000,
    1, 2, 1
);


INSERT INTO employees (
    first_name, last_name, birth_date,
    hire_date, start_date, salary,
    department_id, position_id, supervisor_id
)
VALUES (
    'นางสาวกรกต', 'ย่างไว', '1995-06-20',
    '2020-02-01','2020-02-01', 35000,
    1, 3, 2
);