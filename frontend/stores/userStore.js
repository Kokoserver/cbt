import persistSrore from './persistSrore'
import {writable} from 'svelte/store'

export const userStore = writable([{}])

// export const find = (id) => {
//   return userData.find((user) => {
//     return user.id == id
//   })
// }
// export const remove = (id) => {
//   let data = userData.find((user) => {
//     return user.id == !id
//   })
//   // userStore.set(data)
//   return true
// }
