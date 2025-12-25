'use client';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/lib/api';
import { formatDate } from '@/lib/utils';

interface TaskDetailModalProps {
  task: Task | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function TaskDetailModal({ task, open, onOpenChange }: TaskDetailModalProps) {
  if (!task) return null;

  const getStatusBadge = (status: string) => {
    const variants: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
      completed: 'default',
      in_progress: 'secondary',
      pending: 'outline',
    };
    return (
      <Badge variant={variants[status] || 'outline'}>
        {status.replace('_', ' ')}
      </Badge>
    );
  };

  const getPriorityBadge = (priority: string) => {
    const colors: Record<string, string> = {
      high: 'bg-red-500/10 text-red-500 border-red-500/20',
      medium: 'bg-orange-500/10 text-orange-500 border-orange-500/20',
      low: 'bg-gray-500/10 text-gray-500 border-gray-500/20',
    };
    return (
      <Badge variant="outline" className={colors[priority] || colors.low}>
        {priority}
      </Badge>
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">{task.title}</DialogTitle>
          <DialogDescription>
            Task details and information
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          {task.description && (
            <div>
              <h4 className="text-sm font-medium mb-2">Description</h4>
              <p className="text-sm text-muted-foreground">{task.description}</p>
            </div>
          )}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium mb-2">Status</h4>
              {getStatusBadge(task.status)}
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Priority</h4>
              {getPriorityBadge(task.priority)}
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Start Date</h4>
              <p className="text-sm text-muted-foreground">
                {formatDate(task.start_date)}
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Due Date</h4>
              <p className="text-sm text-muted-foreground">
                {formatDate(task.due_date)}
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Created By</h4>
              <p className="text-sm text-muted-foreground">{task.created_by}</p>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Assigned To</h4>
              <p className="text-sm text-muted-foreground">{task.assigned_to}</p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

