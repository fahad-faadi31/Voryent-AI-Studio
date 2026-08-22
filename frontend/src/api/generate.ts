import { apiFetch } from './client'
import type { GenerateRequest, GenerateResponse } from '../types'

export async function createGeneration(
  data: GenerateRequest,
): Promise<GenerateResponse> {
  return apiFetch<GenerateResponse>('/generate', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}