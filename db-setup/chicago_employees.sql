
--Retrieve csv source here: https://catalog.data.gov/dataset/current-employee-names-salaries-and-position-titles-840f7

drop table if exists "public"."chicago_employees";

/* 
Create table
*/
create table "public"."chicago_employees" (
    id serial primary key,
    employee_name  text,
    job_title text,
    department text,
    ft_or_pt text,
    salary_or_hourly text,
    typical_hours text,
    annual_salary text,
    hourly_rate text
    );

