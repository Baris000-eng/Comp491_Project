import repository.UserRepository as UR

UR.initializeUserTables()
UR.initializeReservationsTable()
UR.intializeITReportLog()

print("environment set-up")
