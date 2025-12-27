'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { taskApi, userApi, Task, TaskStats, User } from '@/lib/api';
import { isAuthenticated, getStoredUser, clearAuth } from '@/lib/auth';
import { Sidebar } from '@/components/Sidebar';
import { MobileMenu } from '@/components/MobileMenu';
import { StatsCards } from '@/components/StatsCards';
import { TaskTable } from '@/components/TaskTable';
import { TaskForm, TaskFormData } from '@/components/TaskForm';
import { ToastContainer, ToastProps } from '@/components/ui/toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Plus, Clock, Bell, Power } from 'lucide-react';
import { cn } from '@/lib/utils';

type StatusFilter = 'all' | 'pending' | 'in_progress' | 'completed';

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [users, setUsers] = useState<User[]>([]);
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
  const [showForm, setShowForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [toasts, setToasts] = useState<ToastProps[]>([]);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }

    loadTasks();
    loadUsers();
  }, [router]);

  useEffect(() => {
    filterTasks();
  }, [tasks, searchQuery, statusFilter]);

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

  const loadUsers = async () => {
    try {
      const data = await userApi.getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Failed to load users:', error);
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

  const filterTasks = () => {
    let filtered = [...tasks];

    // Apply status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter((task) => {
        if (statusFilter === 'pending') return task.status === 'pending';
        if (statusFilter === 'in_progress') return task.status === 'in_progress';
        if (statusFilter === 'completed') return task.status === 'completed';
        return true;
      });
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (task) =>
          task.title.toLowerCase().includes(query) ||
          task.description?.toLowerCase().includes(query) ||
          task.assigned_to.toLowerCase().includes(query)
      );
    }

    setFilteredTasks(filtered);
  };

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task);
    setShowForm(true);
  };

  const handleNewTask = () => {
    setSelectedTask(null);
    setShowForm(true);
  };

  const handleEditTask = (task: Task) => {
    setSelectedTask(task);
    setShowForm(true);
  };

  const handleDeleteTask = async (task: Task) => {
    if (!confirm(`Are you sure you want to delete "${task.title}"?`)) {
      return;
    }

    try {
      await taskApi.deleteTask(task.id);
      await loadTasks();
      showToast('Task deleted', 'The task has been successfully deleted.', 'success');
    } catch (error) {
      console.error('Failed to delete task:', error);
      showToast('Error', 'Failed to delete task. Please try again.', 'error');
    }
  };

  const handleSaveTask = async (formData: TaskFormData) => {
    try {
      const user = getStoredUser();
      if (!user) {
        throw new Error('User not found');
      }

      if (selectedTask) {
        // Update existing task
        await taskApi.updateTask(selectedTask.id, {
          title: formData.title,
          description: formData.description || null,
          start_date: new Date(formData.start_date).toISOString(),
          due_date: new Date(formData.due_date).toISOString(),
          priority: formData.priority,
          status: formData.status,
          assigned_to: formData.assigned_to,
        });
        showToast('Task updated', 'The task has been successfully updated.', 'success');
      } else {
        // Create new task
        await taskApi.createTask({
          title: formData.title,
          description: formData.description || '',
          start_date: new Date(formData.start_date).toISOString(),
          due_date: new Date(formData.due_date).toISOString(),
          priority: formData.priority,
          status: formData.status,
          created_by: user.user_email,
          assigned_to: formData.assigned_to,
        });
        showToast('Task added', 'The task has been successfully created.', 'success');
      }

      await loadTasks();
      setShowForm(false);
      setSelectedTask(null);
    } catch (error) {
      console.error('Failed to save task:', error);
      showToast('Error', selectedTask ? 'Failed to update task.' : 'Failed to create task.', 'error');
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setSelectedTask(null);
  };

  const showToast = (title: string, description: string, variant: 'default' | 'success' | 'error' = 'default') => {
    const id = Date.now().toString();
    const toast: ToastProps = {
      id,
      title,
      description,
      variant,
      onClose: removeToast,
    };
    setToasts((prev) => [...prev, toast]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  const handleLogout = () => {
    clearAuth();
    router.push('/signin');
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="animate-pulse text-muted-foreground">Loading dashboard...</div>
      </div>
    );
  }

  const user = getStoredUser();
  const statusFilters = [
    { label: 'All', value: 'all' as StatusFilter },
    { label: 'Upcoming', value: 'pending' as StatusFilter },
    { label: 'In Progress', value: 'in_progress' as StatusFilter },
    { label: 'Completed', value: 'completed' as StatusFilter },
  ];

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <MobileMenu />
      <div className="flex-1 flex flex-col overflow-hidden md:ml-64">
        {/* Top Header Bar */}
        <header className="border-b bg-card px-6 py-4">
          <div className="flex items-center justify-between">

            <div>
              <h3 className="text-xl font-semibold">Dashboard</h3>
              <p className="text-sm text-muted-foreground">
                {getGreeting()}, {user?.user_name || 'User'}!
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <Clock className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <Bell className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9"
                onClick={handleLogout}
              >
                <Power className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Task Form - Shown at top when adding/editing */}
            {showForm ? (
              <TaskForm
                task={selectedTask}
                users={users}
                currentUserEmail={getStoredUser()?.user_email || ''}
                onSave={handleSaveTask}
                onCancel={handleCancelForm}
              />
            ) : (
              <>
                {/* Statistics Cards */}
                <StatsCards stats={stats} />

                {/* Task Management Section */}
                <div className="space-y-4">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 w-full">
                    {/* Left: Search + Status Filters */}
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 w-full sm:w-auto">
                      {/* Search */}
                      <div className="relative flex-1 max-w-md">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input
                          placeholder="Filter tasks..."
                          value={searchQuery}
                          onChange={e => setSearchQuery(e.target.value)}
                          className="pl-9"
                        />
                      </div>
                      {/* Status Filters */}
                      <div className="flex flex-wrap gap-2 pt-2 sm:pt-0">
                        {statusFilters.map((filter) => (
                          <Button
                            key={filter.value}
                            variant={statusFilter === filter.value ? "default" : "outline"}
                            size="sm"
                            onClick={() => setStatusFilter(filter.value)}
                            className={cn(
                              statusFilter === filter.value && "bg-primary text-primary-foreground"
                            )}
                          >
                            {filter.label}
                          </Button>
                        ))}
                      </div>
                    </div>
                    {/* Right: Add Task Button */}
                    <div className="flex w-full sm:w-auto justify-end">
                      <Button className="gap-2" onClick={handleNewTask}>
                        <Plus className="h-4 w-4" />
                        Add Task
                      </Button>
                    </div>
                  </div>

                  {/* Tasks Table */}
                  <TaskTable
                    tasks={filteredTasks}
                    onTaskClick={handleTaskClick}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                </div>
              </>
            )}
          </div>
        </main>
      </div>

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </div>
  );
}
