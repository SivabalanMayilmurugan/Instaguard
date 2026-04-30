import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Bell, User, Settings, LogOut, ChevronDown } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import ShieldLogo from './ShieldLogo'

export default function Navbar({ onSearch }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [query, setQuery] = useState('')

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim()) onSearch(query.trim())
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header
      className="sticky top-0 z-50 flex items-center gap-4 px-6 py-3"
      style={{
        background: 'rgba(8,12,20,0.85)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255,255,255,0.06)',
      }}
    >
      {/* Brand */}
      <div className="flex items-center gap-2 mr-4 shrink-0">
        <ShieldLogo size={32} />
        <span className="text-lg font-bold">
          <span className="text-white">Insta</span>
          <span className="text-brand-light">Guard</span>
        </span>
      </div>

      {/* Search bar */}
      <form onSubmit={handleSearch} className="flex-1 max-w-xl">
        <div className="relative">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Instagram Username to Scan..."
            className="w-full pl-9 pr-4 py-2 rounded-xl text-sm"
            style={{
              background: 'rgba(255,255,255,0.06)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#f1f5f9',
              outline: 'none',
            }}
            onFocus={(e) => (e.target.style.borderColor = '#3b82f6')}
            onBlur={(e) => (e.target.style.borderColor = 'rgba(255,255,255,0.1)')}
          />
        </div>
      </form>

      <div className="flex items-center gap-2 ml-auto">
        <button
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
          title="Notifications"
        >
          <Bell size={18} />
        </button>

        {/* User dropdown */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen((v) => !v)}
            className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-xl hover:bg-white/5 transition-colors"
          >
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-brand to-indigo-500 flex items-center justify-center text-xs font-bold text-white">
              {user?.full_name?.[0]?.toUpperCase() || 'U'}
            </div>
            <span className="text-sm text-slate-300 hidden sm:block">{user?.full_name}</span>
            <ChevronDown size={14} className="text-slate-500" />
          </button>

          <AnimatePresence>
            {dropdownOpen && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 8 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 mt-2 w-48 rounded-xl py-1 z-50"
                style={{
                  background: '#111827',
                  border: '1px solid rgba(255,255,255,0.1)',
                  boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
                }}
              >
                <div className="px-4 py-2 border-b border-white/5">
                  <p className="text-sm font-medium text-white truncate">{user?.full_name}</p>
                  <p className="text-xs text-slate-500 truncate">{user?.email}</p>
                </div>
                <button className="w-full flex items-center gap-2 px-4 py-2 text-sm text-slate-300 hover:text-white hover:bg-white/5 transition-colors">
                  <Settings size={14} /> Settings
                </button>
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-white/5 transition-colors"
                >
                  <LogOut size={14} /> Sign out
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  )
}
