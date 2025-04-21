from pydantic import BaseModel, Field
from typing import List, Optional

class WordForm(BaseModel):
    oppslag: str = Field(description="The inflected form of the word")
    tag: Optional[str] = Field(None, description="Grammatical tag information")
    boy_tekst: Optional[str] = Field(None, description="Description of the inflection")
    ordbok_tekst: Optional[str] = Field(None, description="Dictionary text for the inflection")

class WordResponse(BaseModel):
    grunnform: str = Field(description="The base form (lemma) of the word")
    ordklasse: str = Field(description="Part of speech (e.g., verb, substantiv)")
    forms: List[WordForm] = Field(description="All inflected forms of the word")

class ErrorResponse(BaseModel):
    detail: str = Field(description="Error message")