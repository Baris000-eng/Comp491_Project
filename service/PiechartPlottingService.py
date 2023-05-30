import sqlite3
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from constants import DB
import repository.Repository as Repo

def piechart_reservations_per_priority_value():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT priority_reserved, COUNT(*) FROM {DB.reservations} GROUP BY priority_reserved')
    data = c.fetchall()
    conn.close()

    priority_values = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_reservations, labels=priority_values, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14})
    ax.axis('equal')
    ax.set_title('Total Reservations by Priority Value')
    plt.legend(title="Priority Value", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html


def piechart_of_reservations_per_class():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT classroom, COUNT(*) FROM {DB.reservations} GROUP BY classroom')
    data = c.fetchall()
    conn.close()
    
    classroom_names = [row[0] for row in data]
    total_reservations = [row[1] for row in data]
    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_reservations, labels=classroom_names, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Total Reservations by Classroom Name')
    plt.legend(title="Classroom Name", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html


def piechart_of_reservations_per_purpose():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT public_or_private, COUNT(*) FROM {DB.reservations} GROUP BY public_or_private')
    data = c.fetchall()
    conn.close()
    
    reservation_purposes = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_reservations, labels=reservation_purposes, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Total Reservations by Purpose')
    plt.legend(title="Reservation Purpose", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html


def piechart_of_reservations_per_role():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'SELECT role, COUNT(*) FROM {DB.reservations} GROUP BY role')
    data = c.fetchall()
    conn.close()
    
    roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_reservations, labels=roles, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Total Reservations by Role')
    plt.legend(title="User Roles", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_user_numbers_per_priority_value():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT priority, COUNT(*) FROM users_db GROUP BY priority')
    data = c.fetchall()
    conn.close()

    priority_values, total_number_of_users = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.pie(total_number_of_users, labels=priority_values, autopct='%1.1f%%', startangle=90)
    ax.set_title('Total Number of Users for Each Priority Value')
    plt.legend(title="User Priority Values", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_user_numbers_per_role():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT role, COUNT(*) FROM users_db GROUP BY role')
    data = c.fetchall()
    conn.close()

    user_roles, total_reservations = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_reservations, labels=user_roles, autopct='%1.1f%%', startangle=90)
    ax.set_title('Total Number of Users for Each User Role')
    plt.legend(title="User Roles", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_it_report_numbers_per_faculty_name():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT faculty_name, COUNT(*) FROM IT_Report_logdb GROUP BY faculty_name')
    data = c.fetchall()
    conn.close()

    faculty_names, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_number_of_it_reports, labels=faculty_names, autopct='%1.1f%%', startangle=90)
    ax.set_title('Number of It Reports per Faculty')
    plt.legend(title="Faculty Names", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_it_report_numbers_per_classroom_name():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT room_name, COUNT(*) FROM IT_Report_logdb GROUP BY room_name')
    data = c.fetchall()
    conn.close()

    room_names, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_number_of_it_reports, labels=room_names, autopct='%1.1f%%', startangle=90)
    ax.set_title('Number of It Reports per Classroom Name')
    plt.legend(title="Classroom Names", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_it_report_numbers_per_problem_description():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT problem_description, COUNT(*) FROM IT_Report_logdb GROUP BY problem_description')
    data = c.fetchall()
    conn.close()

    problem_descriptions, total_number_of_it_reports = map(list, zip(*data))

    fig, ax = plt.subplots(figsize=(15,15))
    ax.pie(total_number_of_it_reports, labels=problem_descriptions, autopct='%1.1f%%', startangle=90)
    ax.set_title('Number of It Reports per Problem Description')
    plt.legend(title="Problem Descriptions", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html