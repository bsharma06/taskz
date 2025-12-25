'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { taskApi, Task, TaskStats } from '@/lib/api';
import { isAuthenticated, getStoredUser } from '@/lib/auth';
import { Sidebar } from '@/components/Sidebar';
import { MobileMenu } from '@/components/MobileMenu';
import { StatsCards } from '@/components/StatsCards';
import { TaskTable } from '@/components/TaskTable';
import { TaskDetailModal } from '@/components/TaskDetailModal';

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<TaskStats>({
    total: 0,
    pending: 0,
    in_progress: 0,
    completed: 0,
    high_priority: 0,
    overdue: 0,
  });
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }

    loadTasks();
  }, [router]);

  const loadTasks = async () => {
    try {
      const data = await taskApi.getTasks();
      setTasks(data);
      calculateStats(data);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (taskList: Task[]) => {
    const now = new Date();
    const overdue = taskList.filter((task) => {
      const dueDate = new Date(task.due_date);
      return dueDate < now && task.status !== 'completed';
    }).length;

    const newStats: TaskStats = {
      total: taskList.length,
      pending: taskList.filter((t) => t.status === 'pending').length,
      in_progress: taskList.filter((t) => t.status === 'in_progress').length,
      completed: taskList.filter((t) => t.status === 'completed').length,
      high_priority: taskList.filter((t) => t.priority === 'high').length,
      overdue,
    };
    setStats(newStats);
  };

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task);
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="animate-pulse text-muted-foreground">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <MobileMenu />
      <div className="flex-1 flex flex-col overflow-hidden md:ml-64">
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Header */}
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
              <p className="text-muted-foreground">
                Welcome back, {getStoredUser()?.user_name || 'User'}
              </p>
            </div>

            {/* Statistics Cards */}
            <StatsCards stats={stats} />

            {/* Tasks Table */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-semibold tracking-tight">Tasks</h2>
              </div>
              <TaskTable tasks={tasks} onTaskClick={handleTaskClick} />
            </div>
          </div>
        </main>
      </div>

      {/* Task Detail Modal */}
      <TaskDetailModal
        task={selectedTask}
        open={isModalOpen}
        onOpenChange={setIsModalOpen}
      />
    </div>
  );
}
