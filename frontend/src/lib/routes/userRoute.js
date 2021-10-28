// all user router
import UserLayout from '../../View/user/UserLayout.svelte'
import DashboardIndex from '../../View/user/DashboardIndex.svelte'
import ExamCenter from '../../View/user/ExamCenter.svelte'



// import user Store
import { isActive } from '../../../stores/candidate'

function userIsActive() {
  if (isActive()) return true
  return false
}
const userRoutes = [
  {
    name: '/user',
    layout: UserLayout,
    onlyIf: { guard: userIsActive, redirect: '/login' },
    nestedRoutes: [
      { name: 'index', redirectTo: 'user/dashboard' },
      {
        name: 'dashboard',
        component: DashboardIndex,
      },
      {
        name: 'exam-center',
        component: ExamCenter,
      },

      //     {
      //       name: "addresses",
      //       nestedRoutes: [
      //         { name: "index", component: AddressesIndex },
      //         { name: "new", component: AddressesNew },
      //         { name: "edit/:id", component: AddressesEdit },
      //       ],
      //     },
    ],
  },
]

export { userRoutes }
