import get_umich_jobs as um

def main():
    job_ids = um.get_job_ids()
    jobs = um.get_jobs_from_ids(job_ids)
    um.create_jobs_csvs(jobs)


if __name__ == "__main__":
    main()