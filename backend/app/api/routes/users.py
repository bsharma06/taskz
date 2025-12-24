from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.api.routes.auth import get_current_user, get_current_user_tenant_id
from typing import List, Optional

router = APIRouter()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """List all users in the current user's tenant."""
    users = db.query(User).filter(User.tenant_id == tenant_id).all()
    return users


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Create a new user in the current user's tenant."""
    # Ensure user is created in the same tenant as the current user
    if user_in.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create user in a different tenant"
        )

    # Verify tenant exists
    tenant = db.query(Tenant).filter(Tenant.id == user_in.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Check if user email already exists
    existing_user = db.query(User).filter(
        User.user_email == user_in.user_email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash password
    hashed_password = get_password_hash(user_in.pwd)

    new_user = User(
        id=str(uuid4()),
        user_email=user_in.user_email,
        user_name=user_in.user_name,
        pwd=hashed_password,
        tenant_id=user_in.tenant_id,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Get a user by ID (only if they belong to user's tenant)."""
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Update a user (only if they belong to user's tenant)."""
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if email is being changed and if it's already taken
    if user_in.user_email and user_in.user_email != user.user_email:
        existing_user = db.query(User).filter(
            User.user_email == user_in.user_email,
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        user.user_email = user_in.user_email

    if user_in.user_name is not None:
        user.user_name = user_in.user_name

    if user_in.pwd is not None:
        user.pwd = get_password_hash(user_in.pwd)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Delete a user (only if they belong to user's tenant)."""
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        db.delete(user)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )