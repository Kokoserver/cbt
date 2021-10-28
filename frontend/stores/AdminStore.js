import { get } from 'svelte/store'
import persistSrore from './persistSrore'
const initualState = { user: {}, token:"", isLogin: false }
const store = persistSrore('admin', initualState)
export let currectuser = get(store)

export const login = (user, token, isLogin) => {
  store.set({ user, token, isLogin })
}

export const logout = () => {
 store.set(initualState)
}
export const isAdmin = () => {
  if (currectuser.isLogin) {
    return true
  }
  return false
}

export const getAdminDeatails = () => {
  if (currectuser.user.is_active) {
    return currectuser.user
  }
  return {}
}

export const getAdminToken = () => {
  if (currectuser.user.is_active) {
    return currectuser.token
  }
  return ''
}
