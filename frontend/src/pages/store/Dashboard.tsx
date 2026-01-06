import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { storeAuthService } from '@/services/storeService'
import { DetectionResult } from '@/types'

export default function StoreDashboard() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [uploadHistory, setUploadHistory] = useState<DetectionResult[]>([])
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>('')

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      navigate('/store')
    }
    loadHistory()
  }, [navigate])

  const loadHistory = async () => {
    try {
      const history = await storeAuthService.getUploadHistory()
      setUploadHistory(history.items ?? [])
    } catch (err: any) {
      console.error('Failed to load history:', err)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const result = await storeAuthService.uploadImage(selectedFile)
      setSuccess(`Image uploaded successfully! Detected items: ${result.items?.join(', ') || 'Processing...'}`)
      setSelectedFile(null)
      setPreviewUrl('')
      ;(e.target as HTMLFormElement).reset()
      // Reload history
      loadHistory()
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    storeAuthService.logout()
    navigate('/store')
  }

  return (
    <div className="py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Store Dashboard</h1>
            <p className="text-gray-600 mt-2">Upload photos to detect items and trigger notifications</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Upload Photo</h2>

            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
                {error}
              </div>
            )}

            {success && (
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-600">
                {success}
              </div>
            )}

            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Image
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition cursor-pointer">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-input"
                  />
                  <label htmlFor="file-input" className="cursor-pointer">
                    {previewUrl ? (
                      <div>
                        <img
                          src={previewUrl}
                          alt="Preview"
                          className="h-48 mx-auto mb-2 rounded-lg object-cover"
                        />
                        <p className="text-sm text-gray-600">
                          {selectedFile?.name}
                        </p>
                      </div>
                    ) : (
                      <div>
                        <svg
                          className="mx-auto h-12 w-12 text-gray-400 mb-2"
                          stroke="currentColor"
                          fill="none"
                          viewBox="0 0 48 48"
                        >
                          <path
                            d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-8-12l-3.172-3.172a4 4 0 00-5.656 0L9.172 15M33 5v6m0 0v6m0-6h6m0 0h6"
                            strokeWidth={2}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                        <p className="text-gray-600">
                          Click to upload a photo
                        </p>
                      </div>
                    )}
                  </label>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || !selectedFile}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
              >
                {loading ? 'Uploading...' : 'Upload & Process'}
              </button>
            </form>
          </div>

          {/* Recent Uploads */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Recent Uploads</h2>

            {uploadHistory.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                No uploads yet. Start by uploading a photo!
              </p>
            ) : (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {uploadHistory.map((upload) => (
                  <div
                    key={upload.id}
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition"
                  >
                    <p className="text-sm text-gray-500">
                      {new Date(upload.timestamp).toLocaleString()}
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {upload.items.map((item) => (
                        <span
                          key={item}
                          className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
                        >
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
