import { EntityType } from './EntityType.model';

export interface UserSubscribeRequest {
  userId: string;
  userEmail: string;
  entityType: EntityType;
  contentId: string;
}
