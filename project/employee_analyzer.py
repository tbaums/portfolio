from database import CursorFromConnectionFromPool
import pandas as pd
import numpy as np 

class EmployeeAnalyzer:

    def __load_from_db(self, department):
        with CursorFromConnectionFromPool() as cursor:
            query = "select *, right(annual_salary, length(annual_salary)-1)::float as salary from chicago_employees where department='{}' and annual_salary != 'nan'".format(department.upper())
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=['id', 
                                                          'employee_name', 
                                                          'job_title', 
                                                          'department', 
                                                          'ft_or_pt', 
                                                          'salary_or_hourly', 
                                                          'typical_hours',
                                                          'to_delete',
                                                          'hourly_rate',
                                                          'salary'])
            df = df.drop(columns=['to_delete'])
        return df 

    def get_police_salaries_by_title(self):
        df = self.__load_from_db('POLICE')
        # a = df[df['job_title']=='SERGEANT']
        jobs = list(df['job_title'].drop_duplicates())

        js_data_container = []
        for job in jobs:
            trace = {
                'x': list(df['salary'][df['job_title'] == job]),
                'type': 'box',
                'name': job
            }
            # print(trace)
            if sum(trace['x'])/len(trace['x']) > 150000 or len(trace['x']) > 50:
                js_data_container.append(trace)

        # df = df.groupby(['job_title'])['salary'].mean()
        return js_data_container


# ea = EmployeeAnalyzer()
# ea.get_police_salaries_by_title()