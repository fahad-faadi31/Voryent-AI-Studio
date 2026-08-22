export interface User {
  id: string
  email: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export type AspectRatio = '1:1' | '16:9' | '9:16'

export interface GenerateRequest {
  prompt: string
  aspect_ratio: AspectRatio
  seed?: number | null
}

export type GenerateResponse = Job

export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed'

export interface Job {
  id: string
  user_id: string
  prompt: string
  status: JobStatus
  aspect_ratio: string
  seed: number | null
  image_url: string | null
  error_message: string | null
  created_at: string
  started_at: string | null
  completed_at: string | null
}

export interface JobListResponse {
  items: Job[]
  total: number
  page: number
  limit: number
  total_pages: number
}

