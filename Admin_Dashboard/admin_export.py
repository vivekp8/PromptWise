from fastapi import APIRouter, Depends, HTTPException
from PromptWise.utils.jwt_utils import get_current_user

router = APIRouter(prefix="/admin/export", tags=["Export System"])

@router.get("/logs")
def export_logs(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return {
        "export": "audit logs",
        "generated_by": user["username"],
        "status": "ready"
    }