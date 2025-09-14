import {useEffect} from "react";
import {api} from "../lib/api"
import {useAuthStore} from "../store/authStore"
import {QueryProvider} from "./QueryProvider";
import {GoogleLoginApi} from "../islands/react/GoogleLoginApi"

export const GoogleLoginProvider = ({children}: {children: React.ReactNode}) => {
  return (
    <QueryProvider>
      <GoogleLoginApi>
        {children}
      </GoogleLoginApi>
    </QueryProvider>
  )
}