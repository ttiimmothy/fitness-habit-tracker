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