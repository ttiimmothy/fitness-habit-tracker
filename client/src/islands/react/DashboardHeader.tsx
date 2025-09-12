import {useAuthStore} from "../../store/authStore";

export const DashboardHeader = () => {
  const { user } = useAuthStore();

  return (
    <>
     {user && <div className="text-2xl font-semibold">Welcome, {user.name || user.email}</div>}
    </>
  )
}