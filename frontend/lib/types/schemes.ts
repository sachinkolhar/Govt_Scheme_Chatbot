export interface Scheme {
  scheme_name: string;
  details: string;
  benefits: string;
  eligibility: string;
  application: string;
  documents: string;
  level: string;
  schemeCategory: string;
  tags: string;
  score: number;
  match_score?: number; // 0-100 percentage
  recommendation_reasons?: string[]; // Why this scheme is recommended
  is_favorite?: boolean; // Whether user has favorited this scheme
  source_title?: string | null;
  source_url?: string | null;
  source_type?: string | null;
  retrieved_at?: string | null;
}

export interface CategorySummary {
  category: string;
  count: number;
}

export interface EligibilityRequest {
  age?: number | null;
  gender?: string | null;
  state?: string | null;
  occupation?: string | null;
  income?: number | null;
  category?: string | null;
  disability: boolean;
  student_status: boolean;
  farmer_status: boolean;
  top_k: number;
}
