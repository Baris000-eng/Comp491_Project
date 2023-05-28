from repository import UserReservationRepository as URR

def createUserReservation(reservation_id: str, user_id: str, is_owner: bool):
    URR.createUserReservation(reservation_id, user_id, is_owner)

