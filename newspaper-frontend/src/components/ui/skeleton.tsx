import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn("bg-gray-200 dark:bg-gray-700 animate-pulse rounded", className)}
    />
  );
}
