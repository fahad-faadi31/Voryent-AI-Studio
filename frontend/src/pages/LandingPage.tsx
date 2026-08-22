import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-16">
      <div className="text-center py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Voryent AI Studio
        </h1>

        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Create premium AI-generated images for South Asian brands,
          e-commerce, and marketing — powered by cutting-edge generative AI.
        </p>

        <Link
          to="/studio"
          className="bg-voryent-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-voryent-700"
        >
          Start Creating
        </Link>
      </div>

      <div className="grid md:grid-cols-3 gap-8 py-12">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="font-semibold text-lg mb-2">Text to Image</h3>
          <p className="text-gray-600">
            Describe your vision and let AI generate professional-quality
            images in seconds.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="font-semibold text-lg mb-2">
            Multiple Aspect Ratios
          </h3>
          <p className="text-gray-600">
            Generate 1:1, 16:9, and 9:16 images optimized for social media
            and e-commerce.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="font-semibold text-lg mb-2">Commercial Ready</h3>
          <p className="text-gray-600">
            Built for South Asian brands, product photography, and marketing
            creatives.
          </p>
        </div>
      </div>

      <footer className="text-center text-gray-500 py-8 text-sm">
        © {new Date().getFullYear()} Voryent Solutions. All rights reserved.
      </footer>
    </div>
  )
}