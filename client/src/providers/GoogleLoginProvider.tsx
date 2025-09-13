import {useEffect} from "react";
import {api} from "../lib/api"
import {useAuthStore} from "../store/authStore"
import {QueryProvider} from "./QueryProvider";
import {GoogleLogin} from "../islands/react/GoogleLogin"

export const GoogleLoginProvider = ({children}: {children: React.ReactNode}) => {
  return (
    <QueryProvider>
      <GoogleLogin>
        {children}
      </GoogleLogin>
    </QueryProvider>
  )
}