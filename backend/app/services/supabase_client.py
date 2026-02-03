"""Supabase client configuration and utilities."""

from supabase import create_client, Client
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Supabase client instance
supabase: Optional[Client] = None


def get_supabase_client() -> Client:
    """Get or create Supabase client instance."""
    global supabase

    if supabase is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
            )

        supabase = create_client(supabase_url, supabase_key)

    return supabase


async def check_connection() -> bool:
    """Check if Supabase connection is working."""
    try:
        client = get_supabase_client()
        # Try a simple query
        response = (
            client.table("stories").select("count", count="exact").limit(1).execute()
        )
        return True
    except Exception as e:
        print(f"Supabase connection check failed: {e}")
        return False
