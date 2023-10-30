import get_umich_jobs as um

def main():
    print("\nSearching IT jobs...")
    job_ids = um.get_job_ids(career_interest=210)

    print("Searching 'analyst' jobs...")
    job_ids.extend(um.get_job_ids(title="analyst"))

    print("Searching 'data' jobs...")
    job_ids.extend(um.get_job_ids(title="data"))

    print("Searching 'python' jobs...")
    job_ids.extend(um.get_job_ids(keyword="python"))

    print("Searching 'SQL' jobs...")
    job_ids.extend(um.get_job_ids(keyword="sql"))

    job_ids = list(set(job_ids))
    print(f'{len(job_ids)} jobs found')

    jobs = um.get_jobs_from_ids(job_ids)
    um.create_jobs_csvs(jobs)

if __name__ == "__main__":
    main()