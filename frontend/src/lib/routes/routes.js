import { publicRoutes } from '../routes/publicRoute'
import { adminRoutes } from '../routes/adminRoute'
import { userRoutes } from './userRoute'

const routes = [...publicRoutes, ...adminRoutes, ...userRoutes]

export { routes }
