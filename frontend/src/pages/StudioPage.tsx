import { useState, useEffect, useRef } from 'react'
import { createGeneration } from '../api/generate'
import { getJob } from '../api/jobs'
import { getImageUrl } from '../api/client'
import type { AspectRatio, Job } from '../types'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

const ASPECT_RATIOS: AspectRatio[] = ['1:1', '16:9', '9:16']

export default function StudioPage() {
  const [prompt, setPrompt] = useState('')
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>('1:1')
  const [seed, setSeed] = useState('')
  const [error, setError] = useState('')
  const [job, setJob] = useState<Job | null>(null)
  const [polling, setPolling] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current)
      }
    }
  }, [])

  async function handleGenerate() {
    setError('')
    setJob(null)

    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    if (prompt.trim().length > 500) {
      setError('Prompt must be 500 characters or less')
      return
    }

    setSubmitting(true)

    try {
      const seedValue = seed.trim() ? parseInt(seed, 10) : null

      if (seed.trim() && Number.isNaN(seedValue)) {
        setError('Seed must be a valid number')
        setSubmitting(false)
        return
      }

      const response = await createGeneration({
        prompt: prompt.trim(),
        aspect_ratio: aspectRatio,
        seed: seedValue,
      })

      setJob(response)
      setPolling(true)
      startPolling(response.id)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Generation request failed',
      )
    } finally {
      setSubmitting(false)
    }
  }

  function startPolling(jobId: string) {
    let attempts = 0
    const MAX_ATTEMPTS = 30

    async function poll() {
      try {
        const currentJob = await getJob(jobId)

        setJob(currentJob)

        if (
          currentJob.status === 'completed' ||
          currentJob.status === 'failed'
        ) {
          setPolling(false)

          if (pollingRef.current) {
            clearInterval(pollingRef.current)
            pollingRef.current = null
          }

          return
        }

        attempts++

        if (attempts >= MAX_ATTEMPTS) {
          setPolling(false)

          if (pollingRef.current) {
            clearInterval(pollingRef.current)
            pollingRef.current = null
          }

          setError('Generation timed out. Please try again.')
        }
      } catch (err) {
        setPolling(false)

        if (pollingRef.current) {
          clearInterval(pollingRef.current)
          pollingRef.current = null
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Failed to check job status',
        )
      }
    }

    poll()

    pollingRef.current = setInterval(poll, 2000)
  }

  const imageUrl = getImageUrl(job?.image_url || null)

  const isProcessing =
    polling ||
    job?.status === 'queued' ||
    job?.status === 'processing'

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">
        AI Image Studio
      </h1>

      {error && <ErrorMessage message={error} />}

      <div className="grid md:grid-cols-2 gap-8 mt-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Prompt
            </label>

            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              rows={4}
              maxLength={500}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-voryent-500"
            />

            <p className="text-xs text-gray-500 mt-1">
              {prompt.length}/500
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Aspect Ratio
            </label>

            <div className="flex gap-2">
              {ASPECT_RATIOS.map((ratio) => (
                <button
                  key={ratio}
                  type="button"
                  onClick={() => setAspectRatio(ratio)}
                  className={`px-4 py-2 rounded-md border ${
                    aspectRatio === ratio
                      ? 'bg-voryent-600 text-white border-voryent-600'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-voryent-500'
                  }`}
                >
                  {ratio}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Seed (optional)
            </label>

            <input
              type="number"
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              placeholder="Random"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-voryent-500"
            />
          </div>

          <button
            type="button"
            onClick={handleGenerate}
            disabled={submitting || Boolean(isProcessing)}
            className="w-full bg-voryent-600 text-white py-3 rounded-md hover:bg-voryent-700 disabled:opacity-50"
          >
            {submitting ? 'Submitting...' : 'Generate'}
          </button>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4 min-h-[400px] flex items-center justify-center">
          {isProcessing && (
            <div className="text-center">
              <LoadingSpinner />

              <p className="text-gray-600 mt-4">
                {job?.status === 'queued'
                  ? 'Queued...'
                  : 'Processing...'}
              </p>
            </div>
          )}

          {job?.status === 'failed' && (
            <div className="text-center">
              <p className="text-red-600">
                {job.error_message || 'Generation failed'}
              </p>
            </div>
          )}

          {job?.status === 'completed' && imageUrl && (
            <img
              src={imageUrl}
              alt={job.prompt}
              className="max-w-full h-auto rounded-md"
            />
          )}

          {!isProcessing && !job && (
            <p className="text-gray-400 text-center">
              Your generated image will appear here
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

