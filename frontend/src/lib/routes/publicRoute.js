// all public route
import PublicLayout from '../../View/public/PublicLayout.svelte'
import Login from '../../View/public/Login.svelte'
import AdminLogin from '../../View/public/AdminLogin.svelte'
import Forgotpassword from '../../View/public/forgotpassword.svelte'
import Register from '../../View/public/Register.svelte'
import NotFound from '../../View/public/NotFound.svelte'

// import { isAdmin } from '../../../stores/AdminStore'
// import {isActive} from "../../../stores/userStore"

// const store = get(adminStore)
function userIsActive() {
  // if (!isActive() || !isAdmin()) return false
  return false
}

const publicRoutes = [
  {
    name: '/',
    component: PublicLayout,
    onlyIf: { guard: userIsActive, redirect: 'login' },
  },
  { name: 'login', component: Login, layout: PublicLayout },
  { name: 'adminLogin', component: AdminLogin, layout: PublicLayout },
  { name: 'register', component: Register, layout: PublicLayout },
  { name: 'forgotpassword', component: Forgotpassword, layout: PublicLayout },
  { name: '404', component: NotFound },
]

export { publicRoutes }
