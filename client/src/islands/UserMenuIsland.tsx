import {PersistQueryProvider} from "./react/PersistQueryProvider"
import UserMenu from "./react/UserMenu";

export const UserMenuIsland = () => {
  return (
    <PersistQueryProvider>
      <UserMenu/>
    </PersistQueryProvider>
  )
}