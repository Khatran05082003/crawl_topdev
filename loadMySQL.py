import pandas as pd
import mysql.connector
from mysql.connector import Error

jobs_df = pd.read_csv('jobs.csv')
company_df = pd.read_csv('company.csv')

connection = None
try:
    connection = mysql.connector.connect(
        host='localhost',  # Thay bằng host của bạn
        database='topdev',  # Thay bằng tên cơ sở dữ liệu của bạn
        user='root',  # Thay bằng username của bạn
        password='pasword'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INT AUTO_INCREMENT PRIMARY KEY,
                job_name VARCHAR(255),
                company_name VARCHAR(255),
                salary VARCHAR(255),
                salary_negotiable BOOLEAN,
                job_description TEXT,
                level VARCHAR(255),
                job_requirements TEXT,
                benefits TEXT,
                interview_process TEXT,
                technologies_used TEXT,
                application_method TEXT
            )
        """)

       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company (
                company_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255),
                logo_url TEXT,
                company_description TEXT,
                company_size VARCHAR(255),
                country VARCHAR(255),
                website VARCHAR(255),
                tagline VARCHAR(255),
                industry VARCHAR(255),
                company_address TEXT
            )
        """)

       
        for i, row in company_df.iterrows():
            cursor.execute("""
                INSERT INTO company (
                    company_name, logo_url, company_description, company_size,
                    country, website, tagline, industry, company_address
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    logo_url = VALUES(logo_url),
                    company_description = VALUES(company_description),
                    company_size = VALUES(company_size),
                    country = VALUES(country),
                    website = VALUES(website),
                    tagline = VALUES(tagline),
                    industry = VALUES(industry),
                    company_address = VALUES(company_address)
            """, (
                row['Công ty'], row['Hình ảnh logo'], row['Giới thiệu công ty'], row['Quy mô công ty'],
                row['Quốc Gia'], row['Website công ty'], row['Tagline'], row['Lĩnh vực công ty'], row['Địa chỉ công ty']
            ))

       
        for i, row in jobs_df.iterrows():
            cursor.execute("""
                INSERT INTO jobs (
                    job_name, company_name, salary, salary_negotiable, job_description,
                    level, job_requirements, benefits, interview_process, technologies_used,
                    application_method
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    company_name = VALUES(company_name),
                    salary = VALUES(salary),
                    salary_negotiable = VALUES(salary_negotiable),
                    job_description = VALUES(job_description),
                    level = VALUES(level),
                    job_requirements = VALUES(job_requirements),
                    benefits = VALUES(benefits),
                    interview_process = VALUES(interview_process),
                    technologies_used = VALUES(technologies_used),
                    application_method = VALUES(application_method)
            """, (
                row['Tên job'], row['Tên Công ty'], row['Mức lương'], row['Thương lượng lương'], row['Mô tả công việc'],
                row['Cấp bậc'], row['Yêu cầu công việc'], row['Quyền lợi'], row['Quy trình phỏng vấn'],
                row['Công nghệ sử dụng'], row['Cách thức ứng tuyển']
            ))

        
        connection.commit()

except Error as e:
    print(f"Error: {e}")
finally:
    try:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    except NameError:
        pass 
