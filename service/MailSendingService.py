import smtplib
from flask import request

def getReservationInformation():
    reservation_info = []
    class_code = request.args.get('class-code')
    start_time = request.args.get('start-time')
    end_time = request.args.get('end-time')
    date = request.args.get('date')
    option = request.args.get('option')
    reservation_info.append(class_code)
    reservation_info.append(start_time)
    reservation_info.append(end_time)
    reservation_info.append(date)
    reservation_info.append(option)
    return reservation_info

def sendReservationInformationAsEmail():
    reservation_info = getReservationInformation()
    email = 'bkaplan10001@gmail.com'
    receiver_email = request.form.get('reservationInfoReceiver')
    random_password = 'cvvbsgxqkuziqgsd'
    protocol = 'smtp.gmail.com'
    
    email_subject = 'Your Reservation Information'
    email_content = 'Reservation Information:\n\n'
    email_content += f'Code of Reserved Class: {reservation_info[0]}\n'
    email_content += f'Reservation Start Time: {reservation_info[1]}\n'
    email_content += f'Reservation End Time: {reservation_info[2]}\n'
    email_content += f'Reservation Date: {reservation_info[3]}\n'
    email_content += f'Reservation Purpose: {reservation_info[4]}\n'
    
    message = f'Subject: {email_subject}\n\n{email_content}'
    
    smt = smtplib.SMTP(protocol, 587)
    smt.ehlo()
    smt.starttls()
    smt.login(email, random_password)
    smt.sendmail(email, receiver_email, message)
    smt.quit()
    
    return "Reservation information sent successfully!"

