import smtplib
from flask import request
import service.ReservationService as RS

def sendReservationInformationAsEmail():
    reservation_info = RS.getReservationInformation()
    reservation_code = RS.generate_classroom_reservation_code()
    print("Reservation Information: "+str(reservation_info))
    email = 'bkaplan10001@gmail.com'
    receiver_email = request.form.get('reservationInfoReceiver')
    random_password = 'cvvbsgxqkuziqgsd'
    protocol = 'smtp.gmail.com'
    
    email_subject = 'Your Reservation Information'
    email_content = 'Reservation Information:\n\n'
    email_content += f'Your reservation code: {reservation_code}\n'
    email_content += f'Your username: {reservation_info[0]}\n'
    email_content += f'Your role: {reservation_info[1]}\n'
    email_content += f'Your priority: {reservation_info[2]}\n'
    email_content += f'Code of Reserved Class: {reservation_info[3]}\n'
    email_content += f'Reservation Start Time: {reservation_info[4]}\n'
    email_content += f'Reservation End Time: {reservation_info[5]}\n'
    email_content += f'Reservation Date: {reservation_info[6]}\n'
    email_content += f'Reservation Purpose: {reservation_info[7]}\n'
    
    message = f'Subject: {email_subject}\n\n{email_content}'
    
    smt = smtplib.SMTP(protocol, 587)
    smt.ehlo()
    smt.starttls()
    smt.login(email, random_password)
    smt.sendmail(email, receiver_email, message)
    smt.quit()
    
    return "Reservation information sent successfully!"

