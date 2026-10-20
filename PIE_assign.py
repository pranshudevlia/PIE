import numpy as np
import gradio as gr
import random

class Job:
    def __init__(self, job_id, processing_time, due_date):
        self.job_id = job_id
        self.processing_time = processing_time
        self.due_date = due_date

    def slack_time(self):
        return self.due_date - self.processing_time

    def criticality_ratio(self):
        return self.due_date / self.processing_time

    def __repr__(self):
        return f"Job-{self.job_id}(P={self.processing_time}, D={self.due_date}, Slack={self.slack_time():.2f}, Ratio={self.criticality_ratio():.2f})"

def generate_jobs(n, processing_range, due_date_factor):
    processing_times = np.random.randint(processing_range[0], processing_range[1] + 1, size=n)
    total_processing_time = np.sum(processing_times)

    due_dates = np.random.randint(
        int(total_processing_time * due_date_factor[0]),
        int(total_processing_time * due_date_factor[1]) + 1,
        size=n
    )

    jobs = [Job(i + 1, p, d) for i, (p, d) in enumerate(zip(processing_times, due_dates))]
    return np.array(jobs)

def fcfs(jobs):
    return jobs

def spt(jobs):
    return np.array(sorted(jobs, key=lambda job: job.processing_time))

def lpt(jobs):
    return np.array(sorted(jobs, key=lambda job: job.processing_time, reverse=True))

def smallest_slack(jobs):
    return np.array(sorted(jobs, key=lambda job: job.slack_time()))

def smallest_criticality_ratio(jobs):
    return np.array(sorted(jobs, key=lambda job: job.criticality_ratio()))

def random_order(jobs):
    shuffled_jobs = jobs.copy()
    np.random.shuffle(shuffled_jobs)
    return shuffled_jobs

def format_schedule(schedule):
    return "\n".join(str(job) for job in schedule)

def schedule_jobs(num_jobs, processing_case, due_date_case):
    processing_cases = [(2, 10), (2, 50), (2, 100)]
    due_date_cases = [(0.3, 0.9), (0.5, 1.1)]
 
    processing_range = processing_cases[processing_case - 1]
    due_date_factor = due_date_cases[due_date_case - 1]
    
    jobs = generate_jobs(num_jobs, processing_range, due_date_factor)
    
    schedules = {
        "Original": format_schedule(jobs),
        "FCFS": format_schedule(fcfs(jobs)),
        "SPT": format_schedule(spt(jobs)),
        "LPT": format_schedule(lpt(jobs)),
        "Smallest Slack Time": format_schedule(smallest_slack(jobs)),
        "Smallest Criticality Ratio": format_schedule(smallest_criticality_ratio(jobs)),
        "Random Order": format_schedule(random_order(jobs))
    }
    
    return schedules["Original"], schedules["FCFS"], schedules["SPT"], schedules["LPT"], schedules["Smallest Slack Time"], schedules["Smallest Criticality Ratio"], schedules["Random Order"]

# Updated interface with range descriptions
interface = gr.Interface(
    fn=schedule_jobs,
    inputs=[
        gr.Number(label="Number of Jobs", value=5, precision=0),
        gr.Radio(label="Processing Case", 
                 choices=["Case 1: Range (2, 10)", "Case 2: Range (2, 50)", "Case 3: Range (2, 100)"], 
                 type="index"),
        gr.Radio(label="Due Date Case", 
                 choices=["Case 1: Factor (0.3, 0.9)", "Case 2: Factor (0.5, 1.1)"], 
                 type="index")
    ],
    outputs=[
        gr.Textbox(label="Original Schedule"),
        gr.Textbox(label="FCFS Schedule"),
        gr.Textbox(label="SPT Schedule"),
        gr.Textbox(label="LPT Schedule"),
        gr.Textbox(label="Smallest Slack Time Schedule"),
        gr.Textbox(label="Smallest Criticality Ratio Schedule"),
        gr.Textbox(label="Random Order Schedule")
    ],
    title="Job Scheduling Simulation",
    description="Choose the number of jobs, processing case, and due date case to generate different job schedules."
)

interface.launch(inbrowser=True)
