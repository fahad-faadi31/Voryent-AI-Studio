import { useState, useEffect } from 'react'
import { listJobs } from '../api/jobs'
import { getImageUrl } from '../api/client'
import type { Job } from '../types'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

export default function HistoryPage() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadJobs()
  }, [])

  async function loadJobs() {
    setLoading(true)
    setError('')

    try {
      const response = await listJobs(1, 20)
      setJobs(response.items)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load history',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">
        Generation History
      </h1>

      {error && <ErrorMessage message={error} />}

      {loading && <LoadingSpinner />}

      {!loading && jobs.length === 0 && (
        <p className="text-gray-500 text-center py-12">
          No generations yet.
        </p>
      )}

      {!loading && jobs.length > 0 && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => {
            const imageUrl = getImageUrl(job.image_url)

            return (
              <div
                key={job.id}
                className="bg-white border border-gray-200 rounded-lg overflow-hidden"
              >
                {job.status === 'completed' && imageUrl && (
                  <img
                    src={imageUrl}
                    alt={job.prompt}
                    className="w-full h-48 object-cover"
                  />
                )}

                <div className="p-4">
                  <p className="text-sm text-gray-700 line-clamp-2">
                    {job.prompt}
                  </p>

                  <div className="flex items-center justify-between mt-2">
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        job.status === 'completed'
                          ? 'bg-green-100 text-green-700'
                          : job.status === 'failed'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-yellow-100 text-yellow-700'
                      }`}
                    >
                      {job.status}
                    </span>

                    <span className="text-xs text-gray-500">
                      {new Date(
                        job.created_at,
                      ).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}