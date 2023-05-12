import repository.UserRepository as UR
import repository.ClassroomRepository as CR
import repository.CourseRepository as COR
import repository.ExamRepository as EXR

UR.initializeUserTables()
UR.initializeReservationsTable()
UR.intializeITReportLog()
CR.initializeClassroomTables()
COR.initializeCourseTable()
EXR.initializeExamTable()
EXR.increment_exams_db()
UR.initializeChatTable()
UR.initializeNewsTable()
