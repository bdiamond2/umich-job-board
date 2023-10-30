import umich_job_scraper as um

def main():
    print("Searching all UMich jobs")
    job_ids = um.get_job_ids()
    jobs = um.get_jobs_from_ids(job_ids)
    um.create_jobs_csvs(jobs)


if __name__ == "__main__":
    main()