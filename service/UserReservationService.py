import repository.UserReservationRepository as URR

def createUserReservation(reservation_id: str, user_id: str, is_owner: bool):
    URR.createUserReservation(reservation_id, user_id, is_owner)

def deleteUserReservation(reservation_id, user_id):
    URR.deleteUserReservation(reservation_id, user_id)

def getNumberOfUsersInReservation(reservation_id):
    return URR.getNumberOfUsersInReservation(reservation_id)

