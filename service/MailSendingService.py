import smtplib
from flask import request, render_template
import service.ReservationService as RS
import string

def sendReservationInformationAsEmail():
    reservation_info = RS.getReservationInformation()
    reservation_code = RS.generate_classroom_reservation_code()
    print("Reservation Information: " + str(reservation_info))

    email = 'bkaplan10001@gmail.com'
    receiver_email = request.form.get('reservationInfoReceiver')
    random_password = 'cvvbsgxqkuziqgsd'
    protocol = 'smtp.gmail.com'

    email_subject = 'Your Reservation Information'
    email_content = f"""Subject: {email_subject}

    Dear {reservation_info[0]},

    Thank you for making a reservation. Below are the details of your reservation:

    Reservation Code: {reservation_code}
    Reserver Username: {reservation_info[0]}
    Reserver Role: {reservation_info[1]}
    Reserver Priority: {reservation_info[2]}
    Reserved Class Code: {reservation_info[3]}
    Reservation Start Time: {reservation_info[4]}
    Reservation End Time: {reservation_info[5]}
    Reservation Duration: {RS.calculateDuration(reservation_info[4], reservation_info[5])} minutes
    Reservation Date: {reservation_info[6]}
    Reservation Purpose: {reservation_info[7]}

    If you have any questions or need further assistance, please feel free to contact us.

    Best regards,
    KuClass Team
    """

    smt = smtplib.SMTP(protocol, 587)
    smt.ehlo()
    smt.starttls()
    smt.login(email, random_password)
    smt.sendmail(email, receiver_email, email_content)
    smt.quit()

    return render_template("successful_reservation_information_sending.html")

def sendReservationOverrideMail(usernames):
    email = 'bkaplan10001@gmail.com'
    receiver_email = 'kuclass2023@gmail.com'
    random_password = 'cvvbsgxqkuziqgsd'
    protocol = 'smtp.gmail.com'

    result = ", ".join(usernames)

    email_subject = 'Your Reservation was Overriden'
    email_content = f"""Subject: {email_subject}


    Dear {result},

    Your reservations were overriden. Please check your reservations to get more information on your overriden reservations.

    If you have any questions or need further assistance, please feel free to contact us.

    Best regards,
    KuClass Team
    """

    smt = smtplib.SMTP(protocol, 587)
    smt.ehlo()
    smt.starttls()
    smt.login(email, random_password)
    smt.sendmail(email, receiver_email, email_content)
    smt.quit()

    return ""


