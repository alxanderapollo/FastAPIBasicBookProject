from fastapi import APIRouter
'''
    In this app you could have multiple API routes, in this one we have an authication route
    the only one way to run this would be to turn off the main app, but then we would lose access to our main app
    end points, and so the way to deal with this is tell FastAPI, we have an extra route for x items in this case auth

    from this file we wxport auth routes to our main API file
'''
router = APIRouter()
@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}