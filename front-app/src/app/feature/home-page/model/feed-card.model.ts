import { FeedType } from './feed-type.mode';

export interface FeedCardData {
  id: number;
  type: FeedType;
  name: string;
  image: string;
}
