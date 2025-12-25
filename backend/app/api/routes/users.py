from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.api.routes.auth import get_current_user, get_optional_token
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
    current_user: User = Depends(get_current_user)
):
    """List all users. Admin can see all users, normal users can only see themselves."""
    if current_user.role == "admin":
        users = db.query(User).all()
    else:
        # Normal users can only see themselves
        users = [current_user]
    return users


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(get_optional_token)
):
    """Create a new user. If user is new, allow creation without auth. If user exists, require auth."""
    # Check if user email already exists (convert to lowercase for comparison)
    user_email_lower = user_in.user_email.lower()
    existing_user = db.query(User).filter(
        User.user_email == user_email_lower
    ).first()
    
    # If user exists, require authentication
    if existing_user:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User already exists. Authentication required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Verify the token is valid and belongs to this user
        from app.core.security import decode_access_token
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = payload["sub"]
        if user_id != existing_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this user"
            )
        # If we get here, user exists and is authenticated - return existing user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # User is new, allow creation without auth
    # Hash password
    hashed_password = get_password_hash(user_in.pwd)
    
    # Convert email to lowercase
    user_email_lower = user_in.user_email.lower()
    
    # Set default role to "normal" if not provided
    user_role = user_in.role if user_in.role else "normal"

    new_user = User(
        id=str(uuid4()),
        user_email=user_email_lower,
        user_name=user_in.user_name,
        pwd=hashed_password,
        role=user_role,
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
    current_user: User = Depends(get_current_user)
):
    """Get a user by ID. Admin can see any user, normal users can only see themselves."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Normal users can only see themselves
    if current_user.role != "admin" and user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to update their own account
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Check if email is being changed and if it's already taken
    if user_in.user_email and user_in.user_email.lower() != user.user_email:
        user_email_lower = user_in.user_email.lower()
        existing_user = db.query(User).filter(
            User.user_email == user_email_lower,
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        user.user_email = user_email_lower

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
    current_user: User = Depends(get_current_user)
):
    """Delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to delete their own account
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
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