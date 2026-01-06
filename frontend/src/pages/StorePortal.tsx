import { Outlet } from 'react-router-dom'

export default function StorePortal() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto">
        <Outlet />
      </div>
    </div>
  )
}
