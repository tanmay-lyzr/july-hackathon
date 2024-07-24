from lyzr_automata.agents.agent_base import *
import requests
import psycopg2
from fastapi import FastAPI
from typing import List, Dict
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata.tools.prebuilt_tools import *
from lyzr_automata.tasks.task_base import *


####################################################
###DATABASE


# PostgreSQL configuration
pg_config = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'database': 'lyzr',
    'port':'5432'
}


def get_pg_connection():
    return psycopg2.connect(**pg_config)


# Employee class
class Employee:
    def __init__(self, name, email, age, gender, position, department):
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.position = position
        self.department = department

def onboarding():
    print("Employee Onboarding")
    name = input("Enter employee name: ")
    email = input("Enter personal email: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    position = input("Enter the position: ")
    department = input("Enter the department: ")
    
    employee = Employee(name, email, age, gender, position, department)

    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employee (name, email, age, gender, position, department)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, email, age, gender, position, department))
    conn.commit()
    conn.close()

    print("Employee details saved successfully.")

    welcome_send_email_task(name=name, position=position, emails=[email])
    department_lead_email = department_heads[department]
    department_head_send_email_task(candidate_name=name,candidate_position=position,emails=[department_lead_email])
    linkedin_post_task(name=name,position=position,image_url="https://i.pinimg.com/originals/cb/37/5e/cb375e56ea17907217a0b970e8eef870.png")
    # send the welcome email by calling the tool url to user
    # send the email to the department manager by again tool url
    # announce the new joinee on social media by tool url
  

##########################################
### code for sending email
# Define the URL
def email_sender(receiver_email, subject, body):
    url = 'http://54.84.189.207/send_email/'

    # Define the payload
    payload = {
        "receiver_emails": receiver_email,
        "subject": subject,
        "body": body
    }

    # Set the headers, if any are needed (you can remove this if no headers are needed)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Print the response (status code and content)
    print(f'Status Code: {response.status_code}')
    print(f'Response Content: {response.content}')


openai_api_key = ***********************************

open_ai_model = OpenAIModel(
    api_key=openai_api_key,
    parameters={
        "model": "gpt-4o",
        "temperature": 0.2,
        "max_tokens": 1500,
    })

welcome_email_sender_agent = Agent(
    role="Email drafter",
    prompt_persona="""
You are STACY, an AI HR Agent. Your task is to write profesional yet compelling welcome emails to the candidate.
Use ONLY the data given to you, AND NO other data. DO NOT INCLUDE ANY PLACEHOLDERS.

    """
)

department_notifier_email_agent = Agent(
    role = "Department Head Notifier",
    prompt_persona="""

You are STACY, an AI HR Agent. Your job is to write professional emails that will be a new employee joining notification email.
Use ONLY the data given to you, AND NO other data. DO NOT INCLUDE ANY PLACEHOLDERS."""
)

department_heads = {"Engineering":"atharva.patil@goml.io",
                    "HR":"rasswanth@lyzr.ai",
                    "Marketing": "gokulavarshini.m@goml.io",
                    "Delivery": "tanmay@lyzr.ai"}

linkedin_post_agent = Agent(
    role="Linkedin post writer",
    prompt_persona="""
You are STACY, an AI HR Agent. Your task is to write a compelling, professional and attractive linkedin post regarding joining of a new employee.
Use ONLY the data given to you, AND NO other data. DO NOT INCLUDE ANY PLACEHOLDERS
"""
)

def welcome_send_email_task(name, position, emails):
    email_sender_task = Task(
        model=open_ai_model,
        input_type=InputType.TEXT,
        output_type=OutputType.TEXT,
        instructions="""
    You are an intelligent email writer agent, Your task is to create porfessional, compelling welcome email with the given name and position of the candidate.
    ALWAYS add <endofsubject) after the subject.
    DO NOT keep any placeholder in the email.
    Career and lives are at stake.
    """,
        agent=welcome_email_sender_agent,
        default_input=f"Name: {name}, Position: {position}"
    ).execute()
    print("emailsender",email_sender_task)
    subject = email_sender_task.split("<endofsubject>")[0]
    body = email_sender_task.split("<endofsubject>")[1]
    
    email_sender(emails, subject=subject, body=body)

def department_head_send_email_task(candidate_name, candidate_position, emails):
    email_sender_task = Task(
        model=open_ai_model,
        input_type=InputType.TEXT,
        output_type=OutputType.TEXT,
        instructions="""
    You are an intelligent email writer agent, Your task is to create porfessional, compelling welcome email with the given name and position of the candidate.
    ALWAYS add <endofsubject) after the subject.
    DO NOT keep any placeholder in the email.
    Career and lives are at stake.
    """,
        agent=welcome_email_sender_agent,
        default_input=f"Name: {candidate_name}, Position: {candidate_position}"
    ).execute()

    print("Inside department",email_sender_task)
    subject = email_sender_task.split("<endofsubject>")[0]
    body = email_sender_task.split("<endofsubject>")[1]
     
    email_sender(emails, subject=subject, body=body)

def linkedin_post(title, image_url, text_content):
    url = 'http://54.84.189.207/post_linkedin/'

    # Define the payload
    payload = {
        "title": title,
        "image_url": image_url,
        "text_content": text_content
    }

    # Set the headers, if any are needed (you can remove this if no headers are needed)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Print the response (status code and content)
    print(f'Status Code: {response.status_code}')
    print(f'Response Content: {response.content}')


def linkedin_post_task(name, position, image_url):
    linkedin_post_sender_task = Task(
        model=open_ai_model,
        input_type=InputType.TEXT,
        output_type=OutputType.TEXT,
        instructions="""
    You are an intelligent LinkedIN post writer. Your task is to create porfessional, compelling and attractive new employee joining welcome post with the given name and position of the candidate.
    ALWAYS add <endoftitle> after the title.
    Career and lives are at stake.
    """,
        agent=welcome_email_sender_agent,
        default_input=f"Name: {name}, Position: {position}"
    ).execute()

    title = linkedin_post_sender_task.split("<endoftitle>")[0]
    body = linkedin_post_sender_task.split("<endoftitle>")[1]
    print("linkedin",linkedin_post_sender_task)
    linkedin_post(title=title, image_url=image_url, text_content=body)

def main():
    while True:
        print("\nChoose an option:")
        print("1. Onboarding")
        print("2. Employee Support")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            onboarding()
        elif choice == '2':
            print("Employee Support is not implemented yet.")
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
