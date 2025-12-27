'use client';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Task } from '@/lib/api';
import { formatDate } from '@/lib/utils';
import { MoreVertical, ArrowUpDown } from 'lucide-react';

interface TaskTableProps {
  tasks: Task[];
  onTaskClick: (task: Task) => void;
}

export function TaskTable({ tasks, onTaskClick }: TaskTableProps) {
  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { label: string; className: string }> = {
      completed: {
        label: 'Completed',
        className: 'bg-green-500/10 text-green-500 border-green-500/20',
      },
      in_progress: {
        label: 'In Progress',
        className: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
      },
      pending: {
        label: 'Upcoming',
        className: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
      },
    };
    
    const statusInfo = statusMap[status] || {
      label: status.replace('_', ' '),
      className: 'bg-gray-500/10 text-gray-500 border-gray-500/20',
    };
    
    return (
      <Badge variant="outline" className={statusInfo.className}>
        {statusInfo.label}
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
        {priority.charAt(0).toUpperCase() + priority.slice(1)}
      </Badge>
    );
  };

  const handleTaskAction = (e: React.MouseEvent, action: string, task: Task) => {
    e.stopPropagation();
    // Handle task actions (edit, delete, etc.)
    console.log(action, task);
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="rounded-md border bg-card">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[300px]">
              <div className="flex items-center gap-2">
                Task
              </div>
            </TableHead>
            <TableHead>
              <div className="flex items-center gap-2">
                Status
                <ArrowUpDown className="h-3 w-3 text-muted-foreground" />
              </div>
            </TableHead>
            <TableHead>
              <div className="flex items-center gap-2">
                Priority
                <ArrowUpDown className="h-3 w-3 text-muted-foreground" />
              </div>
            </TableHead>
            <TableHead>
              <div className="flex items-center gap-2">
                Due Date
                <ArrowUpDown className="h-3 w-3 text-muted-foreground" />
              </div>
            </TableHead>
            <TableHead>Assigned To</TableHead>
            <TableHead className="w-[50px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks.map((task) => (
            <TableRow
              key={task.id}
              onClick={() => onTaskClick(task)}
              className="cursor-pointer hover:bg-accent/50"
            >
              <TableCell className="font-medium">{task.title}</TableCell>
              <TableCell>{getStatusBadge(task.status)}</TableCell>
              <TableCell>{getPriorityBadge(task.priority)}</TableCell>
              <TableCell className="text-muted-foreground">
                {formatDate(task.due_date)}
              </TableCell>
              <TableCell className="text-muted-foreground">
                {task.assigned_to}
              </TableCell>
              <TableCell onClick={(e) => e.stopPropagation()}>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                    >
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onTaskClick(task)}>
                      View Details
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={(e) => handleTaskAction(e, 'edit', task)}>
                      Edit Task
                    </DropdownMenuItem>
                    <DropdownMenuItem 
                      onClick={(e) => handleTaskAction(e, 'delete', task)}
                      className="text-destructive focus:text-destructive"
                    >
                      Delete Task
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

