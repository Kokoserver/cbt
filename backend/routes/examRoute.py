from os import getcwd, remove
import os
from typing import List, Optional
from fastapi import status, APIRouter, Form, File, UploadFile
from fastapi import Depends
from fastapi.responses import JSONResponse
from repository.authentication import get_current_user
from twilio.rest import Client
from odmantic.bson import ObjectId
from starlette.responses import FileResponse
from backend.model.examModel import (
    CandidateLogin,
    ExamModel,
    Candidate,
    ExamResponseModel,
    Question,
    Score,
)
from backend.schema.examSchema import Exam
from backend.schema.userSchema import User
from repository.db import DATABASE
from repository.utils import convert_csv_to_list_dict, convert_to_list_dict__to_excel


router = APIRouter()


# creating a new exam 
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_exam(
    candidate: UploadFile = File(...),
    question: UploadFile = File(...),
    duration: int = Form(...),
    title: str = Form(...),
    user: User = Depends(get_current_user),
):

    if not user.is_active:
        return JSONResponse(
            content={"message": {"AuthError": "Only admin can perfom this operation"}},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    questions = convert_csv_to_list_dict(question, model=Question)
    candidates = convert_csv_to_list_dict(candidate, model=Candidate)
    check_exam = await DATABASE.find_one(
        Exam,
        title == title and Exam.user == user.id,
    )
    if check_exam:
        return JSONResponse(
            content={"message": {"ExamExist": "Exam already exist"}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_exam = await DATABASE.save(
        Exam(
            question=questions,
            candidate=candidates,
            user=user,
            duration=duration,
            title=title,
        )
    )
    if new_exam:
        return {"message": "exam was created successfully"}

    return JSONResponse(
        content={
            "message": {
                "FileError": "incorect file details, please sure the file are in correct form"
            }
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )


# updating the existing question from the database
@router.put("/{examId}", status_code=status.HTTP_200_OK)
async def update_exam(
    examId: str,
    candidate: Optional[UploadFile] = File(default=None),
    question: Optional[UploadFile] = File(default=None),
    duration: int = Form(default=None),
    title: str = Form(...),
    user: User = Depends(get_current_user),
):

    if candidate or question or duration:
        if not user.is_active:
            return JSONResponse(
                content={
                    "message": {"AuthError": "Only admin can perfom this operation"}
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        check_exam: Exam = await DATABASE.find_one(Exam, Exam.id == ObjectId(examId))
        if not check_exam:
            return JSONResponse(
                {"message": {"ExamNotFound": f"Exam with {examId} is not found."}}
            )

        if question:
            questions = convert_csv_to_list_dict(question, model=Question)
            check_exam.question = questions
        if candidate:
            candidates = convert_csv_to_list_dict(candidate, model=Candidate)
            check_exam.candidate = candidates
        if duration:
            check_exam.duration = duration
        if title:
            check_exam.title = title

        if await DATABASE.save(check_exam):
            return {"message": "exam was updated successfully"}
        return JSONResponse(
            content={
                "message": {
                    "FileError": "incorect file details, please sure the file are in correct form"
                }
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# getting single exam 
@router.get(
    "/{examId}", response_model=ExamResponseModel, status_code=status.HTTP_200_OK
)
async def get_exams(
    examId: ObjectId,
    user: User = Depends(get_current_user),
):
    if user.is_active:
        find_exam: Exam = await DATABASE.find_one(Exam, Exam.id == examId)
        if find_exam:
            return find_exam
        return JSONResponse(
            content={"message": {"ExamNotFount": "Exam does not exist"}},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content={"message": {"AuthError": "Only admin can perfom this operation"}},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


# deleting single exam
@router.delete("/{examId}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_exam(
    examId: str,
    user: User = Depends(get_current_user),
):

    if user.is_active:
        find_exam: Exam = await DATABASE.find_one(Exam, Exam.id == ObjectId(examId))
        if find_exam:
            await DATABASE.delete(find_exam)
            try:
                remove(f"{getcwd()}/backend/results/{find_exam.title}.csv")
            except OSError:
                pass
            return {"message": "exam was deleted successfully"}
        return JSONResponse(
            content={"message": {"ExamNotFount": "Exam does not exist"}},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content={"message": {"AuthError": "Only admin can perfom this operation"}},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


# logging student with matric number and password
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_candidate(candidateExam: CandidateLogin):
    # check if student exist in the candidate table
    check_candidate: Exam = await DATABASE.find_one(
        Exam,
        {
            "candidate": {
                "$elemMatch": {
                    "matric_no": candidateExam.matric_no,
                    "password": candidateExam.password,
                    "score": 0,
                    "done": False,
                }
            }
        },
    )
# logging student if their details exist
    if check_candidate:
        return {
            "user": {"matric_no": candidateExam.matric_no},
            "question": check_candidate.question,
        }
    return JSONResponse(
        content={"message": {"Notfound": "you do not enroll for this exam"}},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


# adding student score to database and send them their result via SMS 
@router.post("/addscore", status_code=status.HTTP_200_OK)
async def save_exam_score(userScore: Score):
    check_candidate: Exam = await DATABASE.find_one(
        Exam,
        {
            "candidate": {
                "$elemMatch": {
                    "matric_no": userScore.candidateId,
                    "score": 0,
                    "done": False,
                }
            }
        },
    )

    if check_candidate:
        for candidate in check_candidate.candidate:
            if candidate.matric_no == userScore.candidateId:
                candidate.score = userScore.score
                candidate.done = True
                account_sid = os.getenv("SID")
                auth_token = os.getenv("TOKEN")
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"""
                    Exam result for {check_candidate.title}\n
                    matric No = {candidate.matric_no}\n
                    name = {candidate.password}\n
                    total = {userScore.score}\n
                    exam_status = done\n
                    """,
                    from_="+14845597884",
                    to=f"+{candidate.phone}",
                )

        await DATABASE.save(check_candidate)
        if message.status == "sent":
            return {
                "message": "score was added successfully, you will recieve your result soon"
            }
        return {"message": "score was added successfully"}
    return JSONResponse(
        content={"message": {"Notfound": "you do do not enroll for this exam"}},
        status_code=status.HTTP_404_NOT_FOUND,
    )


# GET ALL EXAM IN THE DATABASE
@router.get("/", response_model=List[Exam], status_code=status.HTTP_200_OK)
async def get_exams_results(
    user: User = Depends(get_current_user),
):
    if user.is_active:
        find_exam: Exam = await DATABASE.find(Exam)
        return find_exam if find_exam else []
    return []


# GET SINGLE RESULT FROM THE DATABASE
@router.get(
    "/{examId}/result", response_model=List[Candidate], status_code=status.HTTP_200_OK
)
async def get_exams_results(
    examId: ObjectId,
    user: User = Depends(get_current_user),
):
    if user.is_active:
        find_exam: Exam = await DATABASE.find_one(Exam, Exam.id == examId)
        if find_exam:
            pd = convert_to_list_dict__to_excel(find_exam.candidate)
            pd.to_csv(f"backend/results/{find_exam.title}.csv")
            return FileResponse(
                path=f"backend/results/{find_exam.title}.csv",
                media_type="application/octet-stream",
                filename=f"{find_exam.title}.csv",
            )
        return JSONResponse(
            content={"message": {"ExamNotFount": "Exam does not exist"}},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content={"message": {"AuthError": "Only admin can perfom this operation"}},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
