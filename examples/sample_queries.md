# QueryForge-AI — Sample NL → SQL Examples

A collection of natural language → SQL examples that QueryForge-AI can generate.

---

## 📊 E-Commerce

**Q:** Show top 5 customers by total spending this month
```sql
SELECT c.customer_name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE MONTH(o.order_date) = MONTH(CURRENT_DATE)
  AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 5;
```

**Q:** How many orders were placed each day last week?
```sql
SELECT DATE(order_date) AS order_day, COUNT(*) AS order_count
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
GROUP BY DATE(order_date)
ORDER BY order_day;
```

---

## 👥 HR / Employees

**Q:** List Engineering employees with salary above 80000
```sql
SELECT e.emp_name, e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Engineering'
  AND e.salary > 80000;
```

**Q:** How many employees are in each department?
```sql
SELECT d.dept_name, COUNT(e.emp_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY employee_count DESC;
```

---

## 📦 Inventory / Products

**Q:** Find products with stock below 10 units
```sql
SELECT product_name, category, stock
FROM products
WHERE stock < 10
ORDER BY stock ASC;
```

**Q:** What is the total revenue per product category for Q3 2024?
```sql
SELECT p.category, SUM(p.price * s.quantity) AS total_revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_date BETWEEN '2024-07-01' AND '2024-09-30'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

---

## 🏫 Education

**Q:** How many students passed the exam in each subject?
```sql
SELECT subject, COUNT(*) AS passed_count
FROM exam_results
WHERE grade >= 50
GROUP BY subject;
```

**Q:** List students who have not submitted any assignment
```sql
SELECT s.student_name
FROM students s
LEFT JOIN assignments a ON s.student_id = a.student_id
WHERE a.assignment_id IS NULL;
```
