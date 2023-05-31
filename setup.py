import repository.UserRepository as UR
import repository.ClassroomRepository as CR
import repository.CourseRepository as COR
import repository.ExamRepository as EXR
import repository.ReservationRepository as RR
import repository.UserReservationRepository as URMR

UR.initializeUserTables()
RR.initializeReservationsTable()
UR.intializeITReportLog()
CR.initializeClassroomTables()
COR.initializeCourseTable()
EXR.initializeExamTable()
UR.initializeChatTable()
UR.initializeNewsTable()
UR.initializeEventAnnouncementsTable()
URMR.initializeUserReservationsTable()
