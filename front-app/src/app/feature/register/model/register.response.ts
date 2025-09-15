import { UserRole } from '../../../infrastructure/auth/model/user-role.model';

export interface RegisterResponse {
  email: string;
  username: string;
  userRole: UserRole;
}
