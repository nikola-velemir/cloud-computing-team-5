import { UserRole } from './user-role.model';

export interface User {
  userId: number;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
}
