import {useAuthStore} from "../../store/authStore";
import {DarkModeToggle} from "./DarkModeToggle";

export const HeaderRight = () => {
  const {user} = useAuthStore()
  
  return (
    <>
    {user ? (
      <div className="flex items-center gap-5">
        <a className="text-sm opacity-60 hover:opacity-100" href="/">Dashboard</a>
        {/* <a className="text-sm opacity-60 hover:opacity-100" href="/badge-intro">Badges</a> */}
        <a className="text-sm opacity-60 hover:opacity-100" href="/badge">Badges</a>
        <a className="text-sm opacity-60 hover:opacity-100" href="/user">Profile</a>
        <DarkModeToggle />

      </div>
    ) : (
      <div className="flex items-center gap-5">
        <DarkModeToggle />

      </div>
    )}
    </>
  )
}
