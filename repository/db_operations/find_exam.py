from odmantic import ObjectId, query
from backend.lecturer.schema import Lecturer
from repository.db import db as exam_collection
from backend.exam.schema import Candidate, Exam
from odmantic.exceptions import KeyNotFoundInDocumentError, DocumentNotFoundError


class Exam_operations:
    @staticmethod
    async def find_exam_by_ID(examcode):
        try:
            exam = await exam_collection.find_one(Exam, Exam.examcode == examcode)
            return exam
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    async def find_all_exam(skip=0):
        try:
            exams = await exam_collection.find(Exam, skip=skip, sort=Exam.id)
            return exams
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    async def find_candidate(candidate: Candidate):
        try:
            # TODO FIND MATCHED CANDIDATE
            # query.match(Exam.candidate.__contains__(matric_no))
            exams = exam_collection.find(Exam)
            if exams:
                cand = [
                    cand_data
                    for cand_data in exams.candidate
                    if cand_data.matric_no == candidate.matric_no
                    and cand_data.password == candidate.password
                ]

            if cand:
                return cand[0]
            return False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    async def find_by_lecturer(lecturer: Lecturer):
        try:
            exams = await exam_collection.find(
                Exam, Exam.lecturerId == lecturer.id, sort=Exam.id
            )
            return exams
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def all_questions(skip: int = 5, limit: int = 10, sort: str = None):
        try:
            exams = await exam_collection.find(
                Exam, limit=limit, skip=skip, sort=Exam.id
            )
            return exams
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    # @staticmethod
    # async def find_exam_by_ID(id: str):
    #     try:
    #         exams = await exam_collection.find_one(Exam, Exam.id == id)
    #         print(exams, "jsdhsdjksdjfksdjhfs")
    #         return exams
    #     except DocumentNotFoundError:
    #         return False
    #     except KeyNotFoundInDocumentError:
    #         return False
    #     except Exception:
    #         return False

    @staticmethod
    async def filter_question(id: str):
        try:
            exams = await exam_collection.find_one(Exam, Exam.id == id)
            if exams:
                return exams
            exams = await exam_collection.find()
            return exams
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def save_exam(exam: Exam):
        saved_question = await exam_collection.save(Exam(**exam.dict()))
        return saved_question if saved_question else False

    @staticmethod
    async def delete_question(exam: Exam):
        deleted_question = await exam_collection.delete(exam)
        return True if deleted_question else False
