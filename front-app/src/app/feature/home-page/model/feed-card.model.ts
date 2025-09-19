import { FeedType } from './feed-type.mode';

export interface FeedCardData {
  id: string;
  type_entity: FeedType;
  name: string;
  image: string;
}
