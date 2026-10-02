from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from models import User, Application
from schemas import ApplicationCreate, ApplicationResponse,  ApplicationStatusUpdate



app = FastAPI(
    title="Job Application API",
    description="API for managing job applications",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Job Application API is running"
    }


@app.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):    
    # Check that the user exists
    user = db.get(User, application.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create application object
    new_application = Application(
        user_id=application.user_id,
        company_name=application.company_name,
        job_title=application.job_title,
        job_description=application.job_description
    )

    # Add to database
    db.add(new_application)

    # Save transaction
    db.commit()

    # Load generated values such as UUID, status, timestamps
    db.refresh(new_application)

    return new_application


@app.get(
    "/applications",
    response_model=list[ApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db)
):
    applications = (
        db.query(Application)
        .order_by(Application.created_at.desc())
        .all()
    )
    return applications
@app.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application
@app.put(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def update_application(
    application_id: UUID,
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    existing_application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if existing_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    # Make sure the new user exists
    user = db.get(User, application.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    existing_application.user_id = application.user_id
    existing_application.company_name = application.company_name
    existing_application.job_title = application.job_title
    existing_application.job_description = application.job_description

    db.commit()
    db.refresh(existing_application)

    return existing_application
@app.delete(
    "/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_application(
    application_id: UUID,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return None
@app.patch(
    "/applications/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: UUID,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    application.status = status_update.status.value

    db.commit()
    db.refresh(application)

    return application