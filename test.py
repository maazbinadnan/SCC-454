from typing import List

def topStudents(positive_feedback: List[str], negative_feedback: List[str], report: List[str], student_id: List[int], k: int) -> List[int]:
    student = {}
    for j in range(k):
        feedback = report[j].split()
        score = 0
        for words in feedback:
            if words in positive_feedback:
                score +=1 
            elif words in negative_feedback:
                score -=1
            student[student_id[j]] = score
    return list(student.keys())

positive_feedback = ["smart","brilliant","studious"]
negative_feedback = ["not"]
report = ["this student is studious","the student is smart"]
student_id = [1,2]
k = 2

print(topStudents(positive_feedback=positive_feedback,negative_feedback=negative_feedback,report=report,student_id=student_id,k=k))