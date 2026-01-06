import { Outlet } from 'react-router-dom'

export default function UserPortal() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto">
        <Outlet />
      </div>
    </div>
  )
}
