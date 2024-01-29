#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import logging
import asyncio
from datetime import datetime
from oncall_agent import OnCallAgent
from fastapi.encoders import jsonable_encoder
import json
from aider_helper import run_aider

# ----------------------------------------------------------------------------
# FastAPI as main entrypoint of the app for consumption
# ----------------------------------------------------------------------------

app = FastAPI()

# Set up CORS middleware options
app.add_middleware(
    CORSMiddleware,
    # Allows all origins from localhost:3001
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

oncall_gent = OnCallAgent()
handled_incidents = []


# ----------------------------------------------------------------------------
# some initial endpoints
# ----------------------------------------------------------------------------


# root
@app.get("/")
async def root():
    return "On-call agent is running"


# incident endpoint
@app.post("/incident")
async def process_incident(request: Request, incident_data: dict):
    # Process the incident data here
    # You can perform any necessary operations with the provided data

    # Get request information
    ip_address = request.client.host
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract incident data
    error_message = incident_data.get("error_message")
    stack_trace = incident_data.get("stack_trace")
    additional_info = incident_data.get("additional_info")

    # Check if incident has already been handled
    if (error_message, stack_trace) in handled_incidents:
        return {"message": "Incident already handled"}

    # Print request information
    logging.error(f"Received incident from:")
    logging.error(f"IP Address: {ip_address}")
    logging.error(f"Time: {current_time}")

    logging.error(f"Error Message: {error_message}")
    logging.error(f"Stack Trace: {stack_trace}")
    logging.error(f"Additional Info: {additional_info}")

    # Mark incident as handled
    handled_incidents.append((error_message, stack_trace))

    asyncio.create_task(handle_incident(
        error_message, stack_trace, additional_info))
    # Return a response if needed
    return {"message": "Incident handled successfully"}


async def handle_incident(error_message, stack_trace, additional_info):
    logging.warn(f"Oncall agent is invoked!")
    response = oncall_gent.research_incident(
        error_message, stack_trace, additional_info)
    root_cause = response.content[0].text.value
    root_cause = root_cause.strip('`').strip('json').strip()
    # Assuming `root_cause` is a JSON string
    try:
        root_cause_json = json.loads(root_cause)
        # Do something with root_cause_json
    except json.JSONDecodeError as e:
        print("Failed to parse JSON. Error:", e)
        print("Raw string:", root_cause)
        return
    except Exception as e:
        print("An unexpected error occurred:", e)
        return
    # Access the values of the fields
    file = root_cause_json['file']
    area = root_cause_json['area']
    instruction = root_cause_json['instruction']
    report = root_cause_json['report_name']

    # Do something with the values
    print("Found solution based on this incident report:")
    print(report)

    # Read the report content and print it out
    with open('../incident_reports/' + report, 'r') as f:
        report_content = f.read()
        print("Report Content:")
        print(report_content)

    print("Now trying to fix the problem!")
    file_path = '/home/roywei/workspace/next13-ecommerce-store/'+file
    print("file path: ", file_path)
    print("instruction: ", instruction)
    print("area in file: ", area)
    run_aider(file_path, instruction, area_to_focus=area)
