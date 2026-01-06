import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import StorePortal from './pages/StorePortal'
import UserPortal from './pages/UserPortal'
import StoreRegister from './pages/store/Register'
import StoreLogin from './pages/store/Login'
import StoreDashboard from './pages/store/Dashboard'
import UserRegister from './pages/user/Register'
import UserLogin from './pages/user/Login'
import UserDashboard from './pages/user/Dashboard'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        
        {/* Store Portal */}
        <Route path="/store" element={<StorePortal />}>
          <Route index element={<StoreLogin />} />
          <Route path="register" element={<StoreRegister />} />
          <Route path="dashboard" element={<StoreDashboard />} />
        </Route>
        
        {/* User Portal */}
        <Route path="/user" element={<UserPortal />}>
          <Route index element={<UserLogin />} />
          <Route path="register" element={<UserRegister />} />
          <Route path="dashboard" element={<UserDashboard />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
