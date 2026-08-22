const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || 'http://127.0.0.1:8000'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `${API_ORIGIN}/api/v1`

export class ApiError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.status = status
    this.detail = detail
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const token = localStorage.getItem('access_token')

  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const errorBody = await response
      .json()
      .catch(() => ({ detail: 'Request failed' }))

    throw new ApiError(
      response.status,
      errorBody.detail || errorBody.message || 'Request failed',
    )
  }

  return response.json()
}

export function getImageUrl(imageUrl: string | null): string | null {
  if (!imageUrl) return null

  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl
  }

  const filename = imageUrl.replace(/\\/g, '/').split('/').pop()

  if (!filename) return null

  return `${API_ORIGIN}/storage/generated/${filename}`
}

export { API_ORIGIN, API_BASE_URL }