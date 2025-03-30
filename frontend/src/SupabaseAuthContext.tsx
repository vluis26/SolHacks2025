import { createContext, useContext, useEffect, useState, ReactNode } from "react"
import { supabase } from "./supabase"
import type { Session, User } from "@supabase/supabase-js"

interface AuthContextType {
  user: User | null
  session: Session | null
  loading: boolean
}

const SupabaseAuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
  loading: true,
})

export const SupabaseAuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const accessToken = urlParams.get("access_token")
    const refreshToken = urlParams.get("refresh_token")
    console.log(accessToken)
    console.log(refreshToken)

    const init = async () => {
      if (accessToken) {
        const { data, error } = await supabase.auth.setSession({
          access_token: accessToken,
          refresh_token: refreshToken || "",
        })

        if (error) {
          console.log(error.message)
        }

        if (!error && data.session) {
          setUser(data.session.user)
          setSession(data.session)
          localStorage.setItem("access_token", accessToken)
          localStorage.setItem("refresh_token", refreshToken || "")
        }

        window.history.replaceState({}, "", window.location.pathname)
      } else {
        const storedAccess = localStorage.getItem("access_token")
        const storedRefresh = localStorage.getItem("refresh_token")

        if (storedAccess && storedRefresh) {
          const { data } = await supabase.auth.setSession({
            access_token: storedAccess,
            refresh_token: storedRefresh,
          })
          setUser(data.session?.user ?? null)
          setSession(data.session ?? null)
        }
      }

      setLoading(false)
    }

    init()
  }, [])

  return (
    <SupabaseAuthContext.Provider value={{ user, session, loading }}>
      {children}
    </SupabaseAuthContext.Provider>
  )
}

export const useSupabaseAuth = () => useContext(SupabaseAuthContext)
