from litestar import get
from ports.http.web.v1.schemas.skill import ReadSkillSchema


@get("/skills", tags=["skill"])
async def get_skills() -> ReadSkillSchema:
    return ReadSkillSchema.from_app()
