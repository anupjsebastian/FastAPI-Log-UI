import os
from datetime import datetime, timedelta
import streamlit as st
import sqlite3
import pandas as pd

# Function to get a list of task names and ids from the /nas_dir directory
def get_tasks():
    nas_dir = "/nas_dir"
    task_names = os.listdir(nas_dir)
    tasks = {}
    for task_name in task_names:
        
        if task_name.endswith('.db'):
            task_names.remove(task_name)
            continue
        
        task_ids = os.listdir(os.path.join(nas_dir, task_name))
        tasks[task_name] = task_ids
    return tasks


# Function to retrieve logs from a specified task_id and database file
def get_logs(task_name, task_id):
    db_path = os.path.join("/nas_dir", task_name, task_id, f"{task_id}.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    logs = c.execute("SELECT * FROM logs").fetchall()
    conn.close()
    return logs


# Function to retrieve logs from the service.db file in /nas_dir
def get_service_logs():
    db_path = os.path.join("/nas_dir", "service.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    logs = c.execute("SELECT * FROM logs").fetchall()
    conn.close()
    return logs


# Function to filter logs by timestamp, level, task_id, and task_name
def filter_logs(logs, start_time, end_time, level, task_name, task_id):
    filtered_logs = []
    for log in logs:
        log_time = datetime.strptime(log[0], '%Y-%m-%d %H:%M:%S.%f').date()
        if (not start_time or log_time >= start_time) and (not end_time or log_time <= end_time) and \
                (not level or log[1] == level) and (not task_name or log[2] == task_name) and \
                (not task_id or log[3] == task_id):
            filtered_logs.append(log)
    return filtered_logs


# Get list of task names and ids
tasks = get_tasks()

# Page layout
st.set_page_config(page_title="Log Viewer", page_icon=":memo:", layout="wide")

# Sidebar
st.sidebar.header("Select Task")
task_name = st.sidebar.selectbox("Task Name", list(tasks.keys()), key="task_name")
task_id = st.sidebar.selectbox("Task ID", tasks[task_name], key="task_id")
view_service_logs = st.sidebar.button("View Service Logs")

# Main page
st.title("Log Viewer")
if view_service_logs:
    logs = get_service_logs()
else:
    logs = get_logs(task_name, task_id)

# Filter logs
st.header("Filter Logs")
start_time = st.date_input("Start Time", key="start_time")
end_time = st.date_input("End Time", key="end_time")
end_time += timedelta(days=1)
level = st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", ""], key="level")
headings = ["Timestamp", "Level", "Task Name", "Task ID", "Message"]
filtered_logs = pd.DataFrame(filter_logs(logs, start_time, end_time, level, task_name, task_id), columns=headings)

# Display logs
st.header("Logs")


st.table(filtered_logs)
