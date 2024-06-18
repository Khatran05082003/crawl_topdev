import random
import time
import pymongo
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['topdev']
mycol = mydb['jobs']


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

def fetch_job_urls():
    id_jobs = []
    for page in range(1, 77):
        url_template = 'https://api.topdev.vn/td/v2/jobs?fields[job]=id,slug,title,salary,company,extra_skills,skills_str,skills_arr,skills_ids,job_types_str,job_levels_str,job_levels_arr,job_levels_ids,addresses,status_display,detail_url,job_url,salary,published,refreshed,applied,candidate,requirements_arr,packages,benefits,content,features,is_free,is_basic,is_basic_plus,is_distinction&fields[company]=slug,tagline,addresses,skills_arr,industries_arr,industries_str,image_cover,image_galleries,benefits&page={}&locale=vi_VN&ordering=jobs_new'
        url = url_template.format(page)
        try:
            result = requests.get(url, headers=headers, timeout=10).text
            data = json.loads(result).get('data')
            if data is None or data == []:
                break
            for item in data:
                if item.get('id') not in id_jobs:
                    id_jobs.append(item.get('id'))
                    mycol.insert_one(item)
            #time.sleep(random.uniform(1, 2))
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"Đã xảy ra lỗi khi lấy dữ liệu từ trang {page}: {e}")
            continue
    return id_jobs

def fetch_details(id_jobs):
    link = 'https://topdev.vn/detail-jobs/'
    titles, companies, job_description, skills_qualifications, benefits = [], [], [], [], []
    interview, industry, company_size, nation, link_company, company_description = [], [], [], [], [], []

    for job_id in id_jobs:
        url = link + str(job_id)
        try:
            html = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(html.text, "html.parser")

            titles.append(soup.find('h1', class_='text-2xl font-bold text-black').get_text(strip=True) if soup.find('h1', class_='text-2xl font-bold text-black') else 'non-existent')
            companies.append(soup.find('p', class_='my-1 line-clamp-1 text-base font-bold text-gray-500').get_text(strip=True) if soup.find('p', class_='my-1 line-clamp-1 text-base font-bold text-gray-500') else 'non-existent')

            prose_sections = soup.find_all('div', class_='prose max-w-full text-sm text-black lg:text-base')
            job_description.append(prose_sections[0].get_text(separator=' ', strip=True) if len(prose_sections) > 0 else 'non-existent')
            skills_qualifications.append(prose_sections[1].get_text(separator=' ', strip=True) if len(prose_sections) > 1 else 'non-existent')
            benefits.append(prose_sections[2].get_text(separator=' ', strip=True) if len(prose_sections) > 2 else 'non-existent')

            interview.append(soup.find('ul', class_='list-disc pl-5 text-base').get_text(separator=' ', strip=True) if soup.find('ul', class_='list-disc pl-5 text-base') else 'non-existent')

            industry_info = soup.find_all('p', class_='line-clamp-2 text-xs text-gray-600 md:text-base')
            industry.append(industry_info[0].get_text(strip=True) if len(industry_info) > 0 else 'non-existent')
            company_size.append(industry_info[1].get_text(strip=True) if len(industry_info) > 1 else 'non-existent')
            nation.append(industry_info[2].get_text(strip=True) if len(industry_info) > 2 else 'non-existent')

            try:
                company_link = 'https://topdev.vn' + soup.find('a', class_='flex min-h-[112px] items-center justify-center')['href']
                soup_company = BeautifulSoup(requests.get(company_link, headers=headers, timeout=10).text, "html.parser")
                link_company.append(soup_company.find('a', class_='mt-2 inline-block break-all text-blue-dark hover:underline')['href'])
                #company_id.append(re.search(r'-(\d+)\?src=topdev_detailjob&medium=logo_company', company_link).group(1))
                company_description.append(soup_company.find('div', class_='prose max-w-full leading-snug text-gray-500').get_text(separator=' ', strip=True))
            except (AttributeError, TypeError, requests.exceptions.RequestException):
                link_company.append('non-existent')
                company_description.append('non-existent')
                #company_id.append('non-existent')
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"Đã xảy ra lỗi khi lấy dữ liệu chi tiết cho công việc ID {job_id}: {e}")
            continue

    data = {
        "id_jobs": id_jobs,
        "titles": titles,
        "companies": companies,
        "job_description": job_description,
        "skills_qualifications": skills_qualifications,
        "benefits": benefits,
        "interview": interview,
        "industry": industry,
        "company_size": company_size,
        "nation": nation,
        "link_company": link_company,
        "company_description": company_description
    }
    return pd.DataFrame(data)

def fetch_db_documents(projection):
    documents = mycol.find({}, projection)
    return pd.json_normalize(list(documents))

if __name__ == "__main__":
    id_jobs = fetch_job_urls()
    details_df = fetch_details(id_jobs)

    projection_job = {
        'id': 1,
        'title': 1,
        'company.display_name': 1,
        'salary.is_negotiable': 1,
        'salary.value': 1,
        'job_levels_str': 1,
        'skills_arr': 1,
        'job_types_str': 1,
        '_id': 0
    }

    projection_company = {
        'id': 1,
        'company.id': 1,
        'company.display_name': 1,
        'company.image_logo': 1,
        'company.addresses.sort_addresses': 1,
        'company.tagline': 1,
        'company.industries_str': 1,
        '_id': 0
    }

    jobs_df = fetch_db_documents(projection_job)
    company_df = fetch_db_documents(projection_company)

    jobs_df = pd.merge(jobs_df, details_df, left_on='id', right_on='id_jobs', how='left')
    company_df = pd.merge(company_df, details_df, left_on='id', right_on='id_jobs', how='left')

    jobs_df = jobs_df[[
        'title',
        'company.display_name',
        'salary.value',
        'salary.is_negotiable',
        'job_description',
        'job_levels_str',
        'skills_qualifications',
        'benefits',
        'interview',
        'skills_arr'
    ]]

    jobs_df.columns = [
        'Tên job',
        'Tên Công ty',
        'Mức lương',
        'Thương lượng lương',
        'Mô tả công việc',
        'Cấp bậc',
        'Yêu cầu công việc',
        'Quyền lợi',
        'Quy trình phỏng vấn',
        'Công nghệ sử dụng'
    ]

    jobs_df['Cách thức ứng tuyển'] = jobs_df.apply(lambda x: f'apply in https://topdev.vn/detail-jobs/{x.name}', axis=1)

    company_df = company_df[[
        'company.display_name',
        'company.image_logo',
        'company_description',
        'company_size',
        'nation',
        'link_company',
        'company.tagline',
        'company.industries_str',
        'company.addresses.sort_addresses'
    ]]

    company_df.columns = [
        'Công ty',
        'Hình ảnh logo',
        'Giới thiệu công ty',
        'Quy mô công ty',
        'Quốc Gia',
        'Website công ty',
        'Tagline',
        'Lĩnh vực công ty',
        'Địa chỉ công ty'
    ]
    
    company_df = company_df.drop_duplicates()
    company_df = company_df.reset_index(drop=True)