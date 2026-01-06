import { useNavigate } from 'react-router-dom'

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">Guardian</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Connecting stores with surplus food to users who want it. Real-time notifications, location-based matching, and zero waste.
          </p>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-4xl mb-3">🏪</div>
            <h3 className="font-bold text-lg mb-2">For Stores</h3>
            <p className="text-gray-600 text-sm">Upload surplus food images and reach nearby customers instantly</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-4xl mb-3">👤</div>
            <h3 className="font-bold text-lg mb-2">For Users</h3>
            <p className="text-gray-600 text-sm">Set your preferences and get notified when surplus food matches nearby</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-4xl mb-3">📍</div>
            <h3 className="font-bold text-lg mb-2">Location Aware</h3>
            <p className="text-gray-600 text-sm">Smart distance-based matching within your chosen radius</p>
          </div>
        </div>

        {/* Call-to-Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {/* Store Portal */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-blue-100 hover:border-blue-300 transition">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Store Portal</h2>
            <p className="text-gray-600 mb-6">
              Manage your store profile, upload surplus food images, and reach customers in real-time.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => navigate('/store')}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition"
              >
                Store Login
              </button>
              <button
                onClick={() => navigate('/store/register')}
                className="w-full bg-blue-100 hover:bg-blue-200 text-blue-700 font-bold py-3 px-4 rounded-lg transition"
              >
                Register as Store
              </button>
            </div>
          </div>

          {/* User Portal */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-green-100 hover:border-green-300 transition">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">User Portal</h2>
            <p className="text-gray-600 mb-6">
              Set your food preferences, choose your location radius, and get notified about nearby surplus food.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => navigate('/user')}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition"
              >
                User Login
              </button>
              <button
                onClick={() => navigate('/user/register')}
                className="w-full bg-green-100 hover:bg-green-200 text-green-700 font-bold py-3 px-4 rounded-lg transition"
              >
                Register as User
              </button>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-bold text-lg text-blue-600 mb-3">For Stores</h4>
              <ol className="space-y-2 text-gray-700">
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-blue-600">1.</span>
                  <span>Register and set your store location</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-blue-600">2.</span>
                  <span>Upload photos of surplus food items</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-blue-600">3.</span>
                  <span>AI detects items automatically</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-blue-600">4.</span>
                  <span>Matching users get notified instantly</span>
                </li>
              </ol>
            </div>
            <div>
              <h4 className="font-bold text-lg text-green-600 mb-3">For Users</h4>
              <ol className="space-y-2 text-gray-700">
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-green-600">1.</span>
                  <span>Register and set your location</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-green-600">2.</span>
                  <span>Choose food items you're interested in</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-green-600">3.</span>
                  <span>Set your search radius (1-50 km)</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-3 text-green-600">4.</span>
                  <span>Get email alerts when items match</span>
                </li>
              </ol>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-600 text-sm">
          <p>Guardian • Making surplus food accessible to everyone</p>
        </div>
      </div>
    </div>
  )
}
