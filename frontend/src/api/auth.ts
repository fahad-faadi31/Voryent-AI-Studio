import { apiFetch } from './client'
import type { AuthResponse } from '../types'

export async function register(
  email: string,
  password: string,
): Promise<void> {
  await apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    }),
  })
}

export async function login(
  email: string,
  password: string,
): Promise<AuthResponse> {
  return apiFetch<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    }),
  })
}