import { UserRole } from './user-role.model';

export interface User {
  userId: number;
  email: string;
  fullName: string;
  username: string;
  role: UserRole;
  birthday:Date
}
