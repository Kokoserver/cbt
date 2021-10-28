import axios from 'axios'
export const baseUrl = 'http://127.0.0.1:8000/api'
export const ExamBaseUrl = `${baseUrl}/exam`
export const userBaseUrl = `${baseUrl}/user`
import { getAdminToken } from '../../../stores/AdminStore'
// import { getUserToken } from '../../../stores/studetsStore'
let token = ''
if (getAdminToken() !== undefined || null) {
  token = getAdminToken()
} 

export default axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-type': 'application/json', "Authorization":`Bearer ${token}`},
})
