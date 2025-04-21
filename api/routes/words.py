from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional

from ..models import WordResponse, WordForm
from ..database import get_db_connection

router = APIRouter()

@router.get("/words/{word}", response_model=List[WordResponse])
def get_word_info(
    word: str = Path(..., description="The word to look up"),
    ordklasse: Optional[str] = Query(None, description="Filter by part of speech (e.g., 'verb', 'subst')")
):
    """
    Get all information about a word, including its inflection forms.
    Optionally filter by part of speech.
    """
    conn = get_db_connection()
    try:
        # First check if the word exists as a lemma
        cursor = conn.execute("SELECT LEMMA_ID, GRUNNFORM FROM LEMMA WHERE GRUNNFORM = ?", (word,))
        lemmas = cursor.fetchall()
        
        if not lemmas:
            raise HTTPException(status_code=404, detail=f"Word '{word}' not found")
        
        results = []
        
        for lemma in lemmas:
            lemma_id = lemma["LEMMA_ID"]
            
            # Get part of speech for this lemma
            cursor = conn.execute("""
                SELECT DISTINCT p.ORDKLASSE
                FROM PARADIGME p
                JOIN LEMMA_PARADIGME lp ON p.PARADIGME_ID = lp.PARADIGME_ID
                WHERE lp.LEMMA_ID = ?
            """, (lemma_id,))
            
            pos_rows = cursor.fetchall()
            
            for pos_row in pos_rows:
                pos = pos_row["ORDKLASSE"]
                
                # Skip if ordklasse filter is specified and doesn't match
                if ordklasse and pos != ordklasse:
                    continue
                
                # Get all word forms
                query = """
                SELECT DISTINCT
                    f.OPPSLAG,
                    f.TAG,
                    b.BOY_TEKST,
                    b.ORDBOK_TEKST
                FROM
                    LEMMA l
                JOIN FULLFORMSLISTE f ON l.LEMMA_ID = f.LEMMA_ID
                LEFT JOIN PARADIGME_BOYING pb
                    ON f.PARADIGME_ID = pb.PARADIGME_ID AND f.BOY_NUMMER = pb.BOY_NUMMER
                LEFT JOIN BOYING b
                    ON pb.BOY_NUMMER = b.BOY_NUMMER AND pb.BOY_GRUPPE = b.BOY_GRUPPE
                WHERE
                    l.LEMMA_ID = ?
                    AND f.NORMERING = 'normert'
                ORDER BY f.OPPSLAG;
                """
                
                cursor = conn.execute(query, (lemma_id,))
                rows = cursor.fetchall()
                
                if rows:
                    forms = [
                        WordForm(
                            oppslag=row["OPPSLAG"],
                            tag=row["TAG"],
                            boy_tekst=row["BOY_TEKST"],
                            ordbok_tekst=row["ORDBOK_TEKST"]
                        ) for row in rows
                    ]
                    
                    results.append(
                        WordResponse(
                            grunnform=lemma["GRUNNFORM"],
                            ordklasse=pos,
                            forms=forms
                        )
                    )
        
        if not results and ordklasse:
            raise HTTPException(
                status_code=404, 
                detail=f"Word '{word}' not found with part of speech '{ordklasse}'"
            )
        
        return results
    
    finally:
        conn.close()

@router.get("/search/", response_model=List[str])
def search_words(
    q: str = Query(..., min_length=1, description="Search query for words starting with this string"),
    limit: int = Query(10, gt=0, le=100, description="Maximum number of results to return")
):
    """Search for words starting with the query string"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT DISTINCT GRUNNFORM FROM LEMMA WHERE GRUNNFORM LIKE ? ORDER BY GRUNNFORM LIMIT ?",
            (f"{q}%", limit)
        )
        return [row["GRUNNFORM"] for row in cursor.fetchall()]
    finally:
        conn.close()

@router.get("/ordklasser/", response_model=List[str])
def get_parts_of_speech():
    """Get all available parts of speech in the database"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT DISTINCT ORDKLASSE FROM PARADIGME WHERE ORDKLASSE IS NOT NULL ORDER BY ORDKLASSE"
        )
        return [row["ORDKLASSE"] for row in cursor.fetchall()]
    finally:
        conn.close()