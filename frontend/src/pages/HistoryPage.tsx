import { useEffect, useState } from 'react'
import { listJobs } from '../api/jobs'
import { getImageUrl } from '../api/client'
import type { Job } from '../types'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

const PAGE_SIZE = 12

export default function HistoryPage() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadJobs(pageNumber: number = page) {
    setLoading(true)
    setError('')

    try {
      const response = await listJobs(pageNumber, PAGE_SIZE)

      setJobs(response.items)
      setPage(response.page)
      setTotalPages(response.total_pages)
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

  useEffect(() => {
    loadJobs(1)
  }, [])

  function handlePrevious() {
    if (page > 1) {
      loadJobs(page - 1)
    }
  }

  function handleNext() {
    if (page < totalPages) {
      loadJobs(page + 1)
    }
  }

  function handleRefresh() {
    loadJobs(page)
  }

  function handleDownload(job: Job) {
    const imageUrl = getImageUrl(job.image_url)

    if (!imageUrl) return

    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `voryent-${job.id}.png`
    link.target = '_blank'
    link.rel = 'noopener noreferrer'
    link.click()
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">
            Generation History
          </h1>

          <p className="text-gray-500 mt-1">
            View your previously generated images.
          </p>
        </div>

        <button
          type="button"
          onClick={handleRefresh}
          disabled={loading}
          className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:border-voryent-500 hover:text-voryent-600 disabled:opacity-50"
        >
          Refresh
        </button>
      </div>

      {error && <ErrorMessage message={error} />}

      {loading && (
        <div className="flex justify-center py-12">
          <LoadingSpinner />
        </div>
      )}

      {!loading && jobs.length === 0 && (
        <div className="text-center py-16 border border-dashed border-gray-300 rounded-lg">
          <p className="text-gray-500">
            No generations yet.
          </p>

          <p className="text-sm text-gray-400 mt-1">
            Generate your first image from the Studio.
          </p>
        </div>
      )}

      {!loading && jobs.length > 0 && (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map((job) => {
              const imageUrl = getImageUrl(job.image_url)

              return (
                <div
                  key={job.id}
                  className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm"
                >
                  <div className="bg-gray-100 aspect-square flex items-center justify-center">
                    {job.status === 'completed' && imageUrl ? (
                      <img
                        src={imageUrl}
                        alt={job.prompt}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <span className="text-sm text-gray-400">
                        {job.status === 'failed'
                          ? 'Generation failed'
                          : 'Processing...'}
                      </span>
                    )}
                  </div>

                  <div className="p-4">
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {job.prompt}
                    </p>

                    <div className="flex items-center justify-between mt-3">
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
                        {job.aspect_ratio}
                      </span>
                    </div>

                    <div className="flex items-center justify-between mt-3">
                      <span className="text-xs text-gray-500">
                        {new Date(
                          job.created_at,
                        ).toLocaleDateString()}
                      </span>

                      {job.status === 'completed' &&
                        imageUrl && (
                          <button
                            type="button"
                            onClick={() => handleDownload(job)}
                            className="text-sm font-medium text-voryent-600 hover:text-voryent-800"
                          >
                            Download
                          </button>
                        )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="flex items-center justify-center gap-4 mt-8">
            <button
              type="button"
              onClick={handlePrevious}
              disabled={page <= 1 || loading}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm disabled:opacity-40"
            >
              Previous
            </button>

            <span className="text-sm text-gray-600">
              Page {page} of {totalPages}
            </span>

            <button
              type="button"
              onClick={handleNext}
              disabled={page >= totalPages || loading}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}
