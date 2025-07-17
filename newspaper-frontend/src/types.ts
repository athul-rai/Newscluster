export type ClusterResponse = {
  [key: string]: string[];
};

export type ClusterSummaryResponse = {
  [key: string]: {summary: string; headlines: string[];};
};

export type FetchStatus = 'idle'|'loading'|'error'|'success';

export interface NewsItem {
  title: string;
  summary: string;
  url: string;
  published_at: string;  // or Date if you parse it
}

export interface Cluster {
  id: string;
  summary: string;
  articles: NewsItem[];
}
