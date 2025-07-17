"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Newspaper, ExternalLink, RefreshCw, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

interface Article {
  title: string;
  url: string;
  summary?: string;
}

interface Cluster {
  id: string;
  summary: string;
  articles: Article[];
}

const Index = () => {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchClusters = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get<Cluster[]>("http://127.0.0.1:8000/api/news");
      setClusters(response.data);
    } catch (error) {
      console.error("Error fetching news:", error);
      setError("Failed to fetch clusters. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClusters();
  }, []);

  const pageBg = "bg-[#f9fafb]";
  const headerBg = "bg-gradient-to-r from-blue-600 to-blue-900";

  if (loading) {
    return (
      <div className={`min-h-screen ${pageBg}`}>
        <div className={`${headerBg} text-white`}>
          <div className="container mx-auto px-4 py-16 text-center">
            <Skeleton className="h-16 w-96 mx-auto mb-4 bg-white/20" />
            <Skeleton className="h-6 w-80 mx-auto bg-white/20" />
          </div>
        </div>

        <div className="container mx-auto px-4 py-12">
          <div className="max-w-5xl mx-auto space-y-6">
            {[1, 2, 3].map((i) => (
              <Card key={i} className="border-0 shadow">
                <CardContent className="p-8">
                  <Skeleton className="h-8 w-3/4 mb-4" />
                  <div className="space-y-3">
                    <Skeleton className="h-5 w-full" />
                    <Skeleton className="h-5 w-4/5" />
                    <Skeleton className="h-5 w-3/5" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`min-h-screen ${pageBg} flex items-center justify-center`}>
        <Card className="max-w-md mx-4 border-0 shadow">
          <CardContent className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2 text-gray-900">Something went wrong</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <Button onClick={fetchClusters} className="bg-blue-600 hover:bg-blue-700 text-white">
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${pageBg}`}>
      {/* Hero Section */}
      <div className={`${headerBg} text-white`}>
        <div className="container mx-auto px-4 py-16 text-center">
          <div className="flex items-center justify-center mb-6">
            <Newspaper className="h-12 w-12 mr-4" />
            <h1 className="text-5xl font-bold tracking-tight">NewsCluster</h1>
          </div>
          <p className="text-xl text-white/90 max-w-2xl mx-auto">
            Discover today's most important stories, intelligently grouped and summarized
          </p>
        </div>
      </div>

      {/* News Clusters */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
            Today's News Clusters
          </h2>

          <div className="space-y-12">
            {clusters.map((cluster) => (
              <div key={cluster.id} className="space-y-6">
                <h3 className="text-2xl font-semibold text-gray-800">
                  📌 {cluster.summary}
                </h3>

                <div className="space-y-4">
                  {cluster.articles.map((article, idx) => (
                    <Card key={idx} className="border border-gray-200 rounded-lg shadow-sm hover:shadow transition">
                      <CardContent className="p-4">
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-start justify-between gap-4"
                        >
                          <div className="flex-1">
                            <h4 className="text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors duration-200 mb-1">
                              {article.title}
                            </h4>
                            {article.summary && (
                              <p className="text-gray-600 text-sm">{article.summary}</p>
                            )}
                          </div>
                          <ExternalLink className="h-4 w-4 text-gray-500 flex-shrink-0 mt-1" />
                        </a>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                <div className="pt-2 border-t border-gray-200">
                  <p className="text-sm text-gray-500">
                    {cluster.articles.length} related{" "}
                    {cluster.articles.length === 1 ? "article" : "articles"}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
