import umich_job_scraper as um


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
    print(f"{len(job_ids)} jobs found")

    jobs = um.get_jobs_from_ids(job_ids)
    jobs_a2 = []
    print("\nFiltering out jobs not located in Ann Arbor...")
    for job in jobs:
        # Both U-M and Michigan Medicine:
        if job.location.find("Ann Arbor") != -1:
            jobs_a2.append(job)
    um.create_jobs_csvs(jobs_a2)
    print("\nDone!")


if __name__ == "__main__":
    main()
