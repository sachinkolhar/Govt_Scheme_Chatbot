"""Eligibility API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

try:
    from ..auth.dependencies import get_current_user
    from ..config.database import SessionLocal
    from ..models.database import User, Favorite
    from ..models.schemas import EligibilityRequest, SchemeResult, FavoriteSchemeResponse, FavoritesListResponse
    from .checker import get_personalized_schemes, profile_from_user
except ImportError:
    from auth.dependencies import get_current_user
    from config.database import SessionLocal
    from models.database import User, Favorite
    from models.schemas import EligibilityRequest, SchemeResult, FavoriteSchemeResponse, FavoritesListResponse
    from eligibility.checker import get_personalized_schemes, profile_from_user


router = APIRouter(prefix="/api", tags=["eligibility"])


@router.post("/find-eligible", response_model=list[SchemeResult])
def find_eligible(payload: EligibilityRequest) -> list[SchemeResult]:
    return get_personalized_schemes(payload, top_k=payload.top_k, user_id=None)


@router.get("/recommendations", response_model=list[SchemeResult])
def recommendations(
    top_k: int = Query(default=6, ge=1, le=25),
    current_user: User = Depends(get_current_user),
) -> list[SchemeResult]:
    profile = profile_from_user(current_user, top_k=top_k)
    return get_personalized_schemes(profile, top_k=top_k, user_id=current_user.id)


@router.post("/favorites/{scheme_id}", response_model=dict)
def add_favorite(
    scheme_id: str,
    scheme_name: str = Query(...),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Add a scheme to user's favorites."""
    db = SessionLocal()
    try:
        # Check if already favorited
        existing = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.scheme_id == scheme_id,
        ).first()
        
        if existing:
            return {"message": "Already in favorites", "success": True}
        
        favorite = Favorite(
            user_id=current_user.id,
            scheme_id=scheme_id,
            scheme_name=scheme_name,
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        
        return {"message": "Added to favorites", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.delete("/favorites/{scheme_id}", response_model=dict)
def remove_favorite(
    scheme_id: str,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Remove a scheme from user's favorites."""
    db = SessionLocal()
    try:
        favorite = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.scheme_id == scheme_id,
        ).first()
        
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        db.delete(favorite)
        db.commit()
        
        return {"message": "Removed from favorites", "success": True}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/favorites", response_model=FavoritesListResponse)
def get_favorites(current_user: User = Depends(get_current_user)) -> FavoritesListResponse:
    """Get user's favorite schemes."""
    db = SessionLocal()
    try:
        favorites = db.query(Favorite).filter(
            Favorite.user_id == current_user.id
        ).order_by(Favorite.created_at.desc()).all()
        
        schemes = [
            FavoriteSchemeResponse(
                scheme_name=f.scheme_name,
                scheme_id=f.scheme_id,
                created_at=f.created_at.isoformat() if f.created_at else None,
            )
            for f in favorites
        ]
        
        return FavoritesListResponse(
            schemes=schemes,
            total_count=len(schemes),
        )
    finally:
        db.close()
