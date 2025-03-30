import Dashboard from './custom_components/Dashboard'
import { useSupabaseAuth } from "./SupabaseAuthContext"

function App() {
  const { user, loading } = useSupabaseAuth()

  if (loading) return <p>Loading...</p>

  return user ? <Dashboard/> : <h1>You are not logged in</h1>
}

export default App
