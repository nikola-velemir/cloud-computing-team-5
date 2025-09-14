import { UserRole } from '../../../infrastructure/auth/model/user-role.model';
import {User} from '../../../infrastructure/auth/model/user.mode';

export interface LoginResponse {
  access_token: string
  id_token: string
  refresh_token: string
  groups: string[]
  user: User
}
