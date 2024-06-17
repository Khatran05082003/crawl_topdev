# Requirement

In this particular project, we will be utilizing the versatile programming language, Python, as our primary tool for the purpose of collecting and collating job postings and information from the professional networking platform.


### Crawling all the job from https://topdev.vn/

1. Fetch **all** job and company information currently displayed on various categories of the website [TopDev](https://topdev.vn/).
   
   **Data will be stored in MongoDB.**

2. Create a backup of the data to send to the Coach for potential restoration on another MongoDB system.

3. Extract the following fields and store them in MySQL for use by other teams

# How to use my project
B1:
git clone  https://github.com/Khatran05082003/crawl_topdev.git

B2:
python crawlTopDev.py

B3:
python loadMySQL.py

## Database Structure

### Jobs Table

- **job_id** (INT, AUTO_INCREMENT): Unique identifier for each job posting.
- **job_name** (VARCHAR(255)): Title or name of the job.
- **company_name** (VARCHAR(255)): Name of the company hiring for the job.
- **salary** (VARCHAR(255)): Salary offered for the job.
- **salary_negotiable** (BOOLEAN): Indicates if the salary is negotiable (True/False).
- **job_description** (TEXT): Description of the job responsibilities.
- **level** (VARCHAR(255)): Job level or position level.
- **job_requirements** (TEXT): Requirements or qualifications needed for the job.
- **benefits** (TEXT): Benefits offered with the job.
- **interview_process** (TEXT): Process or steps involved in the interview.
- **technologies_used** (TEXT): Technologies or tools used in the job role.
- **application_method** (TEXT): Method or link to apply for the job.
  
### Demo
![image](https://github.com/Khatran05082003/crawl_topdev/assets/102920168/6e0c9113-2bf0-4ec5-93ff-9bbe88a6bf91)


### Company Table

- **company_id** (INT, AUTO_INCREMENT): Unique identifier for each company.
- **company_name** (VARCHAR(255)): Name of the company.
- **logo_url** (TEXT): URL to the company's logo image.
- **company_description** (TEXT): Description or overview of the company.
- **company_size** (VARCHAR(255)): Size or scale of the company.
- **country** (VARCHAR(255)): Country where the company is located.
- **website** (VARCHAR(255)): Official website of the company.
- **tagline** (VARCHAR(255)): Tagline or slogan of the company.
- **industry** (VARCHAR(255)): Industry or sector to which the company belongs.
- **company_address** (TEXT): Address or location of the company.
  
### DEMO
![image](https://github.com/Khatran05082003/crawl_topdev/assets/102920168/6a08a96e-a599-4c90-9623-821b4f6f7b90)


