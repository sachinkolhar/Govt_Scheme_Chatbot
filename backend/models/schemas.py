"""
Pydantic request/response schemas for API endpoints.
"""
from datetime import datetime
import time
from typing import Literal, Optional, List
from pydantic import BaseModel, Field


# ---- Auth Models ----
class UserSignup(BaseModel):
    """Request model for user signup."""
    username: str
    name: str
    password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    category: Optional[str] = None
    disability: bool = False
    student_status: bool = False
    farmer_status: bool = False


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str


class UserProfileUpdate(BaseModel):
    """Request model for updating user profile."""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    category: Optional[str] = None
    disability: Optional[bool] = None
    student_status: Optional[bool] = None
    farmer_status: Optional[bool] = None


class UserPublic(BaseModel):
    """Public user information (no sensitive data)."""
    id: int
    username: str
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    category: Optional[str] = None
    disability: bool = False
    student_status: bool = False
    farmer_status: bool = False
    profile_photo_path: Optional[str] = None
    profile_photo_updated_at: Optional[str] = None


class TokenResponse(BaseModel):
    """Response containing authentication token and user info."""
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


# ---- Chat Models ----
class ConversationMessage(BaseModel):
    """Message in a conversation history."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str
    top_k: int = 1
    history: List[ConversationMessage] = Field(default_factory=list)
    conversation_id: Optional[str] = None
    language: str = "en"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    query: str
    answer: str
    response_type: str = "direct_answer"
    source_scheme: Optional["SchemeResult"] = None
    relevant_schemes: List["SchemeResult"] = Field(default_factory=list)
    sources: List["ChatSource"] = Field(default_factory=list)


class ChatSource(BaseModel):
    title: str
    url: str
    source_type: str = "official"
    retrieved_at: Optional[str] = None


# ---- Search Models ----
class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query: str
    top_k: int = 5


class SchemeResult(BaseModel):
    """Single scheme search result."""
    scheme_name: str
    details: str
    benefits: str
    eligibility: str
    application: str
    documents: str
    level: str
    schemeCategory: str
    tags: str
    score: float = 0.0
    match_score: int = 0  # 0-100 percentage
    recommendation_reasons: List[str] = Field(default_factory=list)  # Why this scheme is recommended
    is_favorite: bool = False  # Whether user has favorited this scheme
    source_title: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    retrieved_at: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    results: List[SchemeResult] = Field(default_factory=list)


# ---- Eligibility Models ----
class EligibilityRequest(BaseModel):
    """Request model for eligibility checking."""
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    category: Optional[str] = None
    disability: bool = False
    student_status: bool = False
    farmer_status: bool = False
    top_k: int = 10


class FavoriteSchemeResponse(BaseModel):
    """Response model for favorite scheme."""
    scheme_name: str
    scheme_id: str
    created_at: Optional[str] = None


class FavoritesListResponse(BaseModel):
    """Response model for list of favorite schemes."""
    schemes: List[FavoriteSchemeResponse] = Field(default_factory=list)
    total_count: int = 0


# ---- Reminder Models ----
ReminderType = Literal["deadline", "saved_event", "custom"]


class ReminderCreate(BaseModel):
    """Request model for creating reminders."""

    title: str
    description: Optional[str] = None
    reminder_date: datetime
    related_scheme_name: Optional[str] = None
    reminder_type: ReminderType = "custom"


class ReminderUpdate(BaseModel):
    """Request model for updating reminders."""

    title: Optional[str] = None
    description: Optional[str] = None
    reminder_date: Optional[datetime] = None
    related_scheme_name: Optional[str] = None
    reminder_type: Optional[ReminderType] = None


class ReminderResponse(BaseModel):
    """Response model for reminder records."""

    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    reminder_date: str
    related_scheme_name: Optional[str] = None
    reminder_type: ReminderType
    created_at: str
    updated_at: str


class ReminderListResponse(BaseModel):
    """Response model for listing reminders."""

    reminders: List[ReminderResponse] = Field(default_factory=list)
    total_count: int = 0


# ---- Document Models ----
DocumentType = Literal[
    "aadhaar_card",
    "pan_card",
    "income_certificate",
    "caste_certificate",
    "disability_certificate",
    "land_documents",
    "other",
]


class UserDocumentResponse(BaseModel):
    """Response model for user document metadata."""

    id: int
    user_id: int
    document_type: DocumentType
    original_name: str
    mime_type: str
    file_size: int
    relative_path: str
    created_at: str


class UserDocumentListResponse(BaseModel):
    """Response model for user document list."""

    documents: List[UserDocumentResponse] = Field(default_factory=list)
    total_count: int = 0


class DocumentUploadResponse(BaseModel):
    """Response model for successful document upload."""

    message: str
    document: UserDocumentResponse


class ProfilePhotoResponse(BaseModel):
    """Response model for profile photo metadata."""

    profile_photo_path: Optional[str] = None
    profile_photo_updated_at: Optional[str] = None


class CategoryResponse(BaseModel):
    """Response for category statistics."""
    category: str
    count: int


# ---- Voice Models ----
class VoiceAssistantChatRequest(BaseModel):
    """Request model for voice assistant chat."""
    query: str
    language: str = "en"
    history: List[ConversationMessage] = Field(default_factory=list)
    conversation_id: Optional[str] = None


class VoiceAssistantChatResponse(BaseModel):
    """Response model for voice assistant chat."""
    query: str
    answer: str
    language: str = "en"


class VoiceEligibilityCriteriaRequest(BaseModel):
    """Request model for voice eligibility criteria."""
    scheme_name: str
    language: str = "en"


class VoiceEligibilityCriterion(BaseModel):
    """Single eligibility criterion."""
    key: str
    label: str
    question: str
    expected: str
    description: str = ""


class VoiceEligibilityCriteriaResponse(BaseModel):
    """Response model for voice eligibility criteria."""
    scheme_name: str
    language: str = "en"
    criteria: List[VoiceEligibilityCriterion] = Field(default_factory=list)


# ---- Speech Models ----
class SpeechRequest(BaseModel):
    """Request for speech-to-text transcription or text-to-speech synthesis."""
    audio_base64: Optional[str] = None  # Base64-encoded audio for transcription
    text: Optional[str] = None  # Text to synthesize for TTS
    language: str = "en"  # Language code: en, hi, te, ta
    format: str = "wav"  # Audio format: wav, webm, mp3, ogg, m4a, mp4, flac


class SpeechResponse(BaseModel):
    """Response for speech operations."""
    success: bool
    data: Optional[str] = None  # Base64-encoded audio (TTS) or transcribed text (STT)
    error: Optional[str] = None
    language: str = "en"


# ---- Chat State Model ----
class ChatState(BaseModel):
    """State tracking for multi-turn conversations."""
    pending_relevant_suggestions: bool = False
    last_query: str = ""
    pending_question: Optional[str] = None
    required_field: Optional[str] = None
    clarification_context: str = ""
    previous_candidates: List[dict] = Field(default_factory=list)
    collected_facts: dict = Field(default_factory=dict)
    conversation_id: str = ""
    last_user_query: str = ""
    rewritten_query: str = ""
    active_scheme_id: Optional[str] = None
    active_scheme_name: Optional[str] = None
    recent_retrieved_scheme_ids: List[str] = Field(default_factory=list)
    last_intent: str = "unknown"
    target_group_context: Optional[str] = None
    pending_action: Optional[str] = None
    pending_original_query: Optional[str] = None
    language: str = "en"
    updated_at: float = Field(default_factory=time.time)


ChatResponse.model_rebuild()
