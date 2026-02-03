from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID

from app.services.supabase_client import get_supabase_client
from app.schemas.models import Character, CharacterCreate, ApiResponse

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("", response_model=ApiResponse)
async def list_characters(
    limit: int = Query(default=10, ge=1, le=100), offset: int = Query(default=0, ge=0)
):
    """List all characters."""
    try:
        client = get_supabase_client()
        response = (
            client.table("characters")
            .select("*")
            .range(offset, offset + limit - 1)
            .execute()
        )

        return ApiResponse.ok(
            data=response.data,
            meta={"total": len(response.data), "limit": limit, "offset": offset},
        )
    except Exception as e:
        return ApiResponse.fail(str(e))


@router.post("", response_model=ApiResponse)
async def create_character(character: CharacterCreate):
    """Create a new character."""
    try:
        client = get_supabase_client()

        character_data = character.model_dump()
        response = client.table("characters").insert(character_data).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create character")

        return ApiResponse.ok(data=response.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create character: {str(e)}"
        )


@router.get("/{character_id}", response_model=ApiResponse)
async def get_character(character_id: UUID):
    """Get a specific character."""
    try:
        client = get_supabase_client()
        response = (
            client.table("characters")
            .select("*")
            .eq("id", str(character_id))
            .single()
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Character not found")

        return ApiResponse.ok(data=response.data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch character: {str(e)}"
        )


@router.patch("/{character_id}", response_model=ApiResponse)
async def update_character(character_id: UUID, character_update: dict):
    """Update a character."""
    try:
        client = get_supabase_client()
        response = (
            client.table("characters")
            .update(character_update)
            .eq("id", str(character_id))
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Character not found")

        return ApiResponse.ok(data=response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update character: {str(e)}"
        )


@router.delete("/{character_id}", response_model=ApiResponse)
async def delete_character(character_id: UUID):
    """Delete a character."""
    try:
        client = get_supabase_client()
        response = (
            client.table("characters").delete().eq("id", str(character_id)).execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Character not found")

        return ApiResponse.ok(data={"deleted": True, "character_id": str(character_id)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete character: {str(e)}"
        )
