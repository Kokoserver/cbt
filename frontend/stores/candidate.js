import { get } from 'svelte/store'
import persistSrore from './persistSrore'
const initualState = { user: {matric_no:"", question:[{}]},  isLogin: false }
export const candidateStore = persistSrore('candidate', initualState)
export const currectuser = get(candidateStore)

export const login = (user={},  isLogin=false) => {
  candidateStore.set({ user, isLogin })
}

export const logout = () => {
  candidateStore.set(initualState)
}
export const isActive = () => {
  if (currectuser.isLogin) {
    return true
  }
  return false
}

export const getUserDeatails = () => {
  if (currectuser.isLogin) {
    return currectuser.user.matric_no
  }
  return {}
}

export const getUserToken = () => {
  if (currectuser.isLogin) {
    return currectuser.token
  }
  return ''
}
