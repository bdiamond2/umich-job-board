import umich_job_scraper as um

c1 = um.JobSearchCriteria(career_interest=210)
c2 = um.JobSearchCriteria(title="analyst")
c3 = um.JobSearchCriteria(title="data")
c4 = um.JobSearchCriteria(keyword="python")
c5 = um.JobSearchCriteria(keyword="sql")

um.output_jobs('jobs.csv', c1, c2, c3, c4, c5)