export interface Track {
  id: string;
  name: string;
  artistNames: string[];
  audioUrl: string;
  imageUrl?: string;
  duration: number;
}
