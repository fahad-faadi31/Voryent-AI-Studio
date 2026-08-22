import { apiFetch } from './client'
import type { Job, JobListResponse } from '../types'

export async function getJob(jobId: string): Promise<Job> {
  return apiFetch<Job>(`/jobs/${jobId}`)
}

export async function listJobs(
  page: number = 1,
  limit: number = 20,
): Promise<JobListResponse> {
  return apiFetch<JobListResponse>(
    `/jobs?page=${page}&limit=${limit}`,
  )
}