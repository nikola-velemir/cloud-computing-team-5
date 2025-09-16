import { UserRole } from './user-role.model';

export interface User {
  userId: string;
  email: string;
  fullName: string;
  username: string;
  role: UserRole;
  birthday: Date;
}
