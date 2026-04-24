/*คำสั่งเอาตรวจสอบข้อมูลตาราง*/
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.birth_date,
    e.start_date,
    e.salary,
    d.department_name,
    p.position_name,
    e.supervisor_id
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN positions p ON e.position_id = p.position_id;
  

/*คำสั่งเอาตรวจข้อที่ 2 */
/*SELECT employee_id, first_name, last_name
FROM employees
WHERE supervisor_id IS NULL
  AND position_id <> (
      SELECT position_id
      FROM positions
      WHERE position_name = 'เจ้าของบริษัท'
  );

SELECT COUNT(*) AS owner_without_supervisor
FROM employees e
JOIN positions p ON e.position_id = p.position_id
WHERE p.position_name = 'เจ้าของบริษัท'
  AND e.supervisor_id IS NULL;*/


/*เอาไว้ดูภาพรวมว่า ใครเป็นเจ้า ใครมี/ไม่มี supervisor*/
/*SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    p.position_name,
    e.supervisor_id
FROM employees e
JOIN positions p ON e.position_id = p.position_id
ORDER BY e.employee_id;*/

/*ใช้ตรวจข้อที่ 3 เงื่อนไขที่ 1*/
/*SELECT employee_id, COUNT(DISTINCT department_id)
FROM employees
GROUP BY employee_id
HAVING COUNT(DISTINCT department_id) > 1;*/  /*ผลลัพธ์ควรเป็นค่าว่าง*/

/*ใช้ตรวจข้อที่ 3 เงื่อนไขที่ 2*/
/*SELECT employee_id, COUNT(DISTINCT supervisor_id)
FROM employees
GROUP BY employee_id
HAVING COUNT(DISTINCT supervisor_id) > 1;  /*ผลลัพธ์ควรเป็นค่าว่าง*/

/*ใช้ตรวจข้อที่ 3 เงื่อนไขที่ 3*/
/*SELECT supervisor_id, COUNT(employee_id) AS total_subordinates
FROM employees
WHERE supervisor_id IS NOT NULL
GROUP BY supervisor_id
HAVING COUNT(employee_id) >= 1; */  /*ผลลัพธ์ควรแสดง supervisor_id ที่มีลูกน้องอย่างน้อย 1 คน*/