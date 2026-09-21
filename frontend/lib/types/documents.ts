export type DocumentType =
  | "aadhaar_card"
  | "pan_card"
  | "income_certificate"
  | "caste_certificate"
  | "disability_certificate"
  | "land_documents"
  | "other";

export interface UserDocument {
  id: number;
  user_id: number;
  document_type: DocumentType;
  original_name: string;
  mime_type: string;
  file_size: number;
  relative_path: string;
  created_at: string;
}

export interface UserDocumentListResponse {
  documents: UserDocument[];
  total_count: number;
}

export interface DocumentUploadResponse {
  message: string;
  document: UserDocument;
}

export interface DeleteDocumentResponse {
  message: string;
  success: boolean;
}
