import axios from 'axios'
import { User } from '@/models/User'
import store from '@/store';
const base = 'http://localhost:8000/api'
console.log(base)
export async function reset(user: User) {
  return (
    await axios.post(
      `${base}/users/reset`,
      {},
      {
        headers: getHeaders(user),
      }
    )
  ).data
}

export async function login(username: string, password: string) {
  return (await axios.post(
    `${base}/auth/login/`,
    {username: username, password: password}
  )).data as User
}

function getHeaders(user: User) {
  let headers = { headers: { Authorization: 'Bearer ' + (store as any).state.AppStore.token } }
  return headers;
}
