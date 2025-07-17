export interface Article {
  title: string;
  url: string;
  summary?: string;
}

export interface Cluster {
  id: string|number;
  summary: string;
  articles: Article[];
}