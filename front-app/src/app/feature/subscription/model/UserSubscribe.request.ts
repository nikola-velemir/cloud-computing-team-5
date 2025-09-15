import { EntityType } from './EntityType.model';

export interface UserSubscribeRequest {
  userId: string;
  entityType: EntityType;
  contentId: string;
}
