import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { userAuthService } from '@/services/userService'
import { geocodeAddress } from '@/services/geocoding'
import { Tag } from '@/types'

export default function UserDashboard() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [availableTags, setAvailableTags] = useState<Tag[]>([])
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [location, setLocation] = useState('')
  const [radius, setRadius] = useState(5)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      navigate('/user')
      return
    }
    loadData()
  }, [navigate])

  const loadData = async () => {
    try {
      setLoading(true)
      const [tags, prefs] = await Promise.all([
        userAuthService.getAvailableTags(),
        userAuthService.getPreferences(),
      ])
      setAvailableTags(tags)
      setSelectedTags(prefs.tags || [])
    } catch (err: any) {
      setError('Failed to load preferences')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleTagToggle = (tagId: string) => {
    setSelectedTags((prev) =>
      prev.includes(tagId)
        ? prev.filter((t) => t !== tagId)
        : [...prev, tagId]
    )
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      // Geocode location if provided
      let lat: number | undefined
      let lng: number | undefined
      if (location && location.trim()) {
        const coords = await geocodeAddress(location)
        lat = coords.lat
        lng = coords.lng
      }

      await userAuthService.updatePreferences(selectedTags, {
        lat,
        lng,
        radius_km: radius,
      })
      setSuccess('Preferences saved successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.message || err.response?.data?.error || 'Failed to save preferences')
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = () => {
    userAuthService.logout()
    navigate('/user')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          <p className="mt-4 text-gray-600">Loading preferences...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">My Preferences</h1>
            <p className="text-gray-600 mt-2">Choose what items you're interested in to receive notifications</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition"
          >
            Logout
          </button>
        </div>

        {/* Preferences Section */}
        <div className="bg-white rounded-lg shadow-lg p-8">
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

          <form onSubmit={handleSave} className="space-y-6">
            {/* Location & Radius Section */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                📍 Location Preferences
              </h2>
              <p className="text-gray-600 mb-4">
                Enter your location to get notified about nearby stores
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Address (or City, Zip Code)
                  </label>
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g., San Francisco, CA or 123 Main St"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Leave empty if you don't want location-based filtering
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Notification Radius: {radius} km
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="50"
                    value={radius}
                    onChange={(e) => setRadius(parseInt(e.target.value))}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Only get notified about stores within this distance
                  </p>
                </div>
              </div>
            </div>

            {/* Tags Section */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Select Your Interests
              </h2>
              <p className="text-gray-600 mb-4">
                We'll notify you when stores upload these items
              </p>

              {availableTags.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  No tags available yet
                </p>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {availableTags.map((tag) => (
                    <label
                      key={tag.id}
                      className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition ${
                        selectedTags.includes(tag.id)
                          ? 'border-green-500 bg-green-50'
                          : 'border-gray-200 hover:border-green-300'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedTags.includes(tag.id)}
                        onChange={() => handleTagToggle(tag.id)}
                        className="w-5 h-5 text-green-600 rounded focus:ring-2 focus:ring-green-500 cursor-pointer"
                      />
                      <span className="ml-3 text-gray-700 font-medium">
                        {tag.name}
                      </span>
                    </label>
                  ))}
                </div>
              )}
            </div>

            {/* Summary */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-sm text-gray-600">
                You'll receive notifications for{' '}
                <span className="font-semibold text-green-700">
                  {selectedTags.length} item{selectedTags.length !== 1 ? 's' : ''}
                </span>
              </p>
              {selectedTags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {selectedTags.map((tagId) => {
                    const tag = availableTags.find((t) => t.id === tagId)
                    return (
                      <span
                        key={tagId}
                        className="inline-block bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full"
                      >
                        {tag?.name}
                      </span>
                    )
                  })}
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={saving}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition"
            >
              {saving ? 'Saving...' : 'Save Preferences'}
            </button>
          </form>
        </div>

        {/* Info Section */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">💬 Notifications</h3>
            <p className="text-sm text-blue-800">
              Receive real-time notifications when stores upload items matching your interests.
            </p>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-semibold text-purple-900 mb-2">🔍 Smart Detection</h3>
            <p className="text-sm text-purple-800">
              Our AI system detects fresh produce, bakery items, and more from store photos.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
