from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID

from app.services.supabase_client import get_supabase_client
from app.schemas.models import (
    Story,
    StoryCreate,
    StoryWithCharacters,
    ApiResponse,
    Character,
    StoryCharacterLink,
)

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("", response_model=ApiResponse)
async def list_stories(
    genre: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """List all stories with optional filtering."""
    try:
        client = get_supabase_client()
        query = client.table("stories").select("*")

        if genre:
            query = query.eq("genre", genre)
        if status:
            query = query.eq("status", status)

        response = query.range(offset, offset + limit - 1).execute()

        return ApiResponse.ok(
            data=response.data,
            meta={"total": len(response.data), "limit": limit, "offset": offset},
        )
    except Exception as e:
        return ApiResponse.fail(str(e))


@router.post("", response_model=ApiResponse)
async def create_story(story: StoryCreate):
    """Create a new story."""
    try:
        client = get_supabase_client()

        # Insert story
        story_data = story.model_dump(exclude={"character_ids"})
        story_response = client.table("stories").insert(story_data).execute()

        if not story_response.data:
            raise HTTPException(status_code=500, detail="Failed to create story")

        created_story = story_response.data[0]
        story_id = created_story["id"]

        # Link characters if provided
        if story.character_ids:
            character_links = [
                {"story_id": story_id, "character_id": char_id}
                for char_id in story.character_ids
            ]
            client.table("story_characters").insert(character_links).execute()

        return ApiResponse.ok(data=created_story)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")


@router.get("/{story_id}", response_model=ApiResponse)
async def get_story(story_id: UUID):
    """Get a specific story with its characters."""
    try:
        client = get_supabase_client()

        # Get story
        story_response = (
            client.table("stories")
            .select("*")
            .eq("id", str(story_id))
            .single()
            .execute()
        )

        if not story_response.data:
            raise HTTPException(status_code=404, detail="Story not found")

        story = story_response.data

        # Get linked characters
        characters_response = (
            client.table("story_characters")
            .select("character_id, role_in_story, characters(*)")
            .eq("story_id", str(story_id))
            .execute()
        )

        story["characters"] = (
            [item["characters"] for item in characters_response.data]
            if characters_response.data
            else []
        )

        return ApiResponse.ok(data=story)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch story: {str(e)}")


@router.patch("/{story_id}", response_model=ApiResponse)
async def update_story(story_id: UUID, story_update: dict):
    """Update a story (partial update)."""
    try:
        client = get_supabase_client()

        response = (
            client.table("stories")
            .update(story_update)
            .eq("id", str(story_id))
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Story not found")

        return ApiResponse.ok(data=response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update story: {str(e)}")


@router.delete("/{story_id}", response_model=ApiResponse)
async def delete_story(story_id: UUID):
    """Delete a story and all related data."""
    try:
        client = get_supabase_client()

        response = client.table("stories").delete().eq("id", str(story_id)).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Story not found")

        return ApiResponse.ok(data={"deleted": True, "story_id": str(story_id)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete story: {str(e)}")


@router.post("/{story_id}/characters", response_model=ApiResponse)
async def add_character_to_story(story_id: UUID, link: StoryCharacterLink):
    """Add a character to a story."""
    try:
        client = get_supabase_client()

        link_data = {
            "story_id": str(story_id),
            "character_id": str(link.character_id),
            "role_in_story": link.role_in_story,
        }

        response = client.table("story_characters").insert(link_data).execute()

        return ApiResponse.ok(data=response.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add character: {str(e)}"
        )
