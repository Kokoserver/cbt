// @ts-ignore
import AdminLayout from '../../View/admin/AdminLayout.svelte'
import AdminDashboardIndex from '../../View/admin/AdminDashboardIndex.svelte'
// all user routes for admin actions
import UserIndex from '../../View/admin/user/UserIndex.svelte'
import EditUser from '../../View/admin/user/EditUser.svelte'



// all course route
// @ts-ignore
import NewExam from '../../View/admin/exam/NewExam.svelte'
import ExamIndex from '../../View/admin/exam/ExamIndex.svelte'
import EditExam from '../../View/admin/exam/EditExam.svelte'


// import admin Store
import { isAdmin } from '../../../stores/AdminStore'

// const store = get(adminStore)
function userIsAdmin() {
  if (isAdmin()) return true
  return false
}

const adminRoutes = [
  {
    name: '/admin',
    layout: AdminLayout,
    onlyIf: { guard: userIsAdmin, redirect: 'adminLogin' },
    nestedRoutes: [
      { name: 'index', redirectTo: 'admin/dashboard' },
      {
        name: 'dashboard',
        component: AdminDashboardIndex,
      },
      {
        name: 'exam',
        nestedRoutes: [
          { name: 'index', component: ExamIndex },
          { name: 'new', component: NewExam },
          { name: 'edit/:id', component: EditExam },
        ],
      },

      {
        name: 'user',
        nestedRoutes: [
          { name: 'index', component: UserIndex },
          { name: 'edit/:id', component: EditUser },
        ],
      },
    ],
  },
]

export { adminRoutes }
