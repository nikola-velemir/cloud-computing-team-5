import { UserRole } from '../../../infrastructure/auth/model/user-role.model';

export interface LoginResponse {
  userId: number;
  email: string;
  fullName: string;
  role: UserRole;
  jwt: string;
  suspensionEndDateTime: Date;
}
