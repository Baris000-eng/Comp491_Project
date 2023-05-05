import sqlite3
import io
import base64
import matplotlib.pyplot as plt
import numpy as np


def piechart_reservations_per_priority_value():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT priority_reserved, COUNT(*) FROM reservations_db GROUP BY priority_reserved')
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
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT classroom, COUNT(*) FROM reservations_db GROUP BY classroom')
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
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT public_or_private, COUNT(*) FROM reservations_db GROUP BY public_or_private')
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
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT role, COUNT(*) FROM reservations_db GROUP BY role')
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


def plot_reservations_per_role():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT role, COUNT(*) FROM reservations_db GROUP BY role')
    data = c.fetchall()
    conn.close()
    
    roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(roles, total_reservations)
    ax.set_title('Total Reservations by Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Total Reservations')


    ax.set_xticks(range(len(roles)))
    ax.set_xticklabels(roles)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_reservations_per_purpose():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT public_or_private, COUNT(*) FROM reservations_db GROUP BY public_or_private')
    data = c.fetchall()
    conn.close()
    
    reservation_purposes = [row[0] for row in data]
    total_reservations = [row[1] for row in data]
     
    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(reservation_purposes, total_reservations)
    ax.set_title('Total Reservations by Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Total Reservations')

    ticks = np.linspace(0, len(reservation_purposes)-1, len(reservation_purposes))
    ax.set_xticks(ticks)
    ax.set_xticklabels(reservation_purposes)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_reservations_per_class():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT classroom, COUNT(*) FROM reservations_db GROUP BY classroom')
    data = c.fetchall()
    conn.close()
    
    classroom_names = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(classroom_names, total_reservations)
    ax.set_title('Total Reservations by Classroom Name')
    ax.set_xlabel('Classroom Name')
    ax.set_ylabel('Total Reservations')

    ticks = np.linspace(0, len(classroom_names)-1, len(classroom_names))
    ax.set_xticks(ticks)
    ax.set_xticklabels(classroom_names)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

import numpy as np

def plot_reservations_per_priority_value():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT priority_reserved, COUNT(*) FROM reservations_db GROUP BY priority_reserved')
    data = c.fetchall()
    conn.close()

    priority_values = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(priority_values, total_reservations)
    ax.set_title('Total Reservations by Priority Value')
    ax.set_xlabel('Priority Value')
    ax.set_ylabel('Total Reservations')

    ticks = np.linspace(min(priority_values), max(priority_values), len(priority_values))
    ax.set_xticks(ticks)
    ax.set_xticklabels(priority_values)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_user_numbers_per_priority_value():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT priority, COUNT(*) FROM users_db GROUP BY priority')
    data = c.fetchall()
    conn.close()

    priority_values = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(priority_values, total_reservations)
    ax.set_title('Total Number of Users for Each Priority Value')
    ax.set_xlabel('Priority Value')
    ax.set_ylabel('Total Number of Users')

    ticks = np.linspace(min(priority_values), max(priority_values), len(priority_values))
    ax.set_xticks(ticks)
    ax.set_xticklabels(priority_values)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_user_numbers_per_priority_value():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT priority, COUNT(*) FROM users_db GROUP BY priority')
    data = c.fetchall()
    conn.close()

    priority_values = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.pie(total_reservations, labels=priority_values, autopct='%1.1f%%', startangle=90)
    ax.set_title('Total Number of Users for Each Priority Value')
    plt.legend(title="User Priority Values", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html


def plot_user_numbers_per_role():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT role, COUNT(*) FROM users_db GROUP BY role')
    data = c.fetchall()
    conn.close()

    user_roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.bar(user_roles, total_reservations)
    ax.set_title('Total Number of Users for Each User Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Number of Users')

    ticks = np.linspace(0, len(user_roles)-1, len(user_roles))
    ax.set_xticks(ticks)
    ax.set_xticklabels(user_roles)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html

def plot_piechart_of_user_numbers_per_role():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT role, COUNT(*) FROM users_db GROUP BY role')
    data = c.fetchall()
    conn.close()

    user_roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

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


