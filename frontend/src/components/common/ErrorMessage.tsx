import { AlertCircle } from "lucide-react";
import { cn } from "@/utils";

interface ErrorMessageProps {
  message: string;
  className?: string;
  onRetry?: () => void;
}

export function ErrorMessage({ message, className, onRetry }: ErrorMessageProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800",
        className
      )}
    >
      <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0" />
      <p className="text-sm text-red-700 dark:text-red-300 flex-1">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-sm font-medium text-red-700 dark:text-red-300 hover:underline"
        >
          Retry
        </button>
      )}
    </div>
  );
}