import sqlite3
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from constants import DB
import repository.Repository as Repo


def plot_reservations_per_role():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT role, COUNT(*) FROM {DB.reservations} GROUP BY role')
    data = c.fetchall()
    conn.close()
    
    roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    bars = ax.bar(range(len(roles)), total_reservations)
    ax.set_title('Total Reservations by Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Total Reservations')


    ax.set_xticks(range(len(roles)))
    ax.set_xticklabels(roles)
    plt.xticks(rotation=45, ha="right")
    ax.set_xlim(-0.5, len(roles) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_reservations_per_purpose():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT public_or_private, COUNT(*) FROM {DB.reservations} GROUP BY public_or_private')
    data = c.fetchall()
    conn.close()
    
    reservation_purposes = [row[0] for row in data]
    total_reservations = [row[1] for row in data]
     
    fig, ax = plt.subplots(figsize=(15,15))
    bars = ax.bar(range(len(reservation_purposes)), total_reservations)
    ax.set_title('Total Reservations by Reservation Purpose')
    ax.set_xlabel('Reservation Purpose')
    ax.set_ylabel('Total Reservations')

    ticks = np.linspace(0, len(reservation_purposes)-1, len(reservation_purposes))
    ax.set_xticks(ticks)
    ax.set_xticklabels(reservation_purposes)
    plt.xticks(rotation=45, ha="right")
    ax.set_xlim(-0.5, len(reservation_purposes) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_reservations_per_class():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT classroom, COUNT(*) FROM {DB.reservations} GROUP BY classroom')
    data = c.fetchall()
    conn.close()
    
    classroom_names = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    bars = ax.bar(range(len(classroom_names)), total_reservations)
    ax.set_title('Total Reservations by Classroom Name')
    ax.set_xlabel('Classroom Name')
    ax.set_ylabel('Total Reservations')

    ax.set_xticks(range(len(classroom_names)))
    ax.set_xticklabels(classroom_names)
    plt.xticks(rotation=45, ha="right")
    ax.set_xlim(-0.5, len(classroom_names) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_reservations_per_priority_value():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT priority_reserved, COUNT(*) FROM {DB.reservations} GROUP BY priority_reserved')
    data = c.fetchall()
    conn.close()

    priority_values, total_reservations = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15, 15))
    bars = ax.bar(range(len(priority_values)), total_reservations)
    ax.set_title('Total Reservations by Priority Value')
    ax.set_xlabel('Priority Value')
    ax.set_ylabel('Total Reservations')

    ax.set_xticks(range(len(priority_values)))
    ax.set_xticklabels(priority_values, rotation=45, ha='right')

    # Adjust x-tick positions dynamically
    ax.set_xlim(-0.5, len(priority_values) - 0.5)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html


def plot_user_numbers_per_priority_value():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT priority, COUNT(*) FROM users_db GROUP BY priority')
    data = c.fetchall()
    conn.close()

    priority_values, total_number_of_users = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15, 15))
    bars = ax.bar(range(len(priority_values)), total_number_of_users)
    ax.set_title('Total Number of Users for Each Priority Value')
    ax.set_xlabel('Priority Value')
    ax.set_ylabel('Total Number of Users')

    ax.set_xticks(range(len(priority_values)))
    ax.set_xticklabels(priority_values, rotation=45, ha='right')

    # Adjust x-tick positions dynamically
    ax.set_xlim(-0.5, len(priority_values) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_user_numbers_per_role():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT role, COUNT(*) FROM users_db GROUP BY role')
    data = c.fetchall()
    conn.close()

    user_roles, total_number_of_users = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    bars = ax.bar(range(len(user_roles)), total_number_of_users)
    ax.set_title('Total Number of Users for Each User Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Number of Users')

    ax.set_xticks(range(len(user_roles)))
    ax.set_xticklabels(user_roles)
    plt.xticks(rotation=45, ha="right")
    ax.set_xlim(-0.5, len(user_roles) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

#########################DATA VISUALIZATIONS FOR IT REPORTS#################################################

def plot_histogram_of_it_report_numbers_per_problem_description():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT problem_description, COUNT(*) FROM IT_Report_logdb GROUP BY problem_description')
    data = c.fetchall()
    conn.close()

    problem_descriptions, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    bars = ax.bar(range(len(problem_descriptions)), total_number_of_it_reports)
    ax.set_title('Number of IT Reports per Problem Description')
    ax.set_xlabel('Problem Descriptions')
    ax.set_ylabel('Number of IT Reports')

    ax.set_xticks(range(len(problem_descriptions)))
    ax.set_xticklabels(problem_descriptions)
    ax.grid(axis='y', linestyle='--')
    plt.xticks(rotation=45, ha="right")
    ax.set_xlim(-0.5, len(problem_descriptions) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_histogram_of_it_report_numbers_per_classroom_name():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT room_name, COUNT(*) FROM IT_Report_logdb GROUP BY room_name')
    data = c.fetchall()
    conn.close()

    room_names, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15, 15))
    bars = ax.bar(range(len(room_names)), total_number_of_it_reports)
    ax.set_title('Number of IT Reports for Each Classroom')
    ax.set_xlabel('Classroom Names')
    ax.set_ylabel('Number of IT Reports')

    ax.set_xticks(range(len(room_names)))
    ax.set_xticklabels(room_names)
    ax.grid(axis='y', linestyle='--')
    plt.xticks(rotation=45, ha="right")

    ax.set_xlim(-0.5, len(room_names) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_histogram_of_it_report_numbers_per_faculty_name():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT faculty_name, COUNT(*) FROM IT_Report_logdb GROUP BY faculty_name')
    data = c.fetchall()
    conn.close()

    faculty_names, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15, 15))
    bars = ax.bar(range(len(faculty_names)), total_number_of_it_reports)
    ax.set_title('Number of IT Reports for Each Faculty')
    ax.set_xlabel('Faculty')
    ax.set_ylabel('Number of IT Reports')

    ax.set_xticks(range(len(faculty_names)))
    ax.set_xticklabels(faculty_names, rotation=45, ha='right', fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(axis='y', linestyle='--')

    ax.set_xlim(-0.5, len(faculty_names) - 0.5)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(height, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html
#########################DATA VISUALIZATIONS FOR IT REPORTS#####################################################