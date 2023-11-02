import requests
from bs4 import BeautifulSoup
import pandas as pd


class UMichJob:
    def __init__(self, job_id):
        self.job_id = job_id
        self.url = f"https://careers.umich.edu/job_detail/{job_id}/"
        self.title = ""
        self.location = ""
        self.reg_temp = ""
        self.dept = ""
        self.start_dt = ""
        self.end_dt = ""
        self.salary_low = ""
        self.salary_high = ""
        self.career_interests = []

    def __str__(self):
        return f"{self.title} ({self.job_id})" if self.title != "" else self.url

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)


def reached_end(soup):
    end_text = "There are currently no posted jobs fitting the criteria you selected"
    p_tags = soup.find_all("p")
    for p in p_tags:
        if p != None and end_text in p.text:
            return True
    return False


def get_job_ids(
    career_interest="All",
    page_limit=50,
    job_limit=None,
    title="",
    keyword="",
):
    job_ids = []

    for pageNum in range(0, page_limit):
        print(f"Scanning page {pageNum+1}...")

        url = f"https://careers.umich.edu/search-jobs?career_interest={career_interest}&page={pageNum}&title={title}&keyword={keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if reached_end(soup):
            print(f"Reached the end on page number {pageNum+1}\n")
            break

        a_tags = soup.find_all("a")
        for a in a_tags:
            href = a.get("href")
            if href != None and "job_detail" in href:
                job_id = href.split("/")[2]
                job_ids.append(job_id)

        if job_limit != None and len(job_ids) >= job_limit:
            break

    return job_ids


def get_job_info(job_id):
    job = UMichJob(job_id)
    response = requests.get(job.url)
    soup = BeautifulSoup(response.text, "html.parser")

    div_tags = soup.find_all("div")

    for div in div_tags:
        h3 = div.find("h3")
        if h3 == None:
            continue

        p = div.find("p")
        if p == None:
            continue

        h3_text = h3.text.lower()
        p_text = p.text.strip()

        if "working title" in h3_text:
            job.title = p_text
        elif "work location" in h3_text:
            job.location = p_text
        elif "regular/temporary" in h3_text:
            job.reg_temp = p_text
        elif "department" in h3_text:
            job.dept = p_text
        elif "date" in h3_text:
            date_range = p_text.split("-")
            if len(date_range) > 0:
                job.start_dt = date_range[0].strip()
            if len(date_range) > 1:
                job.end_dt = date_range[1].strip()
        elif "salary" in h3_text:
            salary_range = p_text.split("-")
            if len(salary_range) > 0:
                job.salary_low = money_str_to_float(salary_range[0])
            if len(salary_range) > 1:
                job.salary_high = money_str_to_float(salary_range[1])
        elif "interest" in h3_text:
            interests = div.find_all("p")
            for i in interests:
                job.career_interests.append(i.text)
        else:
            pass
    return job


def money_str_to_float(money_str):
    return float(money_str.replace("$", "").replace(",", "").strip())


def get_jobs_from_ids(job_ids):
    jobs = []
    count = 0
    max_attempts = 5

    for job_id in job_ids:
        count += 1
        attempts = 1
        while attempts <= max_attempts:
            try:
                job = get_job_info(job_id)
                print(f"({count}) {job}")
                jobs.append(job)
                break
            except:
                print(f"Failed attempt {attempts} to scrape job {job_id}")
                attempts += 1
                if attempts > max_attempts:
                    print("Failed all attempts, moving on...")
    return jobs


def create_jobs_csvs(jobs):
    job_dicts = []
    interest_dicts = []

    for job in jobs:
        job_dicts.append(vars(job))
        for interest in job.career_interests:
            interest_dicts.append({"job_id": job.job_id, "career_interest": interest})

    df_jobs = pd.DataFrame(job_dicts)
    df_jobs = df_jobs.drop(
        columns="career_interests"
    )  # use the interests table instead
    df_jobs["start_dt"] = df_jobs["start_dt"].astype("datetime64[ns]")
    df_jobs["end_dt"] = df_jobs["end_dt"].astype("datetime64[ns]")
    df_jobs = df_jobs.sort_values(by="end_dt", ascending=True)

    df_interests = pd.DataFrame(interest_dicts)

    df_jobs.to_csv("data/umich_jobs.csv", index=False)
    df_interests.to_csv("data/umich_job_interests.csv", index=False)
