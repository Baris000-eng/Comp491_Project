import sqlite3
import io
import base64
import matplotlib.pyplot as plt

def plot_reservations_per_role():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT role, COUNT(*) FROM reservations_db GROUP BY role')
    data = c.fetchall()
    conn.close()
    
    roles = [row[0] for row in data]
    total_reservations = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(13,13))
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
     
    fig, ax = plt.subplots(figsize=(13,13))
    ax.bar(reservation_purposes, total_reservations)
    ax.set_title('Total Reservations by Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Total Reservations')


    ax.set_xticks(range(len(reservation_purposes)))
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

    fig, ax = plt.subplots(figsize=(13,13))
    ax.bar(classroom_names, total_reservations)
    ax.set_title('Total Reservations by Classroom Name')
    ax.set_xlabel('Classroom Name')
    ax.set_ylabel('Total Reservations')


    ax.set_xticks(range(len(classroom_names)))
    ax.set_xticklabels(classroom_names)
    plt.xticks(rotation=45, ha="right")

    ax.set_yticks(range(0, max(total_reservations)+1, 5))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    png_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    html = f'<img src="data:image/png;base64,{png_image_base64}"/>'
    return html





