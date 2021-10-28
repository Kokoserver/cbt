from odmantic import ObjectId
from repository.db import db as question_collection
from backend.question.schema import Question
from odmantic.exceptions import KeyNotFoundInDocumentError, DocumentNotFoundError


class Question_operations:
    @staticmethod
    async def find_question_by_ID(id: ObjectId):
        try:
            question = await question_collection.find_one(Question, Question.id == id)
            return question
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def all_questions(skip:int=5, limit:int = 10, sort:str = None):
        try:
            question = await question_collection.find(Question, limit=limit, skip=skip, sort=Question.id | sort)
            return question
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_question_by_question(question: str):
        try:
            question = await question_collection.find_one(Question, Question.question == question)
            return question
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_question_by_code(code: str):
        try:
            question = await question_collection.find_one(Question, Question.code == code)
            return question
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def filter_question(filterBy, filterType: str):
        try:
            if filterType == "semester":
                question = await question_collection.find_one(
                    Question, Question.semester == filterBy
                )
                return question
            if filterType == "unit":
                question = await question_collection.find_one(
                    Question, Question.unit == filterBy
                )
                return question
            if filterType == "level":
                question = await question_collection.find_one(
                    Question, Question.level == filterBy
                )
                return question
            if filterType == "id":
                question = await question_collection.find_one(
                    Question, Question.id == ObjectId(filterBy)
                )

                return question
            question = await question_collection.find()
            return question
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_question_semester(semester: str):
        try:
            question = await question_collection.find_one(
                Question, Question.semester == semester
            )
            return question if question else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_question_semester_and_level(
        semester: str, level:int
    ):
        try:
            question = await question_collection.find(
                Question,
                Question.semester == semester
                and Question.level == int(level)
            )
            return question if question else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    async def find_question_by_either(find_by: Question):
        try:
            question = await question_collection.find_one(
                Question, Question.question == find_by.question and Question.level == find_by.level
            )
            return question if question else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def get_all_question():
        try:
            question = await question_collection.find(Question)
            return question if question else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def save_question(question: Question):
        saved_question = await question_collection.save(Question(**question.dict()))
        return saved_question if saved_question else False

    @staticmethod
    async def delete_question(question: Question):
        deleted_question = await question_collection.delete(question)
        return True if deleted_question else False
