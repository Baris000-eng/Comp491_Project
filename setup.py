import repository.UserRepository as UR
import repository.ClassroomRepository as CR

UR.initializeUserTables()
UR.initializeReservationsTable()
UR.intializeITReportLog()
CR.initializeClassroomTables()
UR.initializeChatTable()
UR.initializeNewsTable()
